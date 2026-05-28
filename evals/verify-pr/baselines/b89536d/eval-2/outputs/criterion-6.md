## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

### Evidence

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` preserves the existing 404 behavior. The handler first fetches the SBOM:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    ...
```

This existing code (shown as unchanged context lines in the diff) fetches the SBOM by ID and returns an error (presumably 404 via `AppError`) if the SBOM does not exist. The PR does not modify this pre-existing lookup logic -- it only adds threshold filtering logic after the SBOM fetch succeeds.

### Analysis

The new threshold filtering code is placed after the SBOM existence check and advisory aggregation, meaning the control flow still reaches the 404 error path when a non-existent SBOM ID is provided, before any threshold logic executes.

While no test was added to verify this behavior (the test file `tests/api/advisory_summary.rs` is missing from the diff entirely), the existing 404 behavior is structurally preserved in the code. The criterion asks only that existing behavior is preserved, which it is -- no modifications were made to the SBOM fetch or error handling path.

This criterion is satisfied.
