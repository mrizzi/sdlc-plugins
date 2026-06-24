# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds an optional `threshold` query parameter via the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The `threshold` field is `Option<String>`, which means when no `threshold` query parameter is provided, the value is `None`.

The filtering logic handles this case explicitly:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When `params.threshold` is `None`, the original `summary` (containing all severity counts) is returned unchanged. This preserves backward compatibility -- callers that do not provide the `threshold` parameter receive the same response as before.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None` arm of the match returns the unmodified `summary` object
- The `SummaryParams.threshold` is `Option<String>`, making it optional in query parameters
- No changes to the response struct or other endpoint behavior are introduced
