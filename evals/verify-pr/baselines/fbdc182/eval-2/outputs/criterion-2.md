# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Result: PASS

## Reasoning

When the `threshold` query parameter is not provided, `params.threshold` is `None`. The code enters the `None =>` branch of the match expression:

```rust
None => summary,
```

This returns the original `summary` object unmodified, which contains all four severity counts (`critical`, `high`, `medium`, `low`) plus `total`. This preserves backward compatibility -- existing API consumers who do not provide the `threshold` parameter will receive the same response as before.
