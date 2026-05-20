# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing SBOM fetch logic is preserved in the handler. The code fetches the SBOM before performing any threshold filtering:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to fetch SBOM")?;
```

The `?` operator propagates any error from `.fetch()`, including the case where the SBOM does not exist. Based on the repository conventions documented in `repo-backend.md`, the `AppError` enum implements `IntoResponse`, so a not-found error from the service layer would be converted to a 404 HTTP response.

The PR diff does not modify this fetch logic -- the SBOM lookup and error propagation remain unchanged from the original implementation. The threshold filtering is applied only after a successful SBOM fetch, so the 404 behavior for non-existent SBOM IDs is preserved.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- SBOM fetch with `.context()` and `?` is unchanged
- The threshold filtering logic is placed after the SBOM fetch, not before
- `common/src/error.rs::AppError` implements `IntoResponse` per the repository conventions
- No modifications to the SBOM service layer appear in the diff
