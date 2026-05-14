## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Result: FAIL**

### Evidence

The task acceptance criteria explicitly require: "Response includes a `threshold_applied` boolean field indicating whether filtering is active."

Examining the diff, the `AdvisorySummary` struct returned in the response contains only:
- `critical`
- `high`
- `medium`
- `low`
- `total`

There is no `threshold_applied` field anywhere in the diff. The `AdvisorySummary` struct is not modified (the diff for `advisory.rs` shows no changes to the struct definition), and no new field is added to the response.

The handler constructs `AdvisorySummary` with only the five fields listed above:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `threshold_applied` boolean field is entirely absent from the implementation. This criterion is clearly not met.
