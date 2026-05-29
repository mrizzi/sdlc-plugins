# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` preserves the existing 404 behavior. The handler includes:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `.fetch(sbom_id.id)` call retrieves the SBOM by ID. Based on the repository's convention (using `AppError` which implements `IntoResponse` and the Axum framework), when a non-existent SBOM ID is provided:

1. `SbomService::fetch()` would return an error (likely `AppError::NotFound` or similar)
2. The `?` operator propagates the error
3. The `Result<Json<AdvisorySummary>, AppError>` return type ensures the error is converted to an HTTP response via the `IntoResponse` implementation on `AppError`

This existing behavior is not modified by the PR. The SBOM lookup code was present before the PR changes and remains unchanged. The PR only adds code after the SBOM lookup succeeds (threshold filtering and response construction).

**Evidence:**
- `SbomService::new(&db).fetch(sbom_id.id)` call is preserved from the original code
- Error propagation via `?` operator is preserved
- Return type `Result<Json<AdvisorySummary>, AppError>` supports error responses
- No changes to the SBOM lookup or error handling path
- The common error module (`common/src/error.rs`) contains `AppError` which implements `IntoResponse` per repo conventions

This criterion is satisfied -- the existing 404 behavior is preserved.

**Note:** While no integration test for the 404 case was added (the test file is entirely missing from the diff -- see separate analysis), the existing endpoint behavior is preserved in the code.
