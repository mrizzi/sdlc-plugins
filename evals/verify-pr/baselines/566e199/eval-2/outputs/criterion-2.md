## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` shows the filtering logic wrapped in a `match &params.threshold` expression. When `params.threshold` is `None` (no threshold query parameter provided), the code falls through to the `None => summary` arm, which returns the original unfiltered `summary` object directly.

This preserves backward compatibility: existing callers that do not pass a `threshold` parameter will receive the same response as before -- all severity counts (critical, high, medium, low) plus the total.

The `SummaryParams` struct defines `threshold` as `Option<String>`, meaning the query parameter is optional and defaults to `None` when absent.

### Evidence

```rust
None => summary,
```

This arm returns the unmodified summary, preserving all severity counts.

### Conclusion

This criterion is satisfied. The endpoint without a threshold parameter returns all severity counts unchanged.
