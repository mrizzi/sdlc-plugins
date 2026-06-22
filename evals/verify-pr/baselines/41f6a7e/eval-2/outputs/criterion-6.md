# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing SBOM fetch logic is preserved in the diff. The handler still calls:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This fetch-or-error pattern is unchanged from the pre-PR code. The SBOM is looked up before any threshold filtering logic runs. If the SBOM does not exist, the error propagation (via the `?` operator and `.context()`) returns the appropriate error response before the threshold filtering code is reached.

The threshold parameter handling is added after the SBOM fetch succeeds, so it cannot interfere with the 404 behavior for non-existent SBOM IDs.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::new(&db).fetch(sbom_id.id)` call and its error handling are in the diff's context lines (unchanged)
- The new threshold filtering logic runs only after a successful SBOM fetch
- No modifications to the SBOM fetch or error propagation paths
