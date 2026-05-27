## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

### Analysis

The filtering logic in `get.rs` (lines 41-56 of the diff) uses inverted comparisons to decide which severity counts to include. When `threshold=high`, `threshold_idx` resolves to `1` (the index of "high" in `["critical", "high", "medium", "low"]`).

The code checks `threshold_idx <= N` where N is a hardcoded positional value for each severity:

- `critical`: always included (correct)
- `high`: `if threshold_idx <= 1` => `if 1 <= 1` => **true** => included (correct)
- `medium`: `if threshold_idx <= 2` => `if 1 <= 2` => **true** => included (WRONG -- medium should be excluded when threshold=high)
- `low`: `if threshold_idx <= 3` => `if 1 <= 3` => **true** => included (WRONG -- low should be excluded when threshold=high)

The comparison is backwards. The code should check whether each severity's position is `<= threshold_idx` (i.e., is the severity at or above the threshold), but instead it checks whether `threshold_idx <= severity_position`. This means for `threshold=high`, all four severity counts are returned, not just critical and high.

The correct condition would be the reverse: include the severity only if its index is <= threshold_idx (e.g., `severity_position <= threshold_idx`). In practice, critical (0) and high (1) both have positions <= 1, while medium (2) and low (3) do not.

Additionally, the `total` field is computed from unfiltered values:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This sums all four original counts regardless of filtering, so even if the per-severity filtering were correct, the total would still be wrong.

### Evidence

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

The comparisons `threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3` are inverted. They should be `1 <= threshold_idx`, `2 <= threshold_idx`, `3 <= threshold_idx` (or equivalently `threshold_idx >= severity_position`).
