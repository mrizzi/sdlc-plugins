# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Result: FAIL

## What was checked

Verified whether the PR diff implements threshold filtering such that `?threshold=high` returns severity counts for only `critical` and `high`, omitting `medium` and `low`.

## Evidence from the diff

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` (lines 41-54 of the diff) implements the following:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

## Gap identified

The filtering logic is **inverted**. The code checks `threshold_idx <= N` (where N is the hardcoded index for each severity) when the correct logic would be `N <= threshold_idx` (i.e., include a severity only if its index is at or below the threshold index).

With `threshold=high` (threshold_idx = 1):
- `critical`: always included (correct)
- `high`: `1 <= 1` evaluates to `true` -- included (correct)
- `medium`: `1 <= 2` evaluates to `true` -- **incorrectly included** (should be 0)
- `low`: `1 <= 3` evaluates to `true` -- **incorrectly included** (should be 0)

The result is that `?threshold=high` returns all four severity counts instead of only critical and high.

Additionally, the `total` field is computed from the unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered counts, so even if the per-severity filtering were correct, the total would still be wrong.
