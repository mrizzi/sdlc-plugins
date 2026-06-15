# Criterion 2: Backward compatibility without threshold parameter

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` shows that when no threshold parameter is provided, the code falls through to the `None` arm of the match:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When `params.threshold` is `None`, the original unfiltered `summary` is returned directly. This preserves the existing behavior -- all severity counts (critical, high, medium, low) are returned as they were before this change.

The `SummaryParams` struct defines `threshold` as `Option<String>`, so the absence of the query parameter results in `None`, which correctly triggers the pass-through path.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` arm returns the unmodified aggregation result.
- The `threshold` field is `Option<String>`, so omitting the query parameter defaults to `None`.
- Backward compatibility is preserved.
