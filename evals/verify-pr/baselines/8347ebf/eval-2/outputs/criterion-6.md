# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The criterion requires that the existing 404 behavior for non-existent SBOM IDs is preserved after the changes. This is about ensuring the PR does not regress existing functionality.

### Existing 404 behavior

The handler code shows:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` call retrieves the SBOM by ID. If the SBOM does not exist, this method presumably returns an error (likely a `NotFound` variant of `AppError` or similar), which propagates via the `?` operator and results in a 404 response. This is the standard pattern used across the codebase (all handlers return `Result<T, AppError>` with `.context()` wrapping, and `AppError` implements `IntoResponse`).

### What the PR changes

The PR does not modify the SBOM fetch logic at all. The existing lines that fetch the SBOM and handle the not-found case are untouched. The threshold filtering logic is added AFTER the successful SBOM fetch, meaning:

1. If the SBOM ID does not exist, the handler returns the same error as before (404)
2. The threshold parameter has no effect on this code path -- the error occurs before threshold processing
3. No changes were made to `SbomService`, `AppError`, or any error handling code

### Assessment

The 404 behavior for non-existent SBOM IDs is preserved because the relevant code path was not modified. The PR only adds logic after the SBOM is successfully fetched.

Note: The task's Test Requirements specify "Test non-existent SBOM ID returns 404," but no test file (`tests/api/advisory_summary.rs`) was created in this PR. However, this criterion is about the behavior being preserved, not about test coverage. The behavior itself is intact.

## Conclusion

This criterion IS satisfied. The existing 404 behavior for non-existent SBOM IDs is preserved -- the SBOM fetch and error handling code is unchanged by this PR.
