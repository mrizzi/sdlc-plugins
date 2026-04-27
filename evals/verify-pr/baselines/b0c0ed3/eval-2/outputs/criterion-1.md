## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Result: FAIL

### Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` contains an inverted condition that produces incorrect results.

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

The condition `threshold_idx <= severity_position` is backwards. It should be `severity_position <= threshold_idx` to include only severities whose position in the ordering is at or above the threshold (i.e., index is less than or equal to the threshold index).

With the current logic, `threshold=high` returns counts for all four severity levels instead of only critical and high. The filter is effectively a no-op for most threshold values, which is the opposite of the intended behavior.

Additionally, the `total` field in the filtered response is computed from unfiltered counts:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

Even if the filtering conditions were corrected, the total would still reflect the sum of all severities rather than only the filtered ones. The total should sum only the counts that survived filtering.

This criterion fails due to both the inverted filtering logic and the incorrect total computation.
