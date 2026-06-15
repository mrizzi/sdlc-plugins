# Criterion 1: Threshold filtering returns only severities at or above threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` introduces threshold filtering logic using a positional index into a severity order array:

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

The severity_order array assigns indices: critical=0, high=1, medium=2, low=3. For `threshold=high`, `threshold_idx = 1`.

Evaluating each condition for threshold=high (idx=1):
- `critical`: always included (correct)
- `high`: `threshold_idx <= 1` = `1 <= 1` = true => included (correct)
- `medium`: `threshold_idx <= 2` = `1 <= 2` = true => included (INCORRECT -- should be excluded)
- `low`: `threshold_idx <= 3` = `1 <= 3` = true => included (INCORRECT -- should be excluded)

The comparison direction is inverted. The condition `threshold_idx <= N` (where N is the hardcoded position of each severity) includes severities at or BELOW the threshold, not at or above it. The correct condition would be `N <= threshold_idx` (or equivalently, the severity's position must be at most threshold_idx to be included).

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so even if the filtering logic were corrected, the total would be wrong.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The filtering conditions are inverted, causing threshold=high to return all four severities instead of only critical and high.
- The total is computed from pre-filter values.
