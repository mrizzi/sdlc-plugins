# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR introduces threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. The relevant code is:

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

The severity ordering array is `["critical"(idx=0), "high"(idx=1), "medium"(idx=2), "low"(idx=3)]`. For `threshold=high`, `threshold_idx` resolves to 1.

### Filtering logic trace for `threshold=high` (idx=1):

| Severity | Condition | Evaluation | Result | Expected |
|----------|-----------|------------|--------|----------|
| critical | always included | -- | included | included |
| high | `1 <= 1` | true | included | included |
| medium | `1 <= 2` | true | **included** | **excluded (0)** |
| low | `1 <= 3` | true | **included** | **excluded (0)** |

The comparison operator is inverted. The conditions use `threshold_idx <= N` but should use `threshold_idx >= N` (or equivalently `N <= threshold_idx`). As written, `threshold=high` includes all four severity levels instead of only critical and high.

### Correct logic would be:

```rust
high: if threshold_idx >= 1 { summary.high } else { 0 },
medium: if threshold_idx >= 2 { summary.medium } else { 0 },
low: if threshold_idx >= 3 { summary.low } else { 0 },
```

With the corrected logic, `threshold=high` (idx=1):
- high: `1 >= 1` -> true -> included
- medium: `1 >= 2` -> false -> 0
- low: `1 >= 3` -> false -> 0

### Additional issue: `total` field

Even if the filtering conditions were correct, the `total` field is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`), not from the filtered values. The total should reflect only the included severities.

## Conclusion

This criterion is **not satisfied**. The filtering logic has an inverted comparison operator that causes `threshold=high` to include all severity counts rather than only critical and high. Additionally, the total field uses unfiltered values.
