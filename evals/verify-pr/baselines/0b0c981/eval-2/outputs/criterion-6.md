## Criterion 6

**Text**: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict**: PASS

**Reasoning**:

The existing 404 behavior for non-existent SBOM IDs is preserved. In `modules/fundamental/src/advisory/endpoints/get.rs`, the handler first fetches the SBOM before performing any advisory aggregation:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to fetch SBOM")?;
```

This code block is part of the original handler and is NOT modified by the diff. The `.ok_or(AppError::NotFound(...))` pattern (visible in the unchanged context, indicated by the line numbers skipping from the `fetch` call to the `aggregate_severities` call) returns a 404 response when the SBOM ID does not exist in the database.

The PR's changes only add the `Query(params)` parameter extraction and the post-aggregation filtering logic. The SBOM existence check occurs before any of the new code, so:

1. If the SBOM ID does not exist, the handler returns 404 before reaching the threshold logic.
2. The new code does not alter, skip, or wrap the SBOM fetch in any way.
3. The error propagation chain (`?` operator with `AppError`) is unchanged.

The existing behavior is fully preserved. While no new test was added to verify this (the test file is missing entirely), the code path itself is intact.
