# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. The implementation uses a `severity_order` array `["critical", "high", "medium", "low"]` and finds the threshold's index via `.position()`.

For `threshold=high`, `threshold_idx = 1`.

The filtering conditions are:

```rust
critical: summary.critical,                                      // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },        // 1 <= 1 = true -> included
medium: if threshold_idx <= 2 { summary.medium } else { 0 },    // 1 <= 2 = true -> included (BUG)
low: if threshold_idx <= 3 { summary.low } else { 0 },          // 1 <= 3 = true -> included (BUG)
```

The condition is inverted. The code checks `threshold_idx <= <severity_position>` but should check `<severity_position> <= threshold_idx`. With `threshold=high` (idx=1), the intent is to include only severities at index 0 (critical) and 1 (high). But because the comparison is backwards, severities at indices 2 (medium) and 3 (low) are also included.

The correct condition should be:
- `high: if 1 <= threshold_idx { summary.high } else { 0 }` (i.e., the severity's own position <= threshold position)
- `medium: if 2 <= threshold_idx { summary.medium } else { 0 }`
- `low: if 3 <= threshold_idx { summary.low } else { 0 }`

As implemented, `threshold=high` returns all four severity counts instead of only critical and high.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines in diff constructing the `AdvisorySummary` struct (lines 47-53 of the diff)
- The comparison `threshold_idx <= N` should be `N <= threshold_idx`

Additionally, the `total` field is computed from unfiltered values:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This uses the original `summary` counts rather than the filtered values, so even if the filtering conditions were fixed, the total would still be incorrect.
