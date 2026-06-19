## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` implements threshold filtering with the following logic:

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

For `threshold=high`, `threshold_idx` = 1 (position of "high" in the array). Tracing through:
- `critical`: always included (no condition) -- correct
- `high`: `threshold_idx(1) <= 1` is true -- includes `summary.high` -- correct
- `medium`: `threshold_idx(1) <= 2` is true -- includes `summary.medium` -- INCORRECT, should be 0
- `low`: `threshold_idx(1) <= 3` is true -- includes `summary.low` -- INCORRECT, should be 0

The condition logic is inverted. The code checks whether `threshold_idx <= severity_position`, but it should check whether `severity_position <= threshold_idx` to include only severities at or above the threshold.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered counts, which is incorrect regardless of the filtering logic.

## Verdict: FAIL

The filtering logic is inverted -- for `threshold=high`, medium and low counts are incorrectly included instead of being zeroed out. The total is also computed from unfiltered values.
