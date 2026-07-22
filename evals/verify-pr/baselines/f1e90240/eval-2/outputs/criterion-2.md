# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The PR handles the absence of a threshold parameter in the `None` branch of the match expression:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the code returns the original `summary` object unchanged. This preserves the existing behavior: all four severity counts (critical, high, medium, low) plus the total are returned exactly as they were before this change.

The `SummaryParams` struct uses `Option<String>` for the threshold field:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

This correctly makes the parameter optional. When the query string does not contain `threshold`, Axum/serde will deserialize it as `None`.

## Conclusion

This criterion is **satisfied**. The endpoint without a threshold parameter returns the complete, unmodified advisory summary, maintaining backward compatibility with existing clients.
