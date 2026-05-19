## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Verdict: PASS

### Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` shows that the `threshold` field in `SummaryParams` is declared as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` will be `None`. The match statement handles this case:

```rust
None => summary,
```

This returns the unfiltered `summary` directly, which contains all four severity counts (critical, high, medium, low) as returned by `AdvisoryService::aggregate_severities()`.

This preserves backward compatibility -- calling the endpoint without `?threshold=...` returns the same response as before the change.

**Evidence from the diff:**
- Lines show `match &params.threshold { ... None => summary }` which passes through the unfiltered aggregation result.
- The `SummaryParams` struct uses `Option<String>`, so the parameter is optional and the endpoint works without it.

This criterion is satisfied.
