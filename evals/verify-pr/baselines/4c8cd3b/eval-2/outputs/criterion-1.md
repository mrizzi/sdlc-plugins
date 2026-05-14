# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. When `threshold=high` is provided, the code attempts to filter by zeroing out severities below the threshold:

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

For `threshold=high`, `threshold_idx` would be 1, so:
- `critical` is always included (correct)
- `high` is included when `threshold_idx <= 1` (1 <= 1 is true, correct)
- `medium` is zeroed when `threshold_idx <= 2` (1 <= 2 is true, so medium is **included** -- this is **incorrect**)

Wait -- re-reading: the condition `if threshold_idx <= 2 { summary.medium } else { 0 }` means medium IS included when threshold_idx is 1 (high). This is wrong. For `threshold=high`, medium should be excluded (set to 0), but the condition `1 <= 2` evaluates to true, so medium is kept.

**Correction on re-analysis:** Actually, let me re-read the logic more carefully:

- `threshold_idx = 1` for "high"
- `high: if threshold_idx <= 1 { summary.high } else { 0 }` -- 1 <= 1 is true, high is kept. Correct.
- `medium: if threshold_idx <= 2 { summary.medium } else { 0 }` -- 1 <= 2 is true, medium is kept. **Incorrect** -- medium should be excluded for threshold=high.
- `low: if threshold_idx <= 3 { summary.low } else { 0 }` -- 1 <= 3 is true, low is kept. **Incorrect** -- low should be excluded for threshold=high.

The filtering logic is **inverted**. The conditions should be `threshold_idx >= N` rather than `threshold_idx <= N` to correctly filter out severities below the threshold. As written, `threshold=high` would return ALL severities (critical, high, medium, low), not just critical and high.

Additionally, the `total` field is computed from the **unfiltered** counts: `summary.critical + summary.high + summary.medium + summary.low`. Even if the filtering conditions were corrected, the total would still be wrong because it should sum only the filtered (non-zero) counts.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-55 in the diff
- The filtering condition logic is inverted, causing all severities to be included regardless of threshold
- The `total` field always sums all four unfiltered counts regardless of filtering

## Conclusion

This criterion is NOT met. The filtering logic is fundamentally broken -- the comparison operators are inverted, and the total is computed from unfiltered values.
