# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

When `threshold=high` is provided, the code resolves `threshold_idx = 1` from the `severity_order` array `["critical", "high", "medium", "low"]`.

The filtering logic then applies these conditions:

- `critical: summary.critical` -- always included (correct)
- `high: if threshold_idx <= 1 { summary.high } else { 0 }` -- `1 <= 1` is TRUE, high is included (correct)
- `medium: if threshold_idx <= 2 { summary.medium } else { 0 }` -- `1 <= 2` is TRUE, medium is **included** (INCORRECT -- should be 0)
- `low: if threshold_idx <= 3 { summary.low } else { 0 }` -- `1 <= 3` is TRUE, low is **included** (INCORRECT -- should be 0)

The filtering logic is inverted. The condition `threshold_idx <= N` includes more severity levels as the threshold becomes more severe, which is the opposite of what is required. With `threshold=high`, medium and low counts are still included in the response instead of being zeroed out.

The correct condition should be `N <= threshold_idx` (include the severity level only if its position in the array is at or above the threshold position). For example, with `threshold=high` (idx=1): high (1 <= 1, included), medium (2 <= 1, excluded), low (3 <= 1, excluded).

Additionally, the `total` field is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered values. Even if the per-field filtering were corrected, the total would still include all four severity levels' original counts, making it inconsistent with the filtered fields.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines: threshold filtering block starting at the `Some(threshold)` match arm
- The condition `threshold_idx <= 2` for medium and `threshold_idx <= 3` for low always evaluates to true for any valid threshold, making filtering ineffective for those levels
- The `total` field uses `summary.critical + summary.high + summary.medium + summary.low` (unfiltered values)
