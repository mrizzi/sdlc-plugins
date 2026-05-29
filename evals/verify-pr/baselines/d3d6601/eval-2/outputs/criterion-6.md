# Criterion 6: 404 for non-existent SBOM IDs preserved

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Analysis

The diff preserves the existing SBOM fetch logic that handles non-existent SBOM IDs:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

This code was present before the diff and remains unchanged. The existing `SbomService::fetch()` method returns an error when the SBOM ID does not exist, which is handled by the `AppError` return type and results in a 404 response (per the repository's error handling conventions documented in `common/src/error.rs`).

The diff only adds threshold filtering logic AFTER the SBOM fetch succeeds, meaning:
1. If the SBOM ID does not exist, `fetch()` returns an error before reaching the new threshold code
2. The error propagates through `Result<Json<AdvisorySummary>, AppError>` as before
3. The 404 behavior is unchanged

**Evidence:**
- The SBOM fetch code is not modified in the diff
- The new threshold filtering logic is placed after the successful SBOM fetch
- The function return type `Result<Json<AdvisorySummary>, AppError>` is preserved
- No changes were made to the error handling flow

This criterion is satisfied -- existing 404 behavior is preserved.
