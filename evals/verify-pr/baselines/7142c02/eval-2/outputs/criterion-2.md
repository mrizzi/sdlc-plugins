# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Result: PASS

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles the no-threshold case in the `None` arm of the match expression:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When `params.threshold` is `None` (i.e., no `threshold` query parameter is provided), the original `summary` object is returned unchanged. This preserves full backward compatibility -- the response structure and content are identical to the pre-change behavior.

The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

Axum's `Query` extractor will deserialize a missing query parameter as `None` for `Option<T>` fields, so omitting the parameter entirely works correctly.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` arm returns the unmodified aggregation result
- The `threshold` field is `Option<String>`, correctly allowing it to be absent

## Conclusion

Backward compatibility is preserved. When no threshold parameter is provided, the endpoint returns all severity counts exactly as before.
