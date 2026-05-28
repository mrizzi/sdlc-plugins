#!/usr/bin/env python3
"""Compute SHA-256 digest of ADF JSON for the description-digest protocol."""

import hashlib
import json
import sys


def compute_digest(raw: str) -> str:
    """Parse JSON input, re-serialize with compact separators, and return the SHA-256 hex digest."""
    parsed = json.loads(raw)
    normalized = json.dumps(parsed, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def main() -> int:
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                raw = f.read()
        else:
            raw = sys.stdin.read()

        if not raw.strip():
            print("error: empty input", file=sys.stderr)
            return 1

        print(compute_digest(raw))
        return 0

    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print(f"error: file not found: {sys.argv[1]}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
