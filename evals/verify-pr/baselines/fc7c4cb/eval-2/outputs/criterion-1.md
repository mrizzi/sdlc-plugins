## Criterion 1

**Text:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**What I checked:** The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`, specifically the `match &params.threshold` block that constructs the filtered `AdvisorySummary`.

**Code evidence:**

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

**Analysis of the filtering logic:**

The severity_order array is `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3 (0 = most severe). For `threshold=high`, `threshold_idx = 1`. The intent is to include severities at or above the threshold (i.e., indices 0 and 1: critical and high).

However, the comparison direction is wrong. The code checks `threshold_idx <= N` (where N is the hardcoded index of each severity), but the correct check should be `N <= threshold_idx` (include severity N if its position is at or above the threshold level).

For `threshold=high` (threshold_idx=1):
- `critical`: always included (correct)
- `high`: `threshold_idx <= 1` => `1 <= 1` => true => included (happens to be correct for this case)
- `medium`: `threshold_idx <= 2` => `1 <= 2` => true => **included (WRONG -- should be excluded)**
- `low`: `threshold_idx <= 3` => `1 <= 3` => true => **included (WRONG -- should be excluded)**

The filter does not actually exclude medium and low when threshold=high. Only threshold=critical would zero out nothing, and threshold=low ironically excludes high and medium.

**Additionally**, the `total` field is computed from unfiltered counts:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This sums all four original severity counts regardless of what was filtered, so even if the per-field filtering worked, the total would be inconsistent.

**Verdict: FAIL**

The filtering logic has inverted comparisons. For `threshold=high`, medium and low counts are still included instead of being zeroed out. The total is also computed from unfiltered values.
