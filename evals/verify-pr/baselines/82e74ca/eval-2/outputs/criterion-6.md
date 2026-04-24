## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Result: PASS

### Analysis

The existing 404 behavior is preserved because the early-return error handling path remains untouched by the PR changes:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code was present before the PR and is not modified by the diff. When `SbomService::fetch()` is called with a non-existent SBOM ID, it returns an error which propagates through the `?` operator as an `AppError`. Per the repository conventions, `AppError` implements `IntoResponse` and maps not-found errors to HTTP 404 status codes.

The PR changes only add the threshold filtering logic after the SBOM has been successfully fetched and the advisory severities have been aggregated. The new code path executes only when the SBOM exists. The early-return error handling for non-existent SBOMs is not altered, so the 404 behavior is correctly preserved.
