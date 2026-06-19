# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## What was checked

Inspected the PR diff for the case when no `threshold` query parameter is provided.

## Evidence

The `SummaryParams` struct defines `threshold` as `Option<String>`. In the handler, the filtering logic uses a `match` on `&params.threshold`:

```rust
None => summary,
```

When no threshold is provided, the original `summary` is returned unchanged. This preserves backward compatibility -- the response contains all severity counts as before.

The `SummaryParams` uses `Query<SummaryParams>` extraction. In Axum, when all fields of a query struct are `Option`, the query string can be entirely absent and the extraction will succeed with all fields set to `None`.

## Verdict: PASS

The implementation correctly returns the unmodified summary when no threshold parameter is provided, preserving backward compatibility.
