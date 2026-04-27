## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Result: PASS

### Analysis

The existing 404 behavior is preserved. The handler's early code path that fetches the SBOM remains unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code predates the PR changes and is untouched by the diff. When `SbomService::fetch()` is called with a non-existent SBOM ID, it returns an error that propagates through the `?` operator as an `AppError`. Per the repository's conventions, `AppError` implements `IntoResponse` and maps not-found conditions to HTTP 404.

The PR's changes are entirely additive and occur after the SBOM has been successfully fetched and advisory severities have been aggregated. The threshold filtering logic does not alter, bypass, or interfere with the early-return error handling path. Therefore, the 404 behavior for non-existent SBOM IDs is correctly preserved.
