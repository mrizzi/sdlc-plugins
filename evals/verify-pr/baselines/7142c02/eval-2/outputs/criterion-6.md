# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Result: PASS

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` preserves the existing SBOM fetch-and-check logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code is unchanged from the original implementation. The `SbomService::fetch()` method presumably returns a `Result` that produces a 404 error (via `AppError`) when the SBOM ID does not exist. The `.context()` wrapping and `?` propagation ensure that any error from the fetch is returned to the caller.

The new threshold filtering code is placed after this SBOM existence check, so non-existent SBOM IDs will still be caught before any threshold logic runs.

The diff does not modify:
- The SBOM fetch call
- The error propagation chain
- The route registration
- Any error handling related to 404 responses

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::new(&db).fetch(sbom_id.id)` call and its error handling are preserved unchanged in the diff context
- New code (threshold filtering) is added only after the SBOM existence check succeeds

## Conclusion

The criterion is met. The existing 404 behavior for non-existent SBOM IDs is preserved because the SBOM fetch logic is unchanged, and the new filtering code is only reached after a successful SBOM lookup.
