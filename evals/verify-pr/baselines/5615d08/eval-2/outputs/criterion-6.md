# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

## Reasoning

The PR diff shows that the existing 404 behavior for non-existent SBOM IDs is preserved. The handler code includes:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` call retrieves the SBOM by ID. If the SBOM does not exist, this call would return an error (likely a "not found" result), which is propagated via the `?` operator to `AppError` and would result in a 404 response. This behavior exists in the original code (shown in the diff context lines without `+` prefix) and is not modified by the PR.

The threshold filtering logic is applied only after the SBOM has been successfully fetched, so a non-existent SBOM ID will still trigger the 404 response before any threshold logic executes.

This criterion specifies "existing behavior preserved," meaning the PR should not break the existing 404 handling. Since the SBOM fetch code is unchanged, this behavior is preserved.

Note: While the existing behavior is preserved in the code, the task also requires a test for this case (`Test non-existent SBOM ID returns 404`), and no test file was created. The absence of the test is tracked under the test requirements, not this acceptance criterion.

## Evidence

- `SbomService::new(&db).fetch(sbom_id.id).await.context(...)?.` -- unchanged from original, propagates not-found errors
- Threshold filtering occurs after SBOM fetch, so 404 is returned before filtering logic runs
- No modifications to the SBOM fetch or error handling flow
