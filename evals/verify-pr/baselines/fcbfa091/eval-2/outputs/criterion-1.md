# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`, but the filtering conditions are **inverted**, causing incorrect results for `threshold=high`.

### Code Under Review

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

### Defect 1: Inverted filtering conditions

For `threshold=high`, the `threshold_idx` is `1` (the position of "high" in the array).

The conditions evaluate as follows:

| Field    | Condition           | Evaluates to | Included? | Expected |
|----------|---------------------|--------------|-----------|----------|
| critical | always              | true         | Yes       | Yes      |
| high     | `1 <= 1`            | true         | Yes       | Yes      |
| medium   | `1 <= 2`            | true         | Yes       | **No** -- should be excluded |
| low      | `1 <= 3`            | true         | Yes       | **No** -- should be excluded |

The correct condition should check whether each severity's index is at or above the threshold (i.e., `severity_index <= threshold_idx`), not whether `threshold_idx <= severity_constant`. The comparison operands are swapped.

For `threshold=high`, the expected result is counts for critical and high **only**, with medium and low set to zero. The implementation includes all four severity levels, violating this criterion.

### Defect 2: Total computed from unfiltered counts

Even if filtering were correct, the `total` field is computed as:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This sums the **unfiltered** `summary.*` values rather than the filtered values. After filtering, `total` should reflect only the included severity counts.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-55 of the diff
- The filtering branch always includes medium and low for any threshold value of "critical" or "high" because the conditions `threshold_idx <= 2` and `threshold_idx <= 3` are true for all threshold_idx values 0-3
- The total field uses `summary.*` (unfiltered) instead of the filtered values
