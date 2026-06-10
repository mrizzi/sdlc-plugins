# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is fundamentally inverted. The code uses a `severity_order` array `["critical", "high", "medium", "low"]` where critical=0, high=1, medium=2, low=3, and then applies threshold filtering with the following conditions:

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

For `threshold=high` (threshold_idx=1):
- critical: always included (correct)
- high: `1 <= 1` = true, included (correct)
- medium: `1 <= 2` = true, included (INCORRECT -- should be excluded)
- low: `1 <= 3` = true, included (INCORRECT -- should be excluded)

The condition is backwards. It checks whether the threshold index is less than or equal to the severity's fixed position, when it should check whether the severity's position is less than or equal to the threshold index. The correct condition for including a severity at position `i` should be `i <= threshold_idx` (meaning the severity is at or above the threshold level), not `threshold_idx <= i`.

As a result, `threshold=high` returns counts for ALL four severities instead of only critical and high. The criterion is not satisfied.

### Additional evidence of the inversion

For `threshold=critical` (idx=0): high (0<=1=true), medium (0<=2=true), low (0<=3=true) -- all included, but only critical should be returned.

For `threshold=low` (idx=3): high (3<=1=false), medium (3<=2=false), low (3<=3=true) -- only critical and low returned, missing high and medium.

The filtering behavior is the exact opposite of what is specified.
