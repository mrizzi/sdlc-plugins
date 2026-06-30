## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Reasoning

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the `match` expression falls through to the `None` arm:

```rust
None => summary,
```

This returns the original `summary` object unchanged, preserving all severity counts (critical, high, medium, low, total) exactly as they were before the change.

The `SummaryParams` struct uses `Option<String>` for the threshold field, so omitting the query parameter results in `None` by default, which is correct Axum/serde behavior.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None` branch of the match returns the unmodified `summary` object
- The `threshold` field is `Option<String>`, defaulting to `None` when not provided
- Backward compatibility is preserved -- the response structure and values are unchanged when no threshold is specified
