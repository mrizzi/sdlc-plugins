# Criterion 1 Analysis

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Assessment: PARTIAL / FAIL

### What the criterion requires
When `threshold=high` is provided, the response should return counts for `critical` and `high` only. All lower severities (`medium`, `low`) should be excluded (presumably zeroed out or omitted).

### What the diff implements
The diff adds a `SummaryParams` struct with an optional `threshold` field and implements filtering logic in the `advisory_summary` handler:

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

### Issues found

1. **`total` is computed from unfiltered counts.** The `total` field sums all four severity counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of threshold filtering. When `threshold=high`, `medium` and `low` are zeroed out in the response, but `total` still includes unfiltered medium and low counts. This is inconsistent — `total` should reflect only the filtered counts.

2. **The filtering logic itself is partially correct.** For `threshold=high`, `threshold_idx` would be 1. Then:
   - `critical`: always included (correct)
   - `high`: `threshold_idx <= 1` is true, so included (correct)
   - `medium`: `threshold_idx <= 2` is true (1 <= 2), so included (**INCORRECT** — medium should be excluded when threshold is high)

   Wait — re-analyzing: with `threshold=high`, `threshold_idx = 1`. The check is `threshold_idx <= 2` for medium, which is `1 <= 2 = true`, so medium IS included. This is **WRONG** — medium should be zeroed out when threshold is high.

   Actually, let me re-read the logic more carefully. The condition checks the threshold_idx against fixed values. The logic seems inverted. For `threshold=high` (idx=1):
   - `high`: `1 <= 1` = true -> include (correct)
   - `medium`: `1 <= 2` = true -> include (**BUG**: should exclude medium for threshold=high)
   - `low`: `1 <= 3` = true -> include (**BUG**: should exclude low for threshold=high)

   The filtering logic is **fundamentally broken**. It should be checking whether each severity's position is at or above the threshold position, not whether the threshold index is less than or equal to the severity's position. The correct logic would be: include a severity if its index <= threshold_idx (i.e., severity_position <= threshold_position).

   Corrected logic should be:
   - `high`: include if `1 <= threshold_idx` (severity idx 1 <= threshold idx 1 -> true, correct)
   - `medium`: include if `2 <= threshold_idx` (severity idx 2 <= threshold idx 1 -> false, exclude, correct)
   - `low`: include if `3 <= threshold_idx` (severity idx 3 <= threshold idx 1 -> false, exclude, correct)

   But the code checks the other direction: `threshold_idx <= severity_fixed_idx`. This means ALL severities at or below the threshold are included, which is the opposite of what's required.

### Verdict: FAIL

The filtering logic is inverted. For `threshold=high`, it would include medium and low when they should be excluded. Additionally, the `total` field uses unfiltered counts.
