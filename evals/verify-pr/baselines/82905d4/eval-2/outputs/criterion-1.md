# Criterion 1: Threshold filtering returns only severities at or above threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Result: FAIL**

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` introduces a `SummaryParams` struct with an optional `threshold` field and adds filtering logic in the `advisory_summary` handler. The filtering logic uses a `severity_order` array `["critical", "high", "medium", "low"]` and finds the threshold index using `.position()`.

The filtering logic appears partially correct for the `threshold=high` case:
- `threshold_idx` for "high" would be 1
- `critical` (always included) -- correct
- `high`: `if threshold_idx <= 1` evaluates to true (1 <= 1) -- correct, included
- `medium`: `if threshold_idx <= 2` evaluates to false (1 <= 2 is true) -- **incorrect**, medium would be included when it should not be

Wait, re-examining: for threshold=high, threshold_idx = 1:
- `high`: `if threshold_idx <= 1` -> `if 1 <= 1` -> true -- high IS included (correct)
- `medium`: `if threshold_idx <= 2` -> `if 1 <= 2` -> true -- medium IS included (**incorrect**, should be excluded)
- `low`: `if threshold_idx <= 3` -> `if 1 <= 3` -> true -- low IS included (**incorrect**, should be excluded)

The filtering logic is **inverted**. The condition should be checking whether the severity index is within the threshold range (at or above), not whether the threshold index is less than or equal to the severity position. For threshold=high (idx=1), only critical (idx=0) and high (idx=1) should be included. The correct condition would be to zero out severities whose index is **greater than** the threshold index.

The current code sets `medium` to 0 only if `threshold_idx > 2` and `low` to 0 only if `threshold_idx > 3`. Since the maximum index is 3, `low` is never filtered out, and `medium` is only filtered when `threshold_idx > 2` (i.e., threshold=low, idx=3).

Additionally, the `total` field is recomputed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of filtering, which means the total does not reflect the filtered result.

**Conclusion:** The filtering logic is incorrect -- for `threshold=high`, medium and low counts would still be included instead of being zeroed out. This criterion is **not satisfied**.
