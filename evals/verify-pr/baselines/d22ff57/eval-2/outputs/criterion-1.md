# Criterion 1

**Text**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Evidence from diff**:

The diff in `get.rs` shows filtering logic:

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

When `threshold=high`, `threshold_idx` = 1. The logic yields:
- `critical`: always included (no condition)
- `high`: `1 <= 1` is true, so included
- `medium`: `1 <= 2` is true, so **medium is included** -- this is WRONG
- `low`: `1 <= 3` is true, so **low is included** -- this is WRONG

Wait -- re-reading the logic more carefully: the intention seems to be that indices at or below `threshold_idx` are included. But `critical` is index 0, `high` is index 1, `medium` is index 2, `low` is index 3. The conditions check `threshold_idx <= N` where N is the index of the severity level. When `threshold=high` (`threshold_idx=1`):
- `high`: `1 <= 1` -> true -> included
- `medium`: `1 <= 2` -> true -> **included (WRONG)**
- `low`: `1 <= 3` -> true -> **included (WRONG)**

The logic is inverted. The condition should be `N <= threshold_idx` (i.e., include only severities whose index is at or below the threshold index) but instead uses `threshold_idx <= N`. This means `threshold=high` would still return all four severity counts, not just critical and high.

Actually, let me re-examine. The severity ordering states critical > high > medium > low. Index 0 = critical (highest), index 3 = low (lowest). The goal is: when threshold=high (index 1), include only severities at index 0 (critical) and index 1 (high), omitting index 2 (medium) and index 3 (low).

The condition `threshold_idx <= 1` for high means: is 1 <= 1? Yes. But this is checking whether the threshold is at or above high, not whether high should be included. For medium: `threshold_idx <= 2` means is 1 <= 2? Yes -- so medium is included, which is WRONG.

The correct condition should be the reverse: the severity's index should be <= threshold_idx. So for medium (index 2): `2 <= 1` would be false, correctly excluding it.

However, looking at it from a different angle: the way the code is structured, the hardcoded numbers (1, 2, 3) represent the index of each severity in the array. The condition `threshold_idx <= 1` for high asks "is the threshold severity at index 0 or 1 (critical or high)?". If threshold is high (1), yes. If threshold is medium (2), 2 <= 1 is false, so high would be excluded. This actually means: "include this severity only if the threshold is at or above this severity level."

Wait, that interpretation works correctly:
- threshold=high (idx=1): critical always, high: 1<=1 true, medium: 1<=2 true, low: 1<=3 true => returns ALL counts. This is WRONG.

The filtering logic is broken. With `threshold=high`, all four severity levels pass their conditions, so all counts are returned. The criterion requires only critical and high.

**Verdict**: FAIL

The filtering logic is inverted. `threshold=high` would return counts for all four severities instead of only critical and high.
