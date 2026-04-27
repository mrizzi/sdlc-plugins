## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Result: PASS

### Analysis

The handler correctly handles the case where no `threshold` query parameter is provided. The `SummaryParams` struct declares `threshold` as `Option<String>`:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` parameter is present in the query string, `params.threshold` is `None`. The match expression handles this case explicitly:

```rust
None => summary,
```

This returns the original `summary` object unchanged, preserving all four severity counts (critical, high, medium, low) and the total exactly as they were before this PR's changes.

This ensures full backward compatibility -- existing API consumers that do not pass a `threshold` parameter will continue to receive the same response they received before.
