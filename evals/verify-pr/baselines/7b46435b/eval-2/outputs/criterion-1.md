# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The task requires that when `threshold=high` is provided, the response should include counts only for severities at or above "high" -- that is, `critical` and `high`, with `medium` and `low` omitted (set to 0).

The implementation defines the severity ordering array as:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

For `threshold=high`, `position()` returns index 1. The filtering logic then applies these conditions:

```rust
critical: summary.critical,                              // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },    // 1 <= 1 -> true -> INCLUDED
medium: if threshold_idx <= 2 { summary.medium } else { 0 }, // 1 <= 2 -> true -> INCLUDED (BUG)
low: if threshold_idx <= 3 { summary.low } else { 0 },       // 1 <= 3 -> true -> INCLUDED (BUG)
```

The condition `threshold_idx <= N` is inverted. It checks whether the threshold position is at or before each severity's hardcoded position, which is the wrong direction. The correct condition should be `N <= threshold_idx` (i.e., include a severity at position N only if N is at or before the threshold position).

**Tracing the logic for threshold=high (idx=1):**
- `high` (position 1): `1 <= 1` = true -- included (correct)
- `medium` (position 2): `1 <= 2` = true -- included (WRONG: should be excluded)
- `low` (position 3): `1 <= 3` = true -- included (WRONG: should be excluded)

The result is that `threshold=high` returns ALL severity counts instead of only critical and high. The filtering effectively does nothing for any threshold except `low`.

**Additional tracing for threshold=critical (idx=0):**
- `high` (position 1): `0 <= 1` = true -- included (WRONG: should be excluded)
- `medium` (position 2): `0 <= 2` = true -- included (WRONG)
- `low` (position 3): `0 <= 3` = true -- included (WRONG)

This confirms the condition is universally inverted. The threshold filter is broken for all severity levels except the trivial `threshold=low` case (which should return everything and happens to work by accident since all conditions are true).

Furthermore, the `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so even if the individual fields were correctly filtered, the total would be incorrect.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines: threshold filtering block (lines ~41-54 in the diff)
- The condition `threshold_idx <= N` should be `N <= threshold_idx`
- The `total` computation uses unfiltered values instead of filtered values
