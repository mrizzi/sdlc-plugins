## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Result: FAIL**

### Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses an inverted comparison that causes incorrect filtering. The code constructs the filtered response as follows:

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

For `threshold=high`, `threshold_idx` resolves to `1`. Tracing each condition:

| Severity | Condition | Evaluation | Included? | Expected |
|----------|-----------|------------|-----------|----------|
| critical | always | -- | yes | yes |
| high | `1 <= 1` | true | yes | yes |
| medium | `1 <= 2` | true | yes | **no** |
| low | `1 <= 3` | true | yes | **no** |

The comparison direction is inverted. The code checks `threshold_idx <= severity_position` but should check `severity_position <= threshold_idx` (include if the severity's rank position is at or above the threshold position). With the current logic, `threshold=high` includes all four severity levels instead of only critical and high.

Additionally, the `total` field is computed from unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered counts, so even if the per-severity filtering were correct, the total would be wrong.

### Evidence

The inverted comparison `threshold_idx <= N` (lines 43-51 of the diff in `get.rs`) means for any threshold_idx value, all severities at positions >= threshold_idx are included -- the exact opposite of the intended behavior. Only `threshold=low` (idx=3) would correctly exclude any severities (by coincidence), but even then it would produce the wrong set.
