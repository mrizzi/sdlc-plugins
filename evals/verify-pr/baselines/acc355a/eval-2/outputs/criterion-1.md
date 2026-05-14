## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Result: FAIL**

### Evidence

The diff in `get.rs` implements threshold filtering with the following logic:

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

When `threshold=high`, `threshold_idx` would be 1. The filtering of individual severity fields (critical, high included; medium, low zeroed out) appears correct for this case. However, the `total` field is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. This means the total will not match the sum of the returned severity counts, which is semantically incorrect and would confuse API consumers.

The total should be computed as:
```rust
total: filtered_critical + filtered_high + filtered_medium + filtered_low
```

Because the total is wrong, the response for `threshold=high` does not correctly represent "counts for critical and high only" -- the total includes medium and low counts that were supposedly filtered out. This criterion is considered **FAIL** due to the incorrect total calculation.
