## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Result: PASS

### Analysis

The existing 404 behavior is preserved by the unchanged code path at the beginning of the handler:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code was present before the PR changes and remains untouched. When `SbomService::fetch()` is called with a non-existent SBOM ID, it returns an error (or `None` mapped to an error), which propagates through the `?` operator as an `AppError`. Based on the repository conventions, `AppError` implements `IntoResponse` and maps not-found conditions to HTTP 404 status codes.

The PR changes only add the threshold filtering logic after the SBOM has been successfully fetched and the advisory severities have been aggregated. The new code does not alter the early-return error handling path, so the 404 behavior for non-existent SBOM IDs is correctly preserved.
