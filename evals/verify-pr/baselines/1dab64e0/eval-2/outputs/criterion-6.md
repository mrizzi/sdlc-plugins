## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Verdict: PASS

### Analysis

The diff preserves the existing 404 behavior for non-existent SBOM IDs. The relevant code path is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` method returns a `Result` that produces an `AppError::NotFound` when the SBOM ID does not exist. This behavior is part of the existing code (not modified in the diff) and continues to work because the diff only adds the threshold filtering logic after the SBOM fetch succeeds.

The function signature still returns `Result<Json<AdvisorySummary>, AppError>`, so the `AppError::NotFound` propagates correctly to produce a 404 HTTP response.

While no new test was written to verify this behavior (the test file `tests/api/advisory_summary.rs` is absent), the existing behavior is structurally preserved since the SBOM fetch code path is not modified.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the `SbomService::fetch()` call and error handling are unchanged
- The `?` operator propagates `AppError::NotFound` from the fetch call
- The threshold filtering logic is applied only after a successful SBOM fetch
- Existing behavior is preserved by virtue of not modifying the fetch path
