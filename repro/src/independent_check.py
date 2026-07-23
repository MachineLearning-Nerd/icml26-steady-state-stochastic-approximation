"""Independent checker entrypoint for the closed-form linear-SA route."""

import json

from research_campaign import independent_linear_checker


if __name__ == "__main__":
    result = independent_linear_checker()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
