# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The PR diff shows that the existing SBOM lookup logic is preserved unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code fetches the SBOM by its ID using `SbomService::fetch()`. If the SBOM does not exist, the `fetch` method would return an error (either a `None` result or an explicit not-found error). The `.context()` wrapping and `?` propagation ensure that errors are converted to `AppError` responses.

Based on the repository conventions documented in `common/src/error.rs`, `AppError` implements `IntoResponse` and maps not-found errors to 404 HTTP status codes. This existing error handling chain was not modified by the PR.

The threshold filtering logic is applied only after the SBOM is successfully fetched and the advisory severities are aggregated. The new code does not alter the control flow for the SBOM lookup or introduce any paths that could bypass the 404 response for non-existent SBOM IDs.

### Note on test coverage

While the existing 404 behavior is preserved in the code, the task required creating a test for this behavior in `tests/api/advisory_summary.rs`. No test file was created (see Criterion 1 / Scope Containment analysis). However, this criterion specifically asks about the endpoint behavior, not test coverage.

## Conclusion

This criterion is **satisfied**. The existing 404 behavior for non-existent SBOM IDs is preserved. The PR does not modify the SBOM lookup or error handling logic.
