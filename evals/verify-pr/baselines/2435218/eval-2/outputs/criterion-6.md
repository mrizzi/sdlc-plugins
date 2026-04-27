# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` shows the handler function includes this pre-existing logic for SBOM lookup:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    ...
```

This code path existed before the PR changes and is preserved in the diff. The `SbomService::fetch()` method returns an error when the SBOM ID is not found, and the existing error handling (via `AppError` and `.context()`) maps this to a 404 response.

The PR does not modify the SBOM lookup logic or the error handling path. The new threshold filtering code is added AFTER the SBOM lookup succeeds, so the 404 behavior for non-existent SBOMs is preserved.

The structure of the handler remains:
1. Fetch the SBOM by ID (returns 404 if not found -- unchanged)
2. Aggregate severity counts (unchanged)
3. Apply threshold filtering (new code, only reached if SBOM exists)
4. Return the response

Since the 404 behavior depends on the SBOM fetch step which is unmodified, the existing behavior is preserved.

**Note:** While the existing behavior is preserved in the handler code, the task also requires a test for this case (`Test non-existent SBOM ID returns 404`), which was not created. The test requirement failure is separate from this acceptance criterion about the runtime behavior.

**Conclusion:** This criterion is satisfied. The existing 404 behavior for non-existent SBOM IDs is preserved by the PR changes.
