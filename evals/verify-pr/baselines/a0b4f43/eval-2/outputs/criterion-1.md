# Criterion 1: Threshold filtering returns only counts at or above threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: PASS**

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` introduces threshold filtering logic in the `advisory_summary` handler. When a `threshold` query parameter is provided, the code:

1. Defines a severity ordering array: `["critical", "high", "medium", "low"]`
2. Finds the index of the provided threshold value in this array using `.position()`
3. Constructs a new `AdvisorySummary` that zeros out severity counts below the threshold index

For `threshold=high`:
- `threshold_idx` would be 1 (position of "high" in the array)
- `critical` is always included (index 0 <= any threshold_idx)
- `high` is included because `threshold_idx <= 1` evaluates to `1 <= 1` which is true
- `medium` is zeroed because `threshold_idx <= 2` evaluates to `1 <= 2` which is true -- wait, this means medium IS included

**Correction on re-analysis:** Actually, looking more carefully at the logic:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

For `threshold=high`, `threshold_idx = 1`:
- `critical`: always included -- correct
- `high`: `1 <= 1` is true, so included -- correct
- `medium`: `1 <= 2` is true, so medium IS included -- INCORRECT

This means the filtering logic is actually WRONG. With `threshold=high`, medium and low should be excluded, but the condition `threshold_idx <= 2` evaluates to true for threshold_idx=1, meaning medium is incorrectly included.

**Wait -- let me re-read the logic more carefully.** The condition structure is: include the severity if the threshold index is at or below a certain position. But this is inverted from what is needed. The intent is "include severities at or above the threshold," but the code checks `threshold_idx <= N` which INCLUDES more severities as the threshold gets more severe (lower index).

Actually, re-analyzing: if `threshold=critical` (index 0):
- high: `0 <= 1` = true (included) -- WRONG, should be excluded
- medium: `0 <= 2` = true (included) -- WRONG
- low: `0 <= 3` = true (included) -- WRONG

This means `threshold=critical` returns ALL counts, which is wrong. Only critical should be returned.

For `threshold=high` (index 1):
- high: `1 <= 1` = true (included) -- correct
- medium: `1 <= 2` = true (included) -- WRONG, should be excluded
- low: `1 <= 3` = true (included) -- WRONG

The filtering logic is inverted. The condition should be checking that the severity's index is at or below the threshold index (i.e., more severe), not the other way around. The correct logic would be something like `severity_idx <= threshold_idx`.

However, looking again at the severity order array: `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3 respectively, and the desired behavior of "include severities at or above threshold":
- For `threshold=high` (idx=1), should include critical (idx=0) and high (idx=1), i.e., indices <= 1

The condition for each severity should check if THAT severity's fixed index is <= threshold_idx. The code hardcodes fixed indices for each field:
- critical is always index 0 (always included) -- correct
- high check: should include if high's index (1) <= threshold_idx, i.e., `1 <= threshold_idx` -- but code checks `threshold_idx <= 1`
- medium check: should include if 2 <= threshold_idx, i.e., `2 <= threshold_idx` -- but code checks `threshold_idx <= 2`

The conditions are backwards. `threshold_idx <= 1` should be `1 <= threshold_idx` (or equivalently `threshold_idx >= 1`).

**Revised Verdict: FAIL** -- The filtering logic is inverted. The conditions are backwards, causing severities below the threshold to be incorrectly included.

**Note:** On further reflection, there is a secondary bug. Even if the logic were correct, the `total` field is recomputed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so it would not match the filtered subset.

However, despite the logic bug, the criterion asks whether the endpoint structure supports threshold filtering, and the code does attempt to implement it. The implementation is buggy but the feature is present in concept. Since verification must be strict (does the code actually satisfy the criterion as stated), the answer depends on correctness of the output.

**Final Verdict: FAIL** -- The filtering logic has inverted conditions, so `threshold=high` would actually return critical, high, medium, AND low counts rather than just critical and high.
