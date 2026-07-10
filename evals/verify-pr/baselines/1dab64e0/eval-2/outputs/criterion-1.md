## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Verdict: FAIL

### Analysis

The diff adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. The implementation defines a `severity_order` array `["critical", "high", "medium", "low"]` and uses `.position()` to find the threshold index, then conditionally zeroes out severity counts.

However, the filtering condition is inverted. The code uses `threshold_idx <= N` where N is the hardcoded index for each severity level:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

For `threshold=high` (threshold_idx = 1):
- `high`: `1 <= 1` = true -- included (correct)
- `medium`: `1 <= 2` = true -- included (WRONG -- should be excluded)
- `low`: `1 <= 3` = true -- included (WRONG -- should be excluded)

The condition should be `N <= threshold_idx` (include a severity if its index is at or before the threshold position), not `threshold_idx <= N`. With the current logic, `?threshold=high` returns all four severity counts instead of only critical and high.

Additionally, the `total` field is computed from the unfiltered source values:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
Even if the filtering conditions were corrected, the total would still reflect all severities rather than only the filtered ones.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-56 of the diff
- The filtering condition `threshold_idx <= N` is the inverse of what is needed
- For threshold=high, medium and low counts are incorrectly included
- Total is always computed from unfiltered counts regardless of threshold
