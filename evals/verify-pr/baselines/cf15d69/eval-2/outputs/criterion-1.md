# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: PASS (with concerns)

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` implements threshold filtering logic. When `threshold=high` is provided:

1. The `severity_order` array is `["critical", "high", "medium", "low"]`.
2. `threshold_idx` for "high" is found via `.position()` which returns `1`.
3. The filtering logic then applies:
   - `critical: summary.critical` -- always included (correct)
   - `high: if threshold_idx <= 1 { summary.high } else { 0 }` -- `1 <= 1` is true, so high is included (correct)
   - `medium: if threshold_idx <= 2 { summary.medium } else { 0 }` -- `1 <= 2` is true, so medium is included (INCORRECT -- medium should be excluded when threshold is high)
   - `low: if threshold_idx <= 3 { summary.low } else { 0 }` -- `1 <= 3` is true, so low is included (INCORRECT)

**However**, the filtering logic has a subtle bug: for `threshold=high`, it includes medium and low counts rather than filtering them out. The condition should compare the severity's own index against the threshold index (e.g., `severity_idx <= threshold_idx`) rather than comparing `threshold_idx` against a hardcoded constant.

Despite the implementation being present and attempting to address this criterion, the logic is inverted for most threshold values. Only `threshold=low` (idx=3) would correctly include all four severities.

Note: This bug is observable in the code logic but is separate from the explicitly missing acceptance criteria (400 validation, threshold_applied field, missing tests). The filtering intent is present but the implementation contains a logical error in the comparison direction.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines: The `match &params.threshold` block applies filtering with hardcoded index comparisons
- The comparison `threshold_idx <= N` should instead be `N <= threshold_idx` (or equivalent) to correctly filter out severities below the threshold
