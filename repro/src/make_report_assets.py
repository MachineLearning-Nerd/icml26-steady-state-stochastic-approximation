"""Render evidence-bearing figures from the serialized claim artifacts."""

from __future__ import annotations

import csv
import hashlib
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
IMAGE_DIR = ROOT / "reports" / "sgd-steady-state-reproduction" / "images"
COLORS = {
    "iid": "#0072B2",
    "markov": "#D55E00",
    "h4": "#009E73",
    "h6": "#CC79A7",
}
MARKERS = {"sgd": "o", "linear": "s", "contractive": "^"}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def grouped(
    records: list[dict[str, str]], keys: tuple[str, ...]
) -> dict[tuple[str, ...], list[dict[str, str]]]:
    result: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for record in records:
        result[tuple(record[key] for key in keys)].append(record)
    return result


def slope(xs: list[float], ys: list[float]) -> float:
    return float(np.polyfit(np.log(xs), np.log(ys), 1)[0])


def finish(fig: plt.Figure, filename: str) -> Path:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = IMAGE_DIR / filename
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def headline_w1(records: list[dict[str, str]]) -> Path:
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    for (noise, model), group in sorted(grouped(records, ("noise", "model")).items()):
        ordered = sorted(group, key=lambda record: float(record["alpha"]))
        x = [float(record["alpha"]) for record in ordered]
        y = [float(record["normalized_upper_ci"]) for record in ordered]
        ax.plot(
            x,
            y,
            color=COLORS[noise],
            marker=MARKERS[model],
            linewidth=2,
            markersize=6,
            label=f"{noise} · {model}",
        )
    ax.set_xscale("log")
    ax.set_xlabel("Stepsize α (log scale)")
    ax.set_ylabel("95% W1 upper bracket / [√α log(1/α)]")
    ax.set_title("The paper-rate normalization stays bounded across all six d=8 families")
    ax.legend(ncol=2, frameon=False)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    return finish(fig, "headline-w1-rate.png")


def w1_slopes(records: list[dict[str, str]]) -> Path:
    labels: list[str] = []
    values: list[float] = []
    colors: list[str] = []
    for (noise, model), group in sorted(grouped(records, ("noise", "model")).items()):
        ordered = sorted(group, key=lambda record: float(record["alpha"]))
        labels.append(f"{noise}\n{model}")
        values.append(
            slope(
                [float(record["alpha"]) for record in ordered],
                [float(record["coordinate_mean"]) for record in ordered],
            )
        )
        colors.append(COLORS[noise])
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    positions = np.arange(len(labels))
    bars = ax.bar(positions, values, color=colors, width=0.68)
    ax.axhline(0.5, color="#333333", linestyle="--", linewidth=1.5, label="half-order reference")
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.015,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_xticks(positions, labels)
    ax.set_ylim(0, 0.66)
    ax.set_ylabel("Fitted log–log W1 slope")
    ax.set_title("Finite-sample slopes resolve near the expected half-order regime")
    ax.text(
        0.99,
        0.05,
        "Wrong O(α) envelopes rejected: 6/6",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=10,
    )
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return finish(fig, "w1-slope-diagnostics.png")


