## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Evidence

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles the no-threshold case in the `None` arm of the match:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original unfiltered `summary` is returned directly. This preserves backward compatibility -- all severity counts (critical, high, medium, low) are included in the response.

The `SummaryParams` struct uses `Option<String>` for the threshold field, which correctly makes it optional in query parameter deserialization:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

This criterion is satisfied.
