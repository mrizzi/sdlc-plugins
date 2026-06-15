# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The acceptance criterion requires that the endpoint continues to return 404 for non-existent SBOM IDs, preserving the existing behavior.

The diff shows that the SBOM fetch logic is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

This code path exists both before and after the changes. The `SbomService::fetch()` call presumably returns an error (mapped to 404 via `AppError`) when the SBOM ID does not exist in the database. Since:

1. The fetch call is not modified in the diff
2. The error handling chain (using `.context()`) is preserved
3. The function signature still returns `Result<Json<AdvisorySummary>, AppError>`
4. The threshold filtering logic occurs AFTER the SBOM fetch, so it cannot interfere with the 404 path

The existing 404 behavior is preserved. When a non-existent SBOM ID is requested, the fetch will fail before the threshold filtering logic is ever reached.

However, it is worth noting that no test was written to verify this behavior (the required `tests/api/advisory_summary.rs` file is entirely missing from the diff), so while the code preserves the behavior, there is no new test coverage for this specific case.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::new(&db).fetch(sbom_id.id)` call is unchanged
- Error propagation via `AppError` is preserved
- Threshold filtering only executes after successful SBOM fetch
