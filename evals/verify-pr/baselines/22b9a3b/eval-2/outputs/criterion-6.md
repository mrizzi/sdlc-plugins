# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The PR diff preserves the existing 404 behavior for non-existent SBOM IDs. The handler code fetches the SBOM first and returns a 404 if it doesn't exist:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code was present before the PR changes (it appears in the unchanged context lines of the diff). The `.fetch()` call will return an error for non-existent SBOM IDs, and the `?` operator will propagate it as an `AppError`, which maps to a 404 response.

The threshold filtering logic is applied AFTER the SBOM lookup succeeds, so the existing 404 behavior is preserved — if the SBOM doesn't exist, the handler returns 404 before any threshold processing occurs.

However, while the existing behavior is preserved in the endpoint code, the task requires integration tests to verify this behavior, and no test file was created (see test requirements analysis).

## Evidence

The SBOM fetch and 404 handling code is in the unchanged context of the diff, confirming it was not modified. The new threshold logic runs only after a successful SBOM fetch.
