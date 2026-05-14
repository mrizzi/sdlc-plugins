## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Result: PASS**

### Evidence

The diff shows that when no threshold parameter is provided, the `params.threshold` field is `None`, and the code falls through to the `None` arm of the match:

```rust
None => summary,
```

This returns the original, unfiltered `AdvisorySummary` directly, preserving backward compatibility. The existing behavior is maintained for clients that do not supply the `threshold` query parameter.

The `SummaryParams` struct defines `threshold` as `Option<String>`, so the parameter is truly optional and existing callers are unaffected.
