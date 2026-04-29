# Criterion 6: 404 for non-existent SBOM IDs

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Analysis

The PR diff shows the handler code that fetches the SBOM:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

This code was present before the PR changes (it appears in the unchanged context lines of the diff). The existing `SbomService::fetch()` method presumably returns an error or `None` when the SBOM ID does not exist, which would be converted to a 404 response through the existing `AppError` handling.

The PR changes do not modify this SBOM fetching logic. The `fetch` call and its error handling remain untouched. The changes only add threshold filtering logic after the SBOM has been successfully fetched and the advisory severities have been aggregated.

Since the existing 404 behavior was not modified by this PR, the behavior is preserved.

However, it should be noted that while the existing behavior is preserved in the code, no integration test was added to verify 404 behavior for non-existent SBOM IDs (the task's Test Requirements explicitly require this). The absence of tests is a separate concern but does not affect whether the code behavior is correct.

**Conclusion:** The existing 404 behavior for non-existent SBOM IDs is preserved because the PR did not modify the SBOM fetching and error handling logic. This criterion IS met (from a code behavior perspective).
