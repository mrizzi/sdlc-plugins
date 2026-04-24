## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Result: PASS

### Analysis

The handler correctly branches on the `params.threshold` value using a `match` expression:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

The `SummaryParams` struct declares `threshold` as `Option<String>`:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided in the request URL, Axum's `Query` extractor deserializes this as `None`. The `None` arm of the match expression returns the original `summary` object unchanged, with all four severity counts (critical, high, medium, low) and the total intact.

This preserves full backward compatibility: existing clients that do not pass a `threshold` parameter will continue to receive all severity counts exactly as before the change was introduced.
