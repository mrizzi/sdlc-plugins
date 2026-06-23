# Criterion 1 Analysis

**Acceptance Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

## Evidence from the Diff

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses a positional index approach:

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

### Logic Trace for `threshold=high`

When `threshold=high`:
- `threshold_idx = 1` (position of "high" in the array)
- `critical`: always included (no condition) -- correct
- `high`: `threshold_idx <= 1` evaluates to `1 <= 1 = true` -- included -- correct
- `medium`: `threshold_idx <= 2` evaluates to `1 <= 2 = true` -- included -- **INCORRECT**: medium should be excluded when threshold=high
- `low`: `threshold_idx <= 3` evaluates to `1 <= 3 = true` -- included -- **INCORRECT**: low should be excluded when threshold=high

The comparison logic is inverted. The code checks whether the threshold index is less than or equal to the severity's position, but it should check whether the severity's position is less than or equal to the threshold index. For threshold=high (idx=1), the code should only include severities at positions 0 (critical) and 1 (high), zeroing out positions 2 (medium) and 3 (low).

### Additional Issue: Total Recomputation

The `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of which severities were zeroed out. Even if the filtering logic were correct, the total would not reflect the filtered result.

### Conclusion

The filtering logic does not correctly implement threshold=high. When threshold=high is specified, the response will still include medium and low counts instead of zeroing them out. The criterion is not satisfied.
