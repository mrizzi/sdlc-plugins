## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

### Reasoning

The existing 404 behavior for non-existent SBOM IDs is preserved by the code. The handler still calls:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` method returns an error (propagated via `?`) when the SBOM ID does not exist, which would result in a 404 response through the `AppError` handling. The new threshold filtering code is only reached after the SBOM is successfully fetched, so the 404 path is not affected.

The diff does not modify the `SbomService::fetch()` method or the error handling path. The `?` operator continues to propagate the not-found error before any threshold logic is reached.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the `SbomService::fetch()` call with `?` propagation is unchanged
- The threshold filtering logic appears after the SBOM fetch, so it cannot interfere with the 404 path
- The `AppError` type (from `common/src/error.rs`) handles the 404 response mapping, and this is not modified
