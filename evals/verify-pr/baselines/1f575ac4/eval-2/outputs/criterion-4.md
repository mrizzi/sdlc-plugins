## Criterion 4: Severity ordering is correct: critical > high > medium > low

**Verdict: PASS**

### Reasoning

The severity ordering is encoded as an array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array places severities in descending order: critical (index 0) > high (index 1) > medium (index 2) > low (index 3). A lower index means higher severity, which correctly implements the required ordering: critical > high > medium > low.

The ordering itself is correct. The issue with the filtering logic (criterion 1) is about how the ordering is applied for filtering, not about the ordering definition itself.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `severity_order` array `["critical", "high", "medium", "low"]` correctly encodes the required ordering
- Index 0 = critical (highest), index 3 = low (lowest)
