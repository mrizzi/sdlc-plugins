# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The PR diff adds filtering logic in `get.rs` that attempts to implement threshold-based filtering. When `threshold=high`, the code sets `threshold_idx` to 1 (the position of "high" in the `severity_order` array `["critical", "high", "medium", "low"]`).

The conditional logic then applies:
- `critical`: always included (no conditional)
- `high`: included when `threshold_idx <= 1` -- this is true for "high" (idx=1), so high is included. Correct.
- `medium`: included when `threshold_idx <= 2` -- this is false for "high" (idx=1 <= 2 is true), so medium IS included. **This is INCORRECT.** For `threshold=high`, medium should be excluded but the condition `1 <= 2` evaluates to true, so medium counts are returned.
- `low`: included when `threshold_idx <= 3` -- same issue, `1 <= 3` is true, so low IS also included.

Wait -- re-reading the code more carefully:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For `threshold=high`, `threshold_idx = 1`.

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

The logic is inverted. `threshold_idx <= 2` means "if the threshold position is at or before medium in the array, include medium." Since high (idx=1) is before medium (idx=2), `1 <= 2` is true, so medium IS included when `threshold=high`. This defeats the purpose of the filter.

The correct logic should be the opposite: include a severity level only if its index is at or before (less than or equal to) the threshold index. The code should check whether each severity's index is <= threshold_idx, not the other way around. The conditions should be:
- `critical` (idx=0): always included (0 <= any threshold_idx)
- `high` (idx=1): `1 <= threshold_idx` -- for threshold=high (idx=1), 1<=1 is true, include. Correct.
- `medium` (idx=2): `2 <= threshold_idx` -- for threshold=high (idx=1), 2<=1 is false, exclude. Correct.
- `low` (idx=3): `3 <= threshold_idx` -- for threshold=high (idx=1), 3<=1 is false, exclude. Correct.

But the code does `threshold_idx <= 2` instead of `2 <= threshold_idx`. The comparisons are backwards.

Additionally, the `total` field is computed from ALL unfiltered counts regardless of threshold:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This should sum only the filtered counts (the values actually returned), not the original unfiltered values.

**Conclusion:** The filtering logic has an inverted comparison bug. For `threshold=high`, medium and low would still be included instead of being zeroed out. The total is also computed incorrectly from unfiltered values. This criterion is NOT satisfied.
