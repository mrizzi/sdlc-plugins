## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

### Reasoning

The filtering logic in `get.rs` does filter individual severity counts correctly when a valid threshold is provided. When `threshold=high`, `threshold_idx` is 1 (the position of "high" in the `severity_order` array), so:

- `critical`: always included (no condition)
- `high`: included because `threshold_idx <= 1` is true (1 <= 1)
- `medium`: zeroed because `threshold_idx <= 2` is false (1 <= 2 is true -- wait, this is actually true)

Re-examining more carefully:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold=high`, `threshold_idx = 1`.

- `critical`: always included (no condition on critical)
- `high`: `if threshold_idx <= 1` => `1 <= 1` => true => included
- `medium`: `if threshold_idx <= 2` => `1 <= 2` => true => included
- `low`: `if threshold_idx <= 3` => `1 <= 3` => true => included

This means `threshold=high` actually returns ALL counts, not just critical and high. The filtering logic is inverted -- the conditions should be checking whether each severity's index is within the threshold range, but the comparison is backwards. The code includes a severity when the threshold index is less than or equal to the severity's position, which is the opposite of what's needed.

For `threshold=high` to return only critical and high, the condition should exclude medium (index 2) and low (index 3). The correct logic would be: include severity at index `i` when `i <= threshold_idx`. But the code checks `threshold_idx <= i`, which includes everything at or after the threshold position.

Additionally, the `total` field is computed from the unfiltered counts:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This sums all original counts regardless of filtering, so `total` will not reflect the filtered result.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The filtering conditions (`threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3`) are inverted -- they include severities below the threshold instead of excluding them
- The `total` field uses unfiltered values from `summary.*` instead of the filtered values
- For `threshold=high` (idx=1): medium passes `1 <= 2` and low passes `1 <= 3`, so all four severities are returned instead of just critical and high
