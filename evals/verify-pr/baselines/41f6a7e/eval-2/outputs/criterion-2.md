# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

When no `threshold` query parameter is provided, `params.threshold` is `None`. The match expression takes the `None` branch, which returns `summary` unchanged:

```rust
None => summary,
```

The original `AdvisorySummary` from `AdvisoryService::aggregate_severities` is returned directly with no modifications. This preserves backward compatibility -- the response is identical to what it was before the threshold feature was added.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None` match arm returns the original `summary` without any filtering
- The `SummaryParams` struct uses `Option<String>` for the `threshold` field, making it optional in the query string
- No changes were made to the `AdvisoryService::aggregate_severities` method that would alter the base response
