# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The PR implements the no-threshold case via a `match` statement on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` is returned without any modification. This preserves the existing behavior exactly.

The `SummaryParams` struct uses `Option<String>` for the threshold field:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

Since `threshold` is `Option<String>`, Axum/serde will deserialize a missing query parameter as `None`, which correctly triggers the `None` branch of the match statement.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` branch returns the unmodified summary
- `Option<String>` correctly handles the absence of the query parameter

## Conclusion

This criterion IS met. Backward compatibility is preserved when no threshold parameter is provided.
