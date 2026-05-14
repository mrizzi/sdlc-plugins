# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The PR correctly handles the case where no `threshold` query parameter is provided. The `SummaryParams` struct declares `threshold` as `Option<String>`, meaning it defaults to `None` when absent from the query string.

In the handler, the `match &params.threshold` expression has a `None` arm that returns the unmodified `summary` object directly:

```rust
None => summary,
```

This preserves the original behavior -- when no threshold is specified, the endpoint returns all severity counts exactly as the existing `aggregate_severities` service method produces them. The response structure is unchanged; the `AdvisorySummary` struct still contains `critical`, `high`, `medium`, `low`, and `total` fields.

The only concern is that the existing `AdvisorySummary` struct does not include the `threshold_applied` boolean field required by criterion 5, but that is a separate criterion. For backward compatibility of the severity counts themselves, this criterion is satisfied.

## Evidence

- `get.rs` line 21: `pub threshold: Option<String>` -- optional parameter
- `get.rs` line 55: `None => summary` -- unmodified summary returned when no threshold
- No changes to `AdvisoryService::aggregate_severities` in `advisory.rs` -- service logic unchanged
