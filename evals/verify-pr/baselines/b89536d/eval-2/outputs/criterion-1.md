## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

### Evidence

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` introduces threshold filtering logic. The `SummaryParams` struct accepts an optional `threshold` query parameter:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The handler processes the threshold in a `match` block:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
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
    }
    None => summary,
};
```

### Analysis

When `threshold=high`, `threshold_idx` resolves to `1` (the index of "high" in the array `["critical", "high", "medium", "low"]`). The filtering conditions are:

- `critical` is always included (unconditional).
- `high`: `threshold_idx <= 1` is `1 <= 1` = true -- included. Correct.
- `medium`: `threshold_idx <= 2` is `1 <= 2` = true -- included. **INCORRECT** -- medium should be excluded when threshold is "high".
- `low`: `threshold_idx <= 3` is `1 <= 3` = true -- included. **INCORRECT** -- low should be excluded when threshold is "high".

The comparison logic is inverted. The condition `threshold_idx <= N` checks whether the threshold's position is at or below severity N's position, which means nearly all severities pass the check. The correct condition should check the reverse: include a severity at position N only when `N <= threshold_idx` (the severity's rank is at or above the threshold).

With the current logic, only `threshold=critical` (index 0) produces correct filtering. For all other thresholds (`high`, `medium`, `low`), severities that should be excluded are incorrectly included.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, producing an incorrect total when filtering is active.

This criterion is not met.
