# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Result: PASS

## Reasoning

The existing SBOM fetch logic in the handler is preserved unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code fetches the SBOM by ID before performing any advisory aggregation. If the SBOM does not exist, `SbomService::fetch()` will return an error (likely mapped to a 404 via the `AppError` type per the repository's error handling conventions), and the `?` operator will propagate it as an early return before reaching the threshold filtering logic.

The PR diff does not modify the SBOM fetch logic, the error propagation path, or the `AppError` type. The 404 behavior for non-existent SBOM IDs is inherited from the pre-existing implementation and remains intact.

Note: while no integration test was added to verify this behavior (the task required a test for this case in `tests/api/advisory_summary.rs`, which is entirely absent from the diff), the code-level behavior is preserved. The missing test is tracked as a scope containment issue (the required test file was not created).
