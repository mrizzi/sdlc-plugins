# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

The code handles the absence of a threshold parameter via the `None` branch of the match expression:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None` (since the field is `Option<String>`), and the original unmodified `summary` is returned directly. This preserves the existing behavior -- all severity counts (critical, high, medium, low, and total) are returned exactly as they were before the PR.

### Conclusion

Backward compatibility is maintained. When no threshold is specified, the endpoint returns the same response as before the change. This criterion is satisfied.
