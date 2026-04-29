# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The PR adds the `threshold` parameter as an `Option<String>` in the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` is `None`. The match expression in the handler handles this case explicitly:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When `threshold` is `None`, the code returns the unmodified `summary` object directly. This preserves the original behavior -- all severity counts (critical, high, medium, low) are returned exactly as they were before the change.

The `advisory_summary` function signature changed to accept the additional `Query(params): Query<SummaryParams>` parameter, but since all fields in `SummaryParams` are `Option`, the query string is not required. An HTTP request without any query parameters will deserialize successfully with `threshold: None`.

### Backward compatibility assessment

- The endpoint path is unchanged: `GET /api/v2/sbom/{id}/advisory-summary`
- No existing fields are removed from the response
- The `threshold` parameter is purely additive (optional)
- When omitted, the response is identical to the pre-change behavior

Note: The response does NOT include the `threshold_applied` boolean field specified in Criterion 5, but that is a separate criterion. For the purposes of backward compatibility of the existing response shape, this criterion is satisfied.

## Conclusion

This criterion IS satisfied. The endpoint without a `threshold` parameter returns all severity counts, preserving backward compatibility.
