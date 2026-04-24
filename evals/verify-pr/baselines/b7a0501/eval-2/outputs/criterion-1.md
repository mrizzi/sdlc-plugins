## Criterion 1: Threshold filtering returns only counts at or above threshold

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only.

**Result**: FAIL

**Reasoning**:

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` introduces a `SummaryParams` struct with an `Option<String>` threshold field and adds filtering logic in the `advisory_summary` handler. When a threshold is provided, the code looks up its index in the `severity_order` array `["critical", "high", "medium", "low"]` and conditionally zeroes out counts.

For `?threshold=high`, `threshold_idx` would be 1. The filtering logic then:
- `critical`: always included (correct)
- `high`: included when `threshold_idx <= 1` => 1 <= 1 => true (correct)
- `medium`: included when `threshold_idx <= 2` => 1 <= 2 => true (INCORRECT -- medium should be excluded for threshold=high)
- `low`: included when `threshold_idx <= 3` => 1 <= 3 => true (INCORRECT -- low should be excluded for threshold=high)

The filtering logic is inverted. The condition `threshold_idx <= N` will be true for all severities at or below the threshold, when it should only be true for severities at or above. For threshold=high (idx=1), only critical (idx=0) and high (idx=1) should be included, but the code includes medium and low as well.

Similarly, for threshold=critical (idx=0), all four severities are included (0 <= 1, 0 <= 2, 0 <= 3 are all true), when only critical should be included.

Additionally, the `total` field is computed from unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered counts, so even if the filtering were correct, the total would be wrong.

**Verdict**: FAIL -- The threshold filtering logic is inverted and does not correctly exclude severities below the threshold. The total is also computed from unfiltered counts.
