## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Analysis

The diff preserves the existing SBOM fetch logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

This code was present before the changes and is not modified by the diff. The `SbomService::fetch()` method presumably returns an error (likely mapped to 404 via `AppError`) when the SBOM ID does not exist. Since this behavior is in the existing code and the diff does not alter the fetch logic or error handling for non-existent SBOMs, the existing 404 behavior should be preserved.

The threshold filtering logic is added AFTER the SBOM fetch succeeds, so it does not interfere with the 404 path.

However, while the code path appears preserved, no test verifies this behavior (the test file `tests/api/advisory_summary.rs` is entirely absent from the diff).

## Verdict: PASS

The existing 404 behavior for non-existent SBOM IDs is preserved -- the SBOM fetch logic is unchanged, and the threshold filtering is applied only after a successful fetch.
