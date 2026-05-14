# Criterion 1: Threshold filtering returns only severities at or above the threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict: FAIL**

## Detailed Reasoning

The PR implements threshold filtering in `modules/fundamental/src/advisory/endpoints/get.rs` using an index-based comparison against the `severity_order` array `["critical", "high", "medium", "low"]` (indices 0, 1, 2, 3 respectively).

When `threshold=high`, the code computes `threshold_idx = 1` (the position of "high" in the array). It then applies the following conditions:

```rust
critical: summary.critical,                              // always included
high: if threshold_idx <= 1 { summary.high } else { 0 }, // 1 <= 1 = true => INCLUDED
medium: if threshold_idx <= 2 { summary.medium } else { 0 }, // 1 <= 2 = true => INCLUDED (BUG)
low: if threshold_idx <= 3 { summary.low } else { 0 },      // 1 <= 3 = true => INCLUDED (BUG)
```

The filtering logic is inverted. The condition `threshold_idx <= N` checks whether the threshold index is less than or equal to each severity's hardcoded position constant. Since the threshold index (1 for "high") is always less than or equal to the positions of lower severities (2 for "medium", 3 for "low"), those lower severities are incorrectly included.

**Correct logic** would check whether each severity's index is less than or equal to the threshold index:

```rust
// severity_idx <= threshold_idx
high: if 1 <= threshold_idx { summary.high } else { 0 },    // 1 <= 1 = true => INCLUDED (correct)
medium: if 2 <= threshold_idx { summary.medium } else { 0 }, // 2 <= 1 = false => EXCLUDED (correct)
low: if 3 <= threshold_idx { summary.low } else { 0 },      // 3 <= 1 = false => EXCLUDED (correct)
```

### Additional issue: `total` field miscalculation

The `total` field in the filtered response is also incorrect:

```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This sums all unfiltered counts. Even if the individual severity filtering were correct, the total would still include all four severity counts. The total should be computed from only the filtered (included) counts.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-55 of the diff
- The comparison direction is `threshold_idx <= constant` instead of `constant <= threshold_idx`
- For `threshold=high` (idx=1): medium (pos 2) and low (pos 3) are incorrectly included because 1 <= 2 and 1 <= 3 are both true
- For `threshold=critical` (idx=0): high, medium, and low are all incorrectly included because 0 <= 1, 0 <= 2, and 0 <= 3 are all true
- Only `threshold=low` (idx=3) would work correctly by coincidence, since 3 <= 1, 3 <= 2 are false while 3 <= 3 is true -- but this would filter medium and high while keeping low, which is still wrong