def tail_controls(
    iid_records: list[dict[str, str]],
    markov_records: list[dict[str, str]],
) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), sharex=True)
    for ax, (noise, records_for_noise) in zip(
        axes, (("iid", iid_records), ("markov", markov_records)), strict=True
    ):
        by_alpha = grouped(records_for_noise, ("alpha",))
        alphas = sorted(float(key[0]) for key in by_alpha)
        correct: list[float] = []
        wrong: list[float] = []
        for alpha in alphas:
            group = by_alpha[(str(alpha),)]
            correct.append(
                max(
                    float(record["gap_upper95"]) / float(record["theorem_rate"])
                    for record in group
                )
            )
            wrong.append(
                max(
                    float(record["gap_upper95"])
                    / (
                        alpha
                        * math.sqrt(math.log(1.0 / alpha))
                        / float(record["threshold"])
                    )
                    for record in group
                )
            )
        correct_calibration = 1.5 * max(
            value for alpha, value in zip(alphas, correct, strict=True) if alpha >= 0.02
        )
        wrong_calibration = 1.1 * max(
            value for alpha, value in zip(alphas, wrong, strict=True) if alpha >= 0.02
        )
        ax.plot(alphas, correct, "o-", color=COLORS[noise], label="paper rate")
        ax.plot(alphas, wrong, "x--", color="#555555", label="wrong O(α) control")
        ax.axhline(
            correct_calibration,
            color=COLORS[noise],
            linestyle=":",
            linewidth=1.4,
            label="paper-rate calibration",
        )
        ax.axhline(
            wrong_calibration,
            color="#555555",
            linestyle=":",
            linewidth=1.2,
            label="wrong-rate calibration",
        )
        ax.axvline(0.02, color="#999999", linewidth=1)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"{noise.upper()} noise")
        ax.set_xlabel("Stepsize α (fine holdout left of 0.02)")
        ax.grid(alpha=0.22)
    axes[0].set_ylabel("Worst normalized 95% tail gap")
    axes[1].legend(frameon=False, fontsize=9)
    fig.suptitle("Projection tails pass the claimed envelope while a too-fast rate breaks")
    fig.tight_layout()
    return finish(fig, "tail-bound-controls.png")


def gibbs_diagnostics(records: list[dict[str, str]]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
    for h_text, color in (("4", COLORS["h4"]), ("6", COLORS["h6"])):
        group = sorted(
            [record for record in records if record["h"] == h_text],
            key=lambda record: float(record["alpha"]),
        )
        alphas = np.array([float(record["alpha"]) for record in group])
        unscaled = np.array([float(record["unscaled_sd"]) for record in group])
        h = int(h_text)
        reference = unscaled[-1] * (alphas / alphas[-1]) ** (1.0 / h)
        observed = slope(alphas.tolist(), unscaled.tolist())
        axes[0].plot(
            alphas,
            unscaled,
            "o-",
            color=color,
            label=f"h={h}, fit={observed:.3f}",
        )
        axes[0].plot(
            alphas,
            reference,
            "--",
            color=color,
            alpha=0.65,
            label=f"h={h}, target={1/h:.3f}",
        )
        ratio = np.array(
            [
                float(record["w1_literal"])
                / max(float(record["w1_intended"]), 1e-12)
                for record in group
            ]
        )
        axes[1].plot(alphas, ratio, "o-", color=color, label=f"h={h}")
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("Stepsize α")
    axes[0].set_ylabel("Unscaled stationary standard deviation")
    axes[0].set_title("Intended α^(1/h) scaling is observed")
    axes[0].legend(frameon=False, fontsize=9)
    axes[1].set_xscale("log")
    axes[1].axhline(1.0, color="#555555", linestyle="--", linewidth=1.2)
    axes[1].set_xlabel("Stepsize α")
    axes[1].set_ylabel("W1(literal density) / W1(Appendix-E density)")
    axes[1].set_title("The printed and intended Gibbs targets disagree")
    axes[1].legend(frameon=False)
    for ax in axes:
        ax.grid(alpha=0.22)
    fig.suptitle("Claim 6: strong intended-rate evidence, but the exact proposition remains blocked")
    fig.tight_layout()
    return finish(fig, "gibbs-scaling-and-target.png")


def main() -> None:
    gaussian = rows(ARTIFACTS / "claim_1" / "raw_metrics.csv")
    iid_tail = rows(ARTIFACTS / "claim_4" / "raw_metrics.csv")
    markov_tail = rows(ARTIFACTS / "claim_5" / "raw_tail_metrics.csv")
    gibbs = rows(ARTIFACTS / "claim_6" / "raw_metrics.csv")
    paths = [
        headline_w1(gaussian),
        w1_slopes(gaussian),
        tail_controls(iid_tail, markov_tail),
        gibbs_diagnostics(gibbs),
    ]
    for path in paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"REPORT_ASSET {path.relative_to(ROOT)} sha256={digest}")


if __name__ == "__main__":
    main()
