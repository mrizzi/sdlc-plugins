# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Result: FAIL

## Reasoning

The filtering logic in `get.rs` is incorrect. It uses the wrong comparison direction when deciding which severity levels to include.

The code defines the severity order as:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold=high`, `threshold_idx` resolves to `1`. The filtering conditions are:

- `critical`: always included (hardcoded, no condition)
- `high: if threshold_idx <= 1 { summary.high } else { 0 }` -- 1 <= 1 is true, so high is included
- `medium: if threshold_idx <= 2 { summary.medium } else { 0 }` -- 1 <= 2 is true, so medium is **included** (WRONG)
- `low: if threshold_idx <= 3 { summary.low } else { 0 }` -- 1 <= 3 is true, so low is **included** (WRONG)

The conditions check whether `threshold_idx <= <fixed index>` but they should check whether each severity's position is within the threshold. The correct logic would compare the severity's index against the threshold index (e.g., `if 2 <= threshold_idx` for medium, or equivalently, include severity only when its array index is <= threshold_idx).

As implemented, `threshold=high` returns all four severity counts instead of just critical and high. The filter effectively does nothing for any threshold except `threshold=low` (which would also include everything anyway since low is the lowest).

Additionally, the `total` field is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so even if the per-severity filtering were corrected, the total would still be wrong.
