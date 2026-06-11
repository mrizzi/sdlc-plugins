# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The PR preserves the existing 404 behavior for non-existent SBOM IDs. The handler code fetches the SBOM before performing any threshold filtering:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This existing pattern (present before the PR changes) uses the `?` operator to propagate errors. Based on the repository conventions documented in repo-backend.md, the codebase uses `AppError` which implements `IntoResponse`, and the `SbomService::fetch` method would return an appropriate error (mapping to 404) when the SBOM ID does not exist. The PR does not modify this fetch-and-validate flow.

The threshold filtering logic is applied only after the SBOM is successfully fetched, so non-existent SBOM IDs are rejected before any threshold processing occurs.

While no new test was added for this behavior (the test file `tests/api/advisory_summary.rs` is missing from the diff entirely), the existing behavior itself is preserved in the handler code.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The SBOM fetch with error propagation (`?`) precedes the threshold filtering code.
- No modifications were made to the SBOM lookup or error handling path.
- The PR adds threshold handling after the existing fetch, preserving the 404 behavior.
