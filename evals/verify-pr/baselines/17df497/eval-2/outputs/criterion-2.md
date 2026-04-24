## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Result: PASS

### Analysis

The handler correctly branches on `params.threshold`:

```rust
None => summary,
```

When no `threshold` query parameter is provided, the `params.threshold` field is `None` (since it is declared as `Option<String>` in the `SummaryParams` struct). The `None` arm of the match expression returns the original `summary` object unchanged.

This preserves full backward compatibility: existing clients that do not pass a `threshold` parameter will continue to receive all four severity counts (critical, high, medium, low) along with the total, exactly as before the change.
