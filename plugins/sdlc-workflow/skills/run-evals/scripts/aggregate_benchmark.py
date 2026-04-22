#!/usr/bin/env python3
"""Aggregate eval grading and timing results into benchmark.json."""

import argparse
import json
import statistics
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate eval results into benchmark.json"
    )
    parser.add_argument(
        "--results", type=Path, required=True, help="Workspace with eval results"
    )
    args = parser.parse_args()

    if not args.results.exists():
        print(f"Results directory not found: {args.results}", file=sys.stderr)
        sys.exit(1)

    pass_rates = []
    time_seconds = []
    tokens = []

    for eval_dir in sorted(args.results.glob("eval-*")):
        grading_path = eval_dir / "grading.json"
        if not grading_path.exists():
            continue

        grading = json.loads(grading_path.read_text())
        rate = grading.get("summary", {}).get("pass_rate")
        if rate is not None:
            pass_rates.append(rate)

        timing_path = eval_dir / "timing.json"
        if timing_path.exists():
            timing = json.loads(timing_path.read_text())
            duration_ms = timing.get("duration_ms")
            if duration_ms is not None:
                time_seconds.append(duration_ms / 1000)
            total_tokens = timing.get("total_tokens")
            if total_tokens is not None:
                tokens.append(total_tokens)

    benchmark = {
        "run_summary": {
            "pass_rate": _stats(pass_rates),
            "time_seconds": _stats(time_seconds),
            "tokens": _stats(tokens),
        }
    }

    output_path = args.results / "benchmark.json"
    output_path.write_text(json.dumps(benchmark, indent=2) + "\n")
    print(f"Written: {output_path}")


def _stats(values: list[float]) -> dict:
    if not values:
        return {"mean": 0.0, "stddev": 0.0}
    mean = statistics.mean(values)
    stddev = statistics.pstdev(values) if len(values) > 1 else 0.0
    return {"mean": round(mean, 2), "stddev": round(stddev, 2)}


if __name__ == "__main__":
    main()
