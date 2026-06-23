# Criterion 2: Without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

The acceptance criterion requires that `GET /api/v2/sbom/{id}/advisory-summary` without a threshold parameter returns all severity counts, maintaining backward compatibility with the existing API.

### Code Analysis

In `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold parameter is defined as `Option<String>`:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The filtering logic handles the `None` case:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` (containing all severity counts: critical, high, medium, low, and total) is returned unchanged.

### Conclusion

The `None` branch correctly passes through the complete, unfiltered summary. Requests without the threshold parameter receive all severity counts exactly as before the change. Backward compatibility is preserved. This criterion is satisfied.
