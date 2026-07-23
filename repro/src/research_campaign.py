"""Faithful CPU checks for the steady-state SA claims in arXiv:2602.13960.

This route uses separable d-dimensional systems.  Independence lets coordinate
Wasserstein-1 distances bracket the paper's Euclidean multivariate W1:

    max_i W1(mu_i, nu_i) <= W1(mu, nu) <= sum_i W1(mu_i, nu_i).

The upper bound follows by coupling the independent coordinates optimally and
using ||x||_2 <= ||x||_1.  Thus the experiment tests a real d-dimensional W1
claim without replacing it by sliced Wasserstein or an arbitrary proxy.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.special import gammaincinv, ndtr, ndtri
from scipy.stats import t as student_t


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_ROOT = ROOT / ".openresearch" / "artifacts"
DIMENSION = 8
ALPHAS = np.array([0.08, 0.04, 0.02, 0.01, 0.005], dtype=float)
GIBBS_ALPHAS = np.array([0.08, 0.04, 0.02, 0.01], dtype=float)
SEEDS = (1729, 2718, 3141, 5772)
GAUSSIAN_CHAINS_PER_SEED = 4096
GAUSSIAN_BATCHES = 8
GIBBS_CHAINS_PER_SEED = 512
GIBBS_BATCHES = 6
IID_REFRESH_PROB = 1.0
MARKOV_RHO = 0.55
SKEW_PROB = 1.0 / 3.0
THRESHOLDS = np.array([0.45, 0.70, 0.95, 1.20], dtype=float)


@dataclass(frozen=True)
class Family:
    name: str
    target_precision: np.ndarray


LINEAR_RATE = np.linspace(0.70, 1.40, DIMENSION)
SGD_QUADRATIC = np.linspace(0.80, 1.50, DIMENSION)
SGD_SINE = np.linspace(0.10, 0.16, DIMENSION)
CONTRACTION = np.linspace(0.20, 0.65, DIMENSION)
FAMILIES = {
    "sgd": Family("sgd", SGD_QUADRATIC + SGD_SINE),
    "linear": Family("linear", LINEAR_RATE),
    "contractive": Family("contractive", 1.0 - CONTRACTION),
}
MIN_CONTRACTION = min(
    float(np.min(SGD_QUADRATIC - SGD_SINE)),
    float(np.min(LINEAR_RATE)),
    float(np.min(1.0 - CONTRACTION)),
)


def git_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def skew_noise(state: np.ndarray) -> np.ndarray:
    high = math.sqrt((1.0 - SKEW_PROB) / SKEW_PROB)
    low = -math.sqrt(SKEW_PROB / (1.0 - SKEW_PROB))
    return np.where(state, high, low)


def directions() -> dict[str, np.ndarray]:
    result = {
        "axis_0": np.eye(DIMENSION)[0],
        "axis_3": np.eye(DIMENSION)[3],
        "mean": np.ones(DIMENSION) / math.sqrt(DIMENSION),
    }
    alt = np.where(np.arange(DIMENSION) % 2 == 0, 1.0, -1.0)
    result["alternating"] = alt / np.linalg.norm(alt)
    return result


def update_states(
    rng: np.random.Generator,
    state: np.ndarray,
    refresh_probability: float,
) -> None:
    refresh = rng.random(state.shape) < refresh_probability
    if np.any(refresh):
        state[refresh] = rng.random(int(np.sum(refresh))) < SKEW_PROB


def simulate_family_samples(
    alpha: float,
    seed: int,
    *,
    markov: bool,
) -> dict[str, np.ndarray]:
    """Simulate independent stationary chains for all three model families."""
    rng = np.random.default_rng(seed)
    shape = (GAUSSIAN_CHAINS_PER_SEED, DIMENSION)
    state = rng.random(shape) < SKEW_PROB
    x_sgd = np.zeros(shape)
    x_linear = np.zeros(shape)
    x_contract = np.zeros(shape)
    rho = MARKOV_RHO if markov else 0.0
    refresh_probability = 1.0 - rho
    burn = int(math.ceil(9.0 / (alpha * MIN_CONTRACTION)))
    gap = int(math.ceil(0.75 / (alpha * MIN_CONTRACTION)))

    def step() -> None:
        update_states(rng, state, refresh_probability)
        xi = skew_noise(state)
        x_sgd[:] += alpha * (
            -(SGD_QUADRATIC * x_sgd + SGD_SINE * np.sin(x_sgd)) + xi
        )
        x_linear[:] += alpha * (-LINEAR_RATE * x_linear + xi)
        x_contract[:] += alpha * (
            CONTRACTION * np.tanh(x_contract) - x_contract + xi
        )

    for _ in range(burn):
        step()

    collected = {"sgd": [], "linear": [], "contractive": []}
    for _ in range(GAUSSIAN_BATCHES):
        for _ in range(gap):
            step()
        scale = math.sqrt(alpha)
        collected["sgd"].append((x_sgd / scale).copy())
        collected["linear"].append((x_linear / scale).copy())
        collected["contractive"].append((x_contract / scale).copy())
    return {name: np.concatenate(parts, axis=0) for name, parts in collected.items()}


def normal_quantiles(n: int, sd: float) -> np.ndarray:
    q = (np.arange(n, dtype=float) + 0.5) / n
    return sd * ndtri(q)


def coordinate_w1(samples: np.ndarray, target_var: np.ndarray) -> np.ndarray:
    values = np.empty(samples.shape[1])
    for j in range(samples.shape[1]):
        ordered = np.sort(samples[:, j])
        values[j] = float(
            np.mean(np.abs(ordered - normal_quantiles(len(ordered), math.sqrt(target_var[j]))))
        )
    return values


def projection_tail_rows(
    samples: np.ndarray,
    target_var: np.ndarray,
    *,
    alpha: float,
    seed: int,
    noise: str,
    model: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for direction_name, zeta in directions().items():
        projection = samples @ zeta
        variance = float(np.sum((zeta**2) * target_var))
        sd = math.sqrt(variance)
        for threshold in THRESHOLDS:
            empirical = float(np.mean(projection > threshold))
            gaussian = float(1.0 - ndtr(threshold / sd))
            gap = abs(empirical - gaussian)
            n = len(projection)
            # Conservative normal approximation for a Bernoulli difference:
            # empirical tail is random; the Gaussian reference is fixed.
            se = math.sqrt(max(empirical * (1.0 - empirical), 1.0 / n) / n)
            upper95 = gap + 1.96 * se
            rate = alpha**0.25 * math.sqrt(math.log(1.0 / alpha)) / threshold
            rows.append(
                {
                    "claim": 4 if noise == "iid" else 5,
                    "noise": noise,
                    "model": model,
                    "alpha": alpha,
                    "seed": seed,
                    "direction": direction_name,
                    "threshold": float(threshold),
                    "empirical_tail": empirical,
                    "gaussian_tail": gaussian,
                    "gap": gap,
                    "gap_upper95": upper95,
                    "theorem_rate": rate,
                    "normalized_upper": upper95 / rate,
                }
            )
    return rows


def target_variance(model: str, *, markov: bool) -> np.ndarray:
    long_run = (1.0 + MARKOV_RHO) / (1.0 - MARKOV_RHO) if markov else 1.0
    return long_run / (2.0 * FAMILIES[model].target_precision)


def aggregate_mean_ci(values: list[float]) -> tuple[float, float, float]:
    arr = np.asarray(values, dtype=float)
    mean = float(np.mean(arr))
    if len(arr) < 2:
        return mean, mean, mean
    half = float(student_t.ppf(0.975, len(arr) - 1) * np.std(arr, ddof=1) / math.sqrt(len(arr)))
    return mean, max(0.0, mean - half), mean + half


def fit_slope(alphas: np.ndarray, values: np.ndarray) -> float:
    return float(np.polyfit(np.log(alphas), np.log(np.maximum(values, 1e-12)), 1)[0])


def run_gaussian_campaign() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    metric_rows: list[dict[str, object]] = []
    tail_rows: list[dict[str, object]] = []
    cached: dict[tuple[str, str, float], list[dict[str, float]]] = {}
    for noise in ("iid", "markov"):
        markov = noise == "markov"
        for alpha in ALPHAS:
            by_seed: dict[str, list[dict[str, float]]] = {name: [] for name in FAMILIES}
            for seed in SEEDS:
                samples = simulate_family_samples(float(alpha), seed + (100_000 if markov else 0), markov=markov)
                for model, model_samples in samples.items():
                    target_var = target_variance(model, markov=markov)
                    coord = coordinate_w1(model_samples, target_var)
                    record = {
                        "coordinate_mean": float(np.mean(coord)),
                        "w1_lower": float(np.max(coord)),
                        "w1_upper": float(np.sum(coord)),
                    }
                    by_seed[model].append(record)
                    tail_rows.extend(
                        projection_tail_rows(
                            model_samples,
                            target_var,
                            alpha=float(alpha),
                            seed=seed,
                            noise=noise,
                            model=model,
                        )
                    )
            for model, records in by_seed.items():
                cached[(noise, model, float(alpha))] = records
                row: dict[str, object] = {
                    "claim": 2 if model == "sgd" and noise == "iid" else (3 if noise == "iid" else 5),
                    "noise": noise,
                    "model": model,
                    "alpha": float(alpha),
                    "dimension": DIMENSION,
                    "independent_seeds": len(SEEDS),
                    "samples_per_seed": GAUSSIAN_CHAINS_PER_SEED * GAUSSIAN_BATCHES,
                    "theorem_rate": float(math.sqrt(alpha) * math.log(1.0 / alpha)),
                }
                for key in ("coordinate_mean", "w1_lower", "w1_upper"):
                    mean, low, high = aggregate_mean_ci([r[key] for r in records])
                    row[key] = mean
                    row[f"{key}_ci_low"] = low
                    row[f"{key}_ci_high"] = high
                row["normalized_upper_ci"] = float(row["w1_upper_ci_high"]) / float(row["theorem_rate"])
                metric_rows.append(row)

    diagnostics: dict[str, object] = {"models": {}}
    all_pass = True
    negative_control_failures = 0
    for noise in ("iid", "markov"):
        for model in FAMILIES:
            rows = [r for r in metric_rows if r["noise"] == noise and r["model"] == model]
            rows.sort(key=lambda r: float(r["alpha"]), reverse=True)
            ratios = np.array([float(r["normalized_upper_ci"]) for r in rows])
            calibrator = 1.50 * float(np.max(ratios[:3]))
            holdout_pass = bool(np.all(ratios[3:] <= calibrator))
            coord_means = np.array([float(r["coordinate_mean"]) for r in rows])
            slope = fit_slope(np.array([float(r["alpha"]) for r in rows]), coord_means)
            # Wrong O(alpha) envelope is deliberately too fast for skew noise.
            wrong_ratios = np.array(
                [float(r["w1_upper_ci_high"]) / float(r["alpha"]) for r in rows]
            )
            wrong_c = 1.10 * float(np.max(wrong_ratios[:3]))
            wrong_holdout_pass = bool(np.all(wrong_ratios[3:] <= wrong_c))
            negative_control_failures += int(not wrong_holdout_pass)
            family_diag = {
                "calibration_constant": calibrator,
                "holdout_pass": holdout_pass,
                "loglog_slope": slope,
                "wrong_O_alpha_control_pass": wrong_holdout_pass,
            }
            diagnostics["models"][f"{noise}:{model}"] = family_diag
            all_pass = all_pass and holdout_pass and (0.15 <= slope <= 1.10)

    tail_pass = True
    for noise in ("iid", "markov"):
        rows = [r for r in tail_rows if r["noise"] == noise]
        coarse = [float(r["normalized_upper"]) for r in rows if float(r["alpha"]) >= 0.02]
        fine = [float(r["normalized_upper"]) for r in rows if float(r["alpha"]) < 0.02]
        calibrator = 1.50 * max(coarse)
        this_pass = max(fine) <= calibrator
        diagnostics[f"{noise}_tail"] = {
            "calibration_constant": calibrator,
            "max_holdout_normalized_upper": max(fine),
            "holdout_pass": this_pass,
        }
        tail_pass = tail_pass and this_pass

    diagnostics["gaussian_contract_pass"] = bool(all_pass)
    diagnostics["tail_contract_pass"] = bool(tail_pass)
    diagnostics["negative_controls_failed_as_intended"] = negative_control_failures
    diagnostics["negative_control_pass"] = negative_control_failures >= 4
    return metric_rows, tail_rows, diagnostics


def gibbs_quantiles(n: int, h: int, *, literal_paper: bool = False) -> np.ndarray:
    q = (np.arange(n, dtype=float) + 0.5) / n
    if literal_paper:
        coefficient = 2.0 * math.factorial(h - 1) / h
    else:
        # Intended generator and Appendix E density for f(x)=x^h/h.
        coefficient = 2.0 / h
    p_abs = np.abs(2.0 * q - 1.0)
    magnitude = (gammaincinv(1.0 / h, p_abs) / coefficient) ** (1.0 / h)
    return np.where(q < 0.5, -magnitude, magnitude)


def simulate_scaled_gibbs(alpha: float, h: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    y = np.zeros(GIBBS_CHAINS_PER_SEED)
    delta = alpha ** (2.0 - 2.0 / h)
    burn = int(math.ceil(9.0 / delta))
    gap = int(math.ceil(0.75 / delta))
    high = math.sqrt((1.0 - SKEW_PROB) / SKEW_PROB)
    low = -math.sqrt(SKEW_PROB / (1.0 - SKEW_PROB))

    def step() -> None:
        xi = np.where(rng.random(len(y)) < SKEW_PROB, high, low)
        y[:] = y - delta * y ** (h - 1) + math.sqrt(delta) * xi
        if not np.all(np.isfinite(y)):
            raise RuntimeError(f"non-finite Gibbs chain for alpha={alpha}, h={h}")

    for _ in range(burn):
        step()
    out: list[np.ndarray] = []
    for _ in range(GIBBS_BATCHES):
        for _ in range(gap):
            step()
        out.append(y.copy())
    return np.concatenate(out)


def run_gibbs_campaign() -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    diagnostics: dict[str, object] = {"orders": {}}
    all_pass = True
    literal_rejected = True
    for h in (4, 6):
        for alpha in GIBBS_ALPHAS:
            per_seed: list[dict[str, float]] = []
            for seed in SEEDS:
                sample = simulate_scaled_gibbs(float(alpha), h, seed + h * 10_000)
                q_intended = gibbs_quantiles(len(sample), h, literal_paper=False)
                q_literal = gibbs_quantiles(len(sample), h, literal_paper=True)
                ordered = np.sort(sample)
                per_seed.append(
                    {
                        "w1_intended": float(np.mean(np.abs(ordered - q_intended))),
                        "w1_literal": float(np.mean(np.abs(ordered - q_literal))),
                        "scaled_sd": float(np.std(sample, ddof=1)),
                        "unscaled_sd": float(alpha ** (1.0 / h) * np.std(sample, ddof=1)),
                        "wrong_sqrt_scaled_sd": float(
                            alpha ** (1.0 / h - 0.5) * np.std(sample, ddof=1)
                        ),
                    }
                )
            row: dict[str, object] = {
                "claim": 6,
                "h": h,
                "alpha": float(alpha),
                "independent_seeds": len(SEEDS),
                "samples_per_seed": GIBBS_CHAINS_PER_SEED * GIBBS_BATCHES,
                "theorem_rate": float(alpha ** (1.0 / h)),
            }
            for key in per_seed[0]:
                mean, low, high = aggregate_mean_ci([r[key] for r in per_seed])
                row[key] = mean
                row[f"{key}_ci_low"] = low
                row[f"{key}_ci_high"] = high
            row["normalized_intended_upper"] = float(row["w1_intended_ci_high"]) / float(row["theorem_rate"])
            rows.append(row)

        h_rows = [r for r in rows if int(r["h"]) == h]
        h_rows.sort(key=lambda r: float(r["alpha"]), reverse=True)
        ratio = np.array([float(r["normalized_intended_upper"]) for r in h_rows])
        calibrator = 1.50 * float(np.max(ratio[:2]))
        holdout_pass = bool(np.all(ratio[2:] <= calibrator))
        unscaled = np.array([float(r["unscaled_sd"]) for r in h_rows])
        scaling_slope = fit_slope(
            np.array([float(r["alpha"]) for r in h_rows]), unscaled
        )
        scaled = np.array([float(r["scaled_sd"]) for r in h_rows])
        scaled_cv = float(np.std(scaled) / np.mean(scaled))
        literal_ratio = np.array(
            [float(r["w1_literal"]) / max(float(r["w1_intended"]), 1e-12) for r in h_rows]
        )
        this_literal_rejected = bool(np.min(literal_ratio[-2:]) > 2.0)
        literal_rejected = literal_rejected and this_literal_rejected
        diagnostics["orders"][str(h)] = {
            "expected_scaling_slope": 1.0 / h,
            "observed_scaling_slope": scaling_slope,
            "correct_scaled_sd_cv": scaled_cv,
            "heldout_rate_pass": holdout_pass,
            "literal_vs_intended_w1_ratio_min_fine": float(np.min(literal_ratio[-2:])),
            "literal_density_rejected": this_literal_rejected,
        }
        all_pass = (
            all_pass
            and holdout_pass
            and abs(scaling_slope - 1.0 / h) <= 0.12
            and scaled_cv <= 0.18
        )
    diagnostics["intended_conditional_rate_pass"] = bool(all_pass)
    diagnostics["literal_main_text_density_rejected"] = bool(literal_rejected)
    diagnostics["source_consistency_status"] = (
        "BLOCKED: Proposition 5.1 is conditional on conjectures and its displayed "
        "density conflicts with Conjecture 5.2 and Appendix E."
    )
    return rows, diagnostics


def independent_linear_checker() -> dict[str, object]:
    """Independent exact-covariance checker using Gaussian innovations.

    For diagonal linear SA with Gaussian noise, the finite-alpha stationary law
    is exactly Gaussian with variance 1/(2*lambda-alpha*lambda^2).  This checks
    the limiting covariance, finite-alpha direction, and rate logic without the
    nonlinear simulator or empirical stationary burn-in.
    """
    alpha = ALPHAS
    worst_w2 = []
    for a in alpha:
        finite_var = 1.0 / (2.0 * LINEAR_RATE - a * LINEAR_RATE**2)
        limit_var = 1.0 / (2.0 * LINEAR_RATE)
        # W2 between centered diagonal Gaussians; W1 <= W2.
        w2 = float(np.linalg.norm(np.sqrt(finite_var) - np.sqrt(limit_var)))
        worst_w2.append(w2)
    ratios = np.asarray(worst_w2) / (np.sqrt(alpha) * np.log(1.0 / alpha))
    slope = fit_slope(alpha, np.asarray(worst_w2))
    passed = bool(np.all(np.diff(ratios) <= 0.05) and slope > 0.75)
    return {
        "method": "closed-form Gaussian stationary covariance; W1 bounded by exact W2",
        "alphas": alpha.tolist(),
        "w2_upper_bounds": worst_w2,
        "normalized_by_paper_rate": ratios.tolist(),
        "loglog_slope": slope,
        "passed": passed,
    }


def csv_text(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def emit_artifact(path: str, text: str) -> None:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(f"ARTIFACT_BEGIN {path} sha256={digest}")
    print(text.rstrip())
    print(f"ARTIFACT_END {path}")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_claim_artifacts(
    gaussian_rows: list[dict[str, object]],
    tail_rows: list[dict[str, object]],
    gibbs_rows: list[dict[str, object]],
    diagnostics: dict[str, object],
    result: dict[str, dict[str, object]],
    resource_info: dict[str, object],
) -> None:
    filters = {
        1: lambda row: True,
        2: lambda row: row.get("noise") == "iid" and row.get("model") == "sgd",
        3: lambda row: row.get("noise") == "iid" and row.get("model") in {"linear", "contractive"},
        5: lambda row: row.get("noise") == "markov",
    }
    for claim, predicate in filters.items():
        selected = [row for row in gaussian_rows if predicate(row)]
        write_text(ARTIFACT_ROOT / f"claim_{claim}" / "raw_metrics.csv", csv_text(selected))
    write_text(
        ARTIFACT_ROOT / "claim_4" / "raw_metrics.csv",
        csv_text([row for row in tail_rows if row["noise"] == "iid"]),
    )
    write_text(ARTIFACT_ROOT / "claim_5" / "raw_tail_metrics.csv", csv_text(
        [row for row in tail_rows if row["noise"] == "markov"]
    ))
    write_text(ARTIFACT_ROOT / "claim_6" / "raw_metrics.csv", csv_text(gibbs_rows))
    for claim in range(1, 7):
        claim_dir = ARTIFACT_ROOT / f"claim_{claim}"
        write_text(
            claim_dir / "verdict.json",
            json.dumps(result[f"claim_{claim}"], indent=2, sort_keys=True) + "\n",
        )
        write_text(
            claim_dir / "runtime.json",
            json.dumps(resource_info, indent=2, sort_keys=True) + "\n",
        )
        write_text(
            claim_dir / "independent_checker_output.json",
            json.dumps(diagnostics["independent_checker"], indent=2, sort_keys=True) + "\n",
        )
        write_text(
            claim_dir / "negative_control_output.json",
            json.dumps(diagnostics["negative_controls"], indent=2, sort_keys=True) + "\n",
        )
        status = result[f"claim_{claim}"]["verdict"]
        write_text(
            claim_dir / "EVAL.md",
            "\n".join(
                [
                    f"# Claim {claim} evaluation",
                    "",
                    f"- Verdict: **{status}**",
                    f"- Scope: {result[f'claim_{claim}']['scope']}",
                    f"- Git SHA: `{git_sha()}`",
                    "- Fixed command: `uv run python repro/src/verify_sgd.py`",
                    f"- Deterministic seeds: `{list(SEEDS)}`",
                    f"- Wall time: `{resource_info['wall_seconds']:.3f}` seconds",
                    "",
                    "See `raw_metrics.csv`, `independent_checker_output.json`, and "
                    "`negative_control_output.json`. Source conditions and deviations "
                    "are recorded in `source_audit.md` and `limitations.md`.",
                    "",
                ]
            ),
        )


def verdicts(
    gaussian: dict[str, object],
    gibbs: dict[str, object],
    independent: dict[str, object],
) -> dict[str, dict[str, object]]:
    model_diag = gaussian["models"]
    iid_all = all(bool(model_diag[f"iid:{m}"]["holdout_pass"]) for m in FAMILIES)
    markov_all = all(bool(model_diag[f"markov:{m}"]["holdout_pass"]) for m in FAMILIES)
    return {
        "claim_1": {
            "verdict": "VERIFIED"
            if iid_all
            and markov_all
            and gaussian["gaussian_contract_pass"]
            and independent["passed"]
            else "BLOCKED",
            "scope": "faithful d=8 assumption-satisfying instantiations of Theorems 3.1 and 4.1",
        },
        "claim_2": {
            "verdict": "VERIFIED"
            if model_diag["iid:sgd"]["holdout_pass"]
            and 0.15 <= model_diag["iid:sgd"]["loglog_slope"] <= 1.10
            else "BLOCKED",
            "scope": "d=8 smooth strongly convex nonquadratic SGD with bounded skew noise",
        },
        "claim_3": {
            "verdict": "VERIFIED"
            if model_diag["iid:linear"]["holdout_pass"]
            and model_diag["iid:contractive"]["holdout_pass"]
            and 0.15 <= model_diag["iid:linear"]["loglog_slope"] <= 1.10
            and 0.15 <= model_diag["iid:contractive"]["loglog_slope"] <= 1.10
            else "BLOCKED",
            "scope": "d=8 Hurwitz linear and globally contractive tanh SA",
        },
        "claim_4": {
            "verdict": "VERIFIED" if gaussian["tail_contract_pass"] else "BLOCKED",
            "scope": "four directions, four thresholds, five stepsizes with held-out envelope checks",
        },
        "claim_5": {
            "verdict": "VERIFIED" if markov_all else "BLOCKED",
            "scope": "bounded product finite-state uniformly ergodic Markov chain; all three models",
        },
        "claim_6": {
            "verdict": "BLOCKED",
            "scope": "intended h=4/h=6 rate tested, but exact proposition is conjectural and source-inconsistent",
            "intended_conditional_rate_pass": gibbs["intended_conditional_rate_pass"],
        },
    }


def main() -> None:
    started = time.perf_counter()
    print("CAMPAIGN arXiv:2602.13960 faithful-separable-v1")
    print(f"GIT_SHA {git_sha()}")
    print(f"FIXED_COMMAND uv run python repro/src/verify_sgd.py")
    print(f"PYTHON {sys.version.split()[0]} NUMPY {np.__version__}")
    print(f"CPU {platform.machine()} logical={os.cpu_count()} platform={platform.platform()}")
    print(
        "CONFIG "
        + json.dumps(
            {
                "dimension": DIMENSION,
                "alphas": ALPHAS.tolist(),
                "gibbs_alphas": GIBBS_ALPHAS.tolist(),
                "seeds": list(SEEDS),
                "gaussian_chains_per_seed": GAUSSIAN_CHAINS_PER_SEED,
                "gaussian_batches": GAUSSIAN_BATCHES,
                "gibbs_chains_per_seed": GIBBS_CHAINS_PER_SEED,
                "gibbs_batches": GIBBS_BATCHES,
                "markov_rho": MARKOV_RHO,
                "noise": "centered variance-one bounded skew two-point",
            },
            sort_keys=True,
        )
    )

    gaussian_rows, tail_rows, gaussian_diag = run_gaussian_campaign()
    gibbs_rows, gibbs_diag = run_gibbs_campaign()
    independent = independent_linear_checker()
    result = verdicts(gaussian_diag, gibbs_diag, independent)
    runtime = time.perf_counter() - started
    resource_info = {
        "wall_seconds": runtime,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    combined_diagnostics = {
        "gaussian": gaussian_diag,
        "gibbs": gibbs_diag,
        "independent_checker": independent,
        "negative_controls": {
            "wrong_O_alpha_envelope": gaussian_diag["negative_control_pass"],
            "literal_prop_5_1_density": gibbs_diag["literal_main_text_density_rejected"],
        },
    }
    write_claim_artifacts(
        gaussian_rows,
        tail_rows,
        gibbs_rows,
        combined_diagnostics,
        result,
        resource_info,
    )
    for claim in range(1, 7):
        checker = subprocess.run(
            [
                sys.executable,
                str(ROOT / "repro" / "src" / "verify_claim_artifacts.py"),
                "--claim",
                str(claim),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        print(checker.stdout.rstrip())
        if checker.returncode != 0:
            print(checker.stderr.rstrip())
            raise SystemExit(f"claim artifact checker failed for claim {claim}")

    emit_artifact("raw/gaussian_w1.csv", csv_text(gaussian_rows))
    emit_artifact("raw/tail_gaps.csv", csv_text(tail_rows))
    emit_artifact("raw/gibbs.csv", csv_text(gibbs_rows))
    emit_artifact(
        "checks/diagnostics.json",
        json.dumps(combined_diagnostics, indent=2, sort_keys=True),
    )
    emit_artifact("runtime.json", json.dumps(resource_info, indent=2, sort_keys=True))
    emit_artifact("verdicts.json", json.dumps(result, indent=2, sort_keys=True))

    print("EVAL_SUMMARY")
    for claim, record in result.items():
        print(f"{claim.upper()} {record['verdict']} — {record['scope']}")
    print(f"RUNTIME_SECONDS {runtime:.3f}")
    failed = [claim for claim, record in result.items() if record["verdict"] not in {"VERIFIED", "FALSIFIED", "BLOCKED"}]
    if failed:
        raise SystemExit(f"invalid verdict state: {failed}")
    # Claim 6 is honestly BLOCKED by source conditions; that is a valid completed
    # verifier outcome. Numerical contract failures for Claims 1-5 are not.
    blocked_numeric = [
        claim for claim in ("claim_1", "claim_2", "claim_3", "claim_4", "claim_5")
        if result[claim]["verdict"] == "BLOCKED"
    ]
    if blocked_numeric:
        raise SystemExit(f"numeric claim contracts failed: {blocked_numeric}")
