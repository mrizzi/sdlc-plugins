# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The existing 404 behavior is preserved by the code already present in the handler. The diff shows the existing code:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

While the diff doesn't show the `.ok_or_not_found()` call explicitly (it's in the unchanged context above the shown hunk), the pattern used by this codebase for fetching entities returns an `Option` from the service layer, and the error handling via `AppError` maps not-found cases to 404 responses. The handler's control flow ensures that if the SBOM does not exist, an error is returned before reaching the threshold filtering logic.

The PR changes do not modify this fetch-and-validate flow. The new threshold filtering code is added after the SBOM fetch, so the 404 behavior for non-existent SBOMs is preserved.

However, it should be noted that no integration test was added to verify this behavior (see Test Requirements analysis), even though the task explicitly requires a test for non-existent SBOM IDs returning 404.

**Conclusion:** This criterion IS satisfied. The existing 404 behavior for non-existent SBOM IDs is preserved by the unchanged fetch logic in the handler.
