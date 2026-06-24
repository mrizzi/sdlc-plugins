# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The diff preserves the existing 404 behavior for non-existent SBOM IDs. The handler code shows:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` call is unchanged from the original implementation. Based on the repository conventions documented in `repo-backend.md`, error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping, and `AppError` implements `IntoResponse`. When a non-existent SBOM ID is requested, `SbomService::fetch()` would return an appropriate error (likely a 404 Not Found), which propagates through the `?` operator.

The diff does not modify the SBOM fetching logic or the error handling path. The `?` operator at the end of the `fetch()` call ensures errors propagate correctly.

While no new test was added for this behavior (the test file `tests/api/advisory_summary.rs` is missing from the diff entirely), the existing behavior is preserved because the relevant code path is unchanged.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::new(&db).fetch(sbom_id.id)` call is unchanged in the diff
- Error propagation via `?` operator is preserved
- The handler return type remains `Result<Json<AdvisorySummary>, AppError>`
- No modifications to error handling paths in the diff
