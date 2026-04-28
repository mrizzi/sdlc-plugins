# Criterion 1: Threshold filtering returns only at-or-above severity counts

## Criterion

`GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only.

## Verdict: PASS (with caveat)

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` introduces threshold filtering logic in the `advisory_summary` handler. When a `threshold` query parameter is provided, the code:

1. Defines a severity ordering array: `["critical", "high", "medium", "low"]`
2. Finds the index of the provided threshold value in this array using `.position()`
3. Conditionally zeros out severity counts below the threshold index

For `threshold=high`, the position index would be `1`. The filtering logic is:
- `critical`: always included (index 0, always at or above any threshold)
- `high`: included when `threshold_idx <= 1` (true for index 1) -- correct
- `medium`: included when `threshold_idx <= 2` (false for index 1, zeroed) -- correct
- `low`: included when `threshold_idx <= 3` (false for index 1, zeroed) -- correct

The filtering logic correctly returns only critical and high counts when `threshold=high`.

**Caveat:** While the filtering itself works, the `total` field is incorrectly computed. It sums all four unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) instead of summing only the filtered counts. This means the `total` will not match the sum of the returned non-zero counts. This is a correctness bug but does not directly violate the wording of this specific criterion (which only specifies "returns counts for critical and high only").

## Evidence

From the diff (lines 41-54 of the modified file):
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
