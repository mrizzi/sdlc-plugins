# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Result: PASS

## What was checked

Verified whether the endpoint continues to return 404 for non-existent SBOM IDs, preserving existing behavior.

## Evidence from the diff

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` retains the existing SBOM fetch logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code was present before the PR changes and remains unchanged. The `SbomService::fetch()` method returns an error (mapped via `AppError`) when the SBOM ID does not exist, which produces a 404 response. The new threshold filtering logic is applied only after the SBOM is successfully fetched, so it does not interfere with the 404 behavior.

## Gap identified

None. The existing 404 behavior for non-existent SBOM IDs is preserved. The PR changes do not alter the SBOM lookup path.
