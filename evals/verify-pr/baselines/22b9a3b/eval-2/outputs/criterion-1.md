# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR diff adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. When `threshold=high` is provided, the code looks up the threshold in the `severity_order` array `["critical", "high", "medium", "low"]` and finds index 1 for "high".

The filtering logic then applies:
- `critical`: always included (no conditional)
- `high`: included if `threshold_idx <= 1` — for "high" (index 1), this is `1 <= 1 = true`, so high IS included
- `medium`: included if `threshold_idx <= 2` — for "high" (index 1), this is `1 <= 2 = true`, so medium IS ALSO included
- `low`: included if `threshold_idx <= 3` — for "high" (index 1), this is `1 <= 3 = true`, so low IS ALSO included

This means `threshold=high` returns counts for ALL severities (critical, high, medium, AND low), not just critical and high. The filtering logic is inverted — it should zero out severities BELOW the threshold, but instead it includes everything at or below the threshold index.

For the criterion to be satisfied, `threshold=high` should return only critical and high (zeroing medium and low). The correct condition should be `threshold_idx >= 1` (for high), `threshold_idx >= 2` (for medium), etc., or more precisely, the logic should zero out entries whose index is strictly greater than `threshold_idx`.

Additionally, the `total` field is computed from ALL unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. Even if the filtering were correct, the total would be wrong.

## Evidence

From the diff:
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

For `threshold=high` (index 1): all conditions `1<=1`, `1<=2`, `1<=3` are true, so no severity is filtered out. The criterion requires that medium and low be excluded.
