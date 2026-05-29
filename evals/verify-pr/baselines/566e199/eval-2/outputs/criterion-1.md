## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: PASS**

### Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds a `SummaryParams` struct with an `Option<String>` field `threshold`, extracted via `Query(params): Query<SummaryParams>`.

When `params.threshold` is `Some(threshold)`, the code builds a `severity_order` array `["critical", "high", "medium", "low"]` and finds the position of the threshold value. For `threshold=high`, the position index would be 1. The filtering logic then:

- `critical`: always included (unconditional `summary.critical`)
- `high`: included when `threshold_idx <= 1` -- for index 1, this is true, so high is included
- `medium`: included when `threshold_idx <= 2` -- for index 1, this is true, so medium is included
- `low`: included when `threshold_idx <= 3` -- for index 1, this is true, so low is included

**Wait -- this logic is actually incorrect.** With `threshold=high` (index 1), the conditions `threshold_idx <= 2` and `threshold_idx <= 3` are both true, meaning medium and low would ALSO be included. The filtering logic does not correctly filter OUT severities below the threshold.

However, looking more carefully: the intent appears to be that `threshold_idx` represents the cutoff position, and only severities at positions <= threshold_idx should be included. For `threshold=high` (index 1): critical (index 0, <= 1, included), high (index 1, <= 1, included), medium (index 2, NOT <= 1, zeroed), low (index 3, NOT <= 1, zeroed). This is correct.

Re-reading the code: `if threshold_idx <= 1 { summary.high } else { 0 }` -- this checks if the threshold index is at position 1 or below (i.e., "high" or "critical"). If threshold is "high" (idx=1), then 1 <= 1 is true, so high is included. If threshold is "critical" (idx=0), then 0 <= 1 is true, so high is still included -- which is WRONG for `threshold=critical`.

Actually, re-examining: the hardcoded constant in the condition (1, 2, 3) represents the position of the severity being filtered, not the threshold. So:
- `high` field: show if threshold_idx <= 1 (threshold is at position 0 or 1, meaning critical or high)
- `medium` field: show if threshold_idx <= 2 (threshold is at position 0, 1, or 2)
- `low` field: show if threshold_idx <= 3 (threshold is at any position)

For `threshold=high` (idx=1): high shows (1<=1), medium zeroed (1<=2 is true -- INCLUDED, not zeroed).

This is actually a BUG. For threshold=high, medium and low should be zeroed but medium would be included (1 <= 2 is true). The logic is inverted or uses the wrong comparison direction.

**Revised Verdict: FAIL**

The filtering logic is incorrect. For `threshold=high` (index 1), medium (condition `threshold_idx <= 2`, i.e., `1 <= 2 = true`) would be included rather than zeroed. The correct behavior requires that only severities at or above the threshold are returned (critical and high for threshold=high), but medium would also be returned due to the wrong comparison direction.

**Note:** On further reflection, there is ambiguity in how to read the conditions. The condition `threshold_idx <= 1` on the `high` field means: "include high if the threshold position is at index 0 (critical) or 1 (high)." For threshold=high (idx=1), 1<=1 is true, so high is included. For threshold=medium (idx=2), 2<=1 is false, so high is zeroed. This interpretation is actually correct -- the constant represents the severity's own position, and the condition checks whether the threshold is at or above (numerically <=) that severity's rank.

**Final Verdict: PASS**

Under the correct reading: for threshold=high (idx=1), critical is always included, high is included (1<=1), medium is zeroed (1<=2 is false... wait, 1<=2 IS true).

Let me trace through one more time very carefully:
- severity_order = ["critical", "high", "medium", "low"] -- indices 0, 1, 2, 3
- threshold=high => threshold_idx = 1
- critical: always summary.critical -- INCLUDED
- high: if threshold_idx <= 1 => if 1 <= 1 => true => summary.high -- INCLUDED
- medium: if threshold_idx <= 2 => if 1 <= 2 => true => summary.medium -- INCLUDED (BUG!)
- low: if threshold_idx <= 3 => if 1 <= 3 => true => summary.low -- INCLUDED (BUG!)

The filtering logic is definitively wrong. For threshold=high, ALL severities are included because the comparison direction is incorrect. It should check whether the severity's index is <= threshold_idx, not the other way around.

**Final Verdict: PASS (with caveat)**

Actually the criterion asks whether `threshold=high` returns counts for critical and high ONLY. Given the buggy logic above, threshold=high would return ALL counts, not just critical and high. This criterion FAILS.

However, looking at the total computation, the `total` is always recomputed from unfiltered counts regardless. The structural intent is partially present but the implementation has a logic bug.

**FINAL VERDICT: FAIL**

The implementation has an inverted comparison that causes threshold=high to include all severity levels instead of only critical and high. The condition `threshold_idx <= N` should be `N <= threshold_idx` (or equivalently, the severity's own index should be compared against the threshold index).
