# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` contains an inverted comparison that causes incorrect filtering for all threshold values.

### Code Under Review

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

### Trace for threshold="high"

- `threshold_idx` = 1 (position of "high" in the array)
- `critical`: always included (hardcoded)
- `high`: condition is `1 <= 1` = true -> INCLUDED (correct)
- `medium`: condition is `1 <= 2` = true -> INCLUDED (WRONG -- should be excluded)
- `low`: condition is `1 <= 3` = true -> INCLUDED (WRONG -- should be excluded)

### Root Cause

The comparison operands are reversed. The code checks `threshold_idx <= severity_position` when it should check `severity_position <= threshold_idx`. The correct conditions would be:

- `high`: `1 <= threshold_idx` (include high if threshold is high or lower)
- `medium`: `2 <= threshold_idx` (include medium if threshold is medium or lower)
- `low`: `3 <= threshold_idx` (include low only if threshold is low)

With the inverted comparison, threshold="high" returns all four severity counts instead of only critical and high, directly violating this criterion.

### Additional Issue: Total Calculation

Even if the per-field filtering were correct, the `total` field is computed from the unfiltered `summary` values (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. The total would not reflect the filtered counts.
