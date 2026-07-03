# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The task requires that when `threshold=high` is passed, the response should return severity counts for **critical and high only**, omitting medium and low.

### Code Inspection

In `modules/fundamental/src/advisory/endpoints/get.rs`, the filtering logic is:

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

### Why This Fails

The comparison direction is inverted. The code checks `threshold_idx <= field_index` when it should check `field_index <= threshold_idx`. For `threshold=high` (index 1 in the severity_order array):

| Field | Index | Condition | Result | Expected |
|-------|-------|-----------|--------|----------|
| critical | 0 | always included | included | included |
| high | 1 | `1 <= 1` = true | included | included |
| medium | 2 | `1 <= 2` = true | **included** | **excluded** |
| low | 3 | `1 <= 3` = true | **included** | **excluded** |

Medium and low are incorrectly included because the condition `threshold_idx <= field_constant` is satisfied for all fields when threshold_idx is small. The correct logic would be `field_index <= threshold_idx` (i.e., include the field only if its severity rank is at or above the threshold rank).

### Additional Issue: Incorrect Total Computation

Even if the per-field filtering were correct, the `total` field is computed from the unfiltered summary values (`summary.critical + summary.high + summary.medium + summary.low`), not from the filtered values. When filtering is active, the total should reflect only the included counts.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-55 of the diff
- **Bug:** Comparison `threshold_idx <= N` should be `N <= threshold_idx` (or equivalently, each field's severity index should be compared against the threshold index)
- **Impact:** The threshold parameter has no practical filtering effect -- all severity counts are always returned regardless of the threshold value
