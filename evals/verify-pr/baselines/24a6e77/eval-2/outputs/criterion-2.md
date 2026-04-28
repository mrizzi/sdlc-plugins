# Criterion 2: No threshold returns all severity counts (backward compatible)

## Criterion

`GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible).

## Verdict: PASS

## Reasoning

The diff introduces the `SummaryParams` struct with `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` will be `None`. The match expression handles this case:

```rust
None => summary,
```

This returns the unmodified `summary` object directly, which contains all four severity counts as produced by `AdvisoryService::aggregate_severities()`. This preserves the original behavior exactly -- the response is identical to what was returned before the threshold feature was added.

## Evidence

- The `SummaryParams.threshold` field is `Option<String>`, meaning it is not required
- The `None` arm of the match returns the original `summary` without modification
- The existing `AdvisoryService::aggregate_severities()` method in `advisory.rs` is unchanged (the diff shows no modifications to the aggregation logic itself)
- The original endpoint signature added `Query(params): Query<SummaryParams>` as a new parameter, which does not affect callers who omit the query string
