"""Fixed entrypoint for the cumulative arXiv:2602.13960 reproduction.

The OpenResearch run command is frozen as:
    uv run python repro/src/verify_sgd.py
Experiment branches vary this committed implementation, never the command.
"""

from research_campaign import main


if __name__ == "__main__":
    main()
