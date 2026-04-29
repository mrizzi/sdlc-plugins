# Criterion 1: Threshold filtering returns only severities at or above threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` does implement threshold filtering logic. The code adds a `SummaryParams` struct with an optional `threshold` field and applies filtering in the `advisory_summary` handler.

The filtering logic uses a `severity_order` array `["critical", "high", "medium", "low"]` and determines a `threshold_idx` based on the position of the threshold value. For `threshold=high`, `threshold_idx` would be 1, and the filtering logic is:

```rust
critical: summary.critical,           // always included
high: if threshold_idx <= 1 { ... },  // included when idx <= 1 (true for high at idx 1)
medium: if threshold_idx <= 2 { ... }, // included when idx <= 2 (false for high at idx 1... wait, 1 <= 2 is true)
low: if threshold_idx <= 3 { ... },   // included when idx <= 3 (1 <= 3 is true)
```

**Wait -- there is a logic error here.** For `threshold=high` (index 1), the conditions evaluate as:
- `critical`: always included (correct)
- `high`: `1 <= 1` = true, so included (correct)
- `medium`: `1 <= 2` = true, so included (INCORRECT -- medium should be excluded when threshold is high)
- `low`: `1 <= 3` = true, so included (INCORRECT -- low should be excluded when threshold is high)

The comparison logic is inverted. The condition should be checking that the severity's index is at or below the threshold index (meaning the severity is at or above the threshold level), but instead it checks if the threshold index is at or below the severity's index. This means `threshold=high` would include ALL severities (critical, high, medium, low), not just critical and high.

The correct logic should be `if severity_idx <= threshold_idx` (e.g., for high at index 1: critical at index 0 <= 1 is true, high at index 1 <= 1 is true, medium at index 2 <= 1 is false, low at index 3 <= 1 is false). But the code uses the threshold_idx on the left side of the comparison instead of the severity's own index.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of filtering, which is incorrect -- the total should reflect only the filtered counts.

**Conclusion:** The threshold filtering logic has a critical bug. For `threshold=high`, it would return all four severity counts instead of only critical and high. This criterion is NOT met.
