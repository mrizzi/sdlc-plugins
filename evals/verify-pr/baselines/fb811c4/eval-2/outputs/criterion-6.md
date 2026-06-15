# Criterion 6: 404 for Non-Existent SBOM IDs

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Analysis

The existing SBOM fetch logic is preserved unchanged in the diff. The handler first fetches the SBOM by ID before performing any advisory summary operations:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This fetch call is present in both the old and new versions of the code. If the SBOM does not exist, the `SbomService::fetch()` method returns an error that propagates through the `?` operator, resulting in an appropriate error response (404 Not Found) from the existing `AppError` handling.

The threshold filtering changes are applied only after a successful SBOM fetch, so non-existent SBOM IDs continue to produce 404 responses regardless of whether a threshold parameter is provided.

## Evidence

From the diff context lines (unchanged code):
```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

The SBOM fetch occurs before the new threshold filtering logic. The return type `Result<Json<AdvisorySummary>, AppError>` and the `.context()` error wrapping pattern are unchanged, preserving the existing 404 behavior.
