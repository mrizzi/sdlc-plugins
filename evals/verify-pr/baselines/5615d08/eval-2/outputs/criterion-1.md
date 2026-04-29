# Criterion 1: Threshold filtering returns only critical and high counts

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

## Reasoning

The PR diff in `get.rs` introduces threshold filtering logic in the `advisory_summary` handler. When `params.threshold` is `Some(threshold)`, the code builds a `severity_order` array `["critical", "high", "medium", "low"]` and finds the threshold index using `position()`.

For `threshold=high`, the index would be `1`. The filtering logic is:
- `critical`: always included (`summary.critical`)
- `high`: included if `threshold_idx <= 1` (true for index 1) -- correct
- `medium`: included if `threshold_idx <= 2` (false for index 1, set to 0) -- correct
- `low`: included if `threshold_idx <= 3` (false for index 1, set to 0) -- correct

The filtering of individual severity counts appears correct for this specific case. However, there is a critical bug: the `total` field is computed as `summary.critical + summary.high + summary.medium + summary.low`, which sums the **unfiltered** counts from the original `summary`, not the filtered values. This means the `total` does not reflect the filtered result, making the response internally inconsistent.

When `threshold=high`, the response would show `medium: 0, low: 0` but `total` would still include the original medium and low counts. This is a correctness defect -- the total should sum only the counts that are returned (i.e., only critical and high).

Additionally, there is no `threshold_applied` boolean field in the response (see Criterion 5), which is a separate but related gap.

The basic filtering of individual severity fields works for the `threshold=high` case, but the incorrect `total` field makes the overall response incorrect. The criterion asks for counts "for critical and high only" -- a response with a `total` that includes medium and low counts does not satisfy this.

## Evidence

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `total` line uses `summary.critical + summary.high + summary.medium + summary.low` (unfiltered values) instead of summing the filtered values.
