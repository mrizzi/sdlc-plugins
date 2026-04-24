## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Result: FAIL

### Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` contains an inverted comparison that causes incorrect results.

The severity order array is defined as:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This gives indices: critical=0, high=1, medium=2, low=3. For `threshold=high`, `threshold_idx` resolves to 1.

The filtering conditions are then applied as follows:

- `critical`: always included (hardcoded as `summary.critical`) -- correct
- `high`: `if threshold_idx <= 1` -- evaluates to `1 <= 1` = true -- included (correct)
- `medium`: `if threshold_idx <= 2` -- evaluates to `1 <= 2` = true -- **incorrectly included**
- `low`: `if threshold_idx <= 3` -- evaluates to `1 <= 3` = true -- **incorrectly included**

The condition `threshold_idx <= severity_position` is backwards. The intended behavior is to include only severities at or above the threshold. Since lower indices represent higher severity, the correct condition should be `severity_position <= threshold_idx` -- include a severity only if its position in the ordering is at or before the threshold position. With the inverted condition, `threshold=high` includes all four severity levels instead of only critical and high.

Additionally, even if the filtering logic were corrected, the `total` field is computed from the unfiltered counts:

```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This sums all four original severity counts regardless of which severities were filtered out. The total should reflect only the counts that are included in the filtered response.

Both the filtering inversion and the incorrect total computation cause this criterion to fail.
