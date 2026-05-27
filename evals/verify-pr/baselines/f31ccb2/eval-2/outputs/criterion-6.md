## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

### Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved. The diff does not modify the SBOM fetch logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

This code path was present before the change and remains unchanged. If the SBOM ID does not exist, the `fetch` call will return an error (or `None`), which the existing error-handling chain converts to a 404 response via `AppError`.

The threshold filtering logic is applied only after the SBOM has been successfully fetched and the advisory aggregation has completed, so it does not interfere with the 404 path.

### Evidence

The diff shows the SBOM fetch block is untouched (context lines only, no `+` or `-` markers on those lines). The new filtering code is inserted after the `aggregate_severities` call, which itself only runs after a successful SBOM fetch.
