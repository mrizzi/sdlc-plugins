# Criterion 1: Threshold filtering returns only severities at or above threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** PARTIAL FAIL

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds threshold filtering logic. When `threshold=high` is provided, the code locates "high" in the `severity_order` array at index 1 and then conditionally includes counts:

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
- `high` is included because `1 <= 1` is true (correct)
- `medium` is zeroed because `1 <= 2` is true -- WAIT, this is a problem. When threshold_idx is 1 (high), `1 <= 2` evaluates to true, so medium would be INCLUDED, not excluded.

**Bug identified:** The filtering logic is INVERTED for medium and low. When threshold=high:
- `threshold_idx = 1`
- `if threshold_idx <= 2 { summary.medium } else { 0 }` -- since 1 <= 2 is true, medium is INCLUDED
- `if threshold_idx <= 3 { summary.low } else { 0 }` -- since 1 <= 3 is true, low is INCLUDED

This means threshold=high would return ALL counts, not just critical and high. The logic is backwards -- it should be `>=` comparisons from the other direction, or the conditions should be reversed. The code would only zero out a field when `threshold_idx > N`, but the threshold index for "high" (1) is never greater than any of the comparison values (1, 2, 3).

Actually, re-reading more carefully: the intent seems to be that fields at positions > threshold_idx should be zeroed. For threshold=high (idx=1):
- critical (idx 0): always shown (correct)
- high (idx 1): shown if threshold_idx <= 1 -- 1 <= 1 = true, shown (correct)
- medium (idx 2): shown if threshold_idx <= 2 -- 1 <= 2 = true, shown (WRONG -- should be hidden)
- low (idx 3): shown if threshold_idx <= 3 -- 1 <= 3 = true, shown (WRONG -- should be hidden)

The condition is checking the wrong direction. It should be something like `if 1 <= threshold_idx` (i.e., the severity index should be <= threshold_idx), not `if threshold_idx <= 1`. The correct logic would be: include severity at position N if N <= threshold_idx.

**Additionally**, the `total` field is computed from unfiltered counts regardless of threshold:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This should sum only the filtered counts.

**Result:** FAIL -- The threshold filtering logic is inverted and would not correctly filter severities. The total is also computed incorrectly from unfiltered values.
