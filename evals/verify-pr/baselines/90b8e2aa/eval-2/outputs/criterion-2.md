# Criterion 2: Without threshold, returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

When no `threshold` query parameter is provided, the `params.threshold` field is `None`, and the code takes the `None` branch:

```rust
None => summary,
```

This returns the unmodified `summary` from `AdvisoryService::aggregate_severities()`, which contains all four severity counts (critical, high, medium, low) and the total.

### Evidence

- The `SummaryParams` struct defines `threshold` as `Option<String>`, so it correctly defaults to `None` when the query parameter is absent.
- The `None` arm passes through the original aggregated summary without any modification.
- No other code paths alter the summary before it is returned.

### Conclusion

Backward compatibility is preserved. Existing API consumers calling the endpoint without a `threshold` parameter will receive the same response structure and data as before this change.
