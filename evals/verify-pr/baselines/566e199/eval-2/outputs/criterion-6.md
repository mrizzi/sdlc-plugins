## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

### Analysis

The diff preserves the existing 404 behavior for non-existent SBOM IDs. The handler code includes:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This pattern uses the `?` operator to propagate errors from the `SbomService::fetch` call. Based on the repo conventions (all handlers return `Result<T, AppError>` with `.context()` wrapping, and `AppError` implements `IntoResponse`), when an SBOM with the given ID is not found, the `fetch` method returns an error that gets converted to a 404 response via the `AppError` enum.

The diff does not modify this error-handling path -- it only adds the threshold filtering logic after the SBOM fetch succeeds. The new code is purely additive in the path after successful SBOM lookup.

### Evidence

- The `SbomService::fetch()` call and its `?` error propagation are unchanged in the diff
- The threshold filtering logic is applied only after the SBOM is successfully fetched
- The `AppError` enum in `common/src/error.rs` handles not-found errors per repo conventions

### Conclusion

This criterion is satisfied. The existing 404 behavior for non-existent SBOM IDs is preserved because the new threshold logic does not alter the SBOM fetch error-handling path.
