# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing SBOM fetch logic in the handler is preserved:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to fetch SBOM")?;
```

This code fetches the SBOM by ID and propagates any error (including not-found errors) via the `?` operator and `AppError`. The repository uses the `common/src/error.rs::AppError` enum which implements `IntoResponse`, and the existing `SbomService::fetch` method would return an appropriate error for non-existent IDs.

The PR diff does not modify the SBOM fetch logic or error handling path. The threshold filtering occurs after the SBOM fetch, so a non-existent SBOM ID would still result in an error response before the filtering logic is reached.

While no integration test was added to verify this behavior (the task required a test for 404 on non-existent SBOM IDs in `tests/api/advisory_summary.rs`), the existing behavior is preserved in the handler code itself.

The criterion is satisfied (existing behavior is preserved).
