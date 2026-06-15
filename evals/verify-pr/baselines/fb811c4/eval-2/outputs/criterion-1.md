# Criterion 1: Threshold Filtering

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

## Analysis

The threshold filtering logic in `get.rs` is incorrect. The code uses index-based comparison against the `severity_order` array `["critical", "high", "medium", "low"]`, but the comparison direction is inverted.

When `threshold=high`:
- `threshold_idx` = 1 (position of "high" in the array)
- `critical` is always included (correct)
- `high`: `threshold_idx <= 1` evaluates to `1 <= 1` = true, so high is included (correct)
- `medium`: `threshold_idx <= 2` evaluates to `1 <= 2` = true, so medium is INCLUDED (incorrect -- should be zeroed)
- `low`: `threshold_idx <= 3` evaluates to `1 <= 3` = true, so low is INCLUDED (incorrect -- should be zeroed)

The result is that `threshold=high` returns all four severity counts instead of only critical and high. The filter effectively does nothing for any threshold value except "critical" (idx=0), where medium (`0 <= 2` = true) and low (`0 <= 3` = true) are still incorrectly included.

Additionally, the `total` field is recomputed from unfiltered values:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This uses the original `summary` fields rather than the filtered values, so the total never reflects the threshold.

## Evidence

From the diff in `get.rs`:
```rust
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

The conditions need to be reversed. To zero out severities below the threshold, the comparison should check if the threshold index is low enough (i.e., the threshold is at or above that severity level). The correct logic would use `>=` comparisons from the threshold's perspective or reverse the inequality direction.
