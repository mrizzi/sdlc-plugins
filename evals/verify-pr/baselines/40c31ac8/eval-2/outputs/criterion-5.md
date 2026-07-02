# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Result: FAIL

## What was checked

Verified whether the API response includes a `threshold_applied` boolean field that indicates whether threshold filtering is active.

## Evidence from the diff

The filtered response constructed in `modules/fundamental/src/advisory/endpoints/get.rs` creates an `AdvisorySummary` with these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `None` case returns `summary` as-is:
```rust
None => summary,
```

Neither branch adds a `threshold_applied` field to the response. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`, not modified in this diff) was not extended to include this field.

## Gap identified

The `threshold_applied` boolean field is **completely absent** from the response. The implementation would need to:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct in `model/summary.rs`
2. Set it to `true` when a valid threshold is provided and filtering is applied
3. Set it to `false` when no threshold is provided

Neither the struct modification nor the field assignment was implemented.
