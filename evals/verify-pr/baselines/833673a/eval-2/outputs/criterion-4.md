# Criterion 4: Severity ordering is correct: critical > high > medium > low

## Verdict: FAIL

## Analysis

The severity ordering definition is correct, but its application in the filtering logic is broken, rendering it effectively non-functional.

**Ordering definition (correct):**
The `severity_order` array is defined as `["critical", "high", "medium", "low"]`, with index 0 being the highest severity (critical) and index 3 being the lowest (low). This correctly represents the ordering critical > high > medium > low.

**Ordering application (broken):**
The filtering logic uses the threshold index in comparisons that are inverted. The conditions check `threshold_idx <= N` (where N is the severity's position) instead of `N <= threshold_idx` (checking if the severity's rank is high enough to be included).

For the ordering to be correctly applied, a severity should be included when its position in the array is at or before (<=) the threshold position. For example, with `threshold=high` (idx=1):
- critical (idx 0): 0 <= 1 = true (include) -- correct
- high (idx 1): 1 <= 1 = true (include) -- correct
- medium (idx 2): 2 <= 1 = false (exclude) -- correct
- low (idx 3): 3 <= 1 = false (exclude) -- correct

But the actual code checks:
- high: `threshold_idx <= 1` => `1 <= 1` = true (correct by coincidence)
- medium: `threshold_idx <= 2` => `1 <= 2` = true (WRONG -- should exclude)
- low: `threshold_idx <= 3` => `1 <= 3` = true (WRONG -- should exclude)

The only case where the filter works correctly is `threshold=low` (idx=3), where all severities are correctly included. For any higher threshold, the filter fails to exclude lower severities.

While the ordering is correctly defined as a data structure, the criterion requires that the ordering be correctly applied in filtering, which it is not.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `severity_order` array correctly orders severities
- The filtering conditions invert the comparison, making the ordering ineffective
- Only `threshold=low` produces correct results (all included); `threshold=critical` also works (only critical, since high/medium/low conditions with idx=0 evaluate to 0<=1, 0<=2, 0<=3 = all true, which is wrong -- all are included instead of only critical)
- Actually for `threshold=critical` (idx=0): high `0 <= 1` = true (WRONG), medium `0 <= 2` = true (WRONG), low `0 <= 3` = true (WRONG). So even threshold=critical includes everything.
