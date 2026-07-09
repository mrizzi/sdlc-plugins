## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Result: PASS**

### Analysis

The diff shows that the SBOM lookup logic preceding the advisory aggregation is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

The context lines in the diff (lines 31-37) show this existing code is preserved without modification. The `fetch()` call returns an `Option`, and the existing `.ok_or_else(|| AppError::NotFound(...))` pattern (visible from the unchanged handler structure and the `?` operator) converts a missing SBOM into a 404 response before the threshold filtering logic is reached.

### Evidence

1. The SBOM fetch block appears in the diff context (unchanged lines), confirming it was not modified.

2. The handler's return type remains `Result<Json<AdvisorySummary>, AppError>`, and `AppError` implements `IntoResponse` with appropriate HTTP status codes (including 404 for `NotFound`), as documented in the repo structure (`common/src/error.rs -- AppError enum, implements IntoResponse`).

3. The new threshold filtering code is placed after the SBOM lookup, so it only executes when a valid SBOM is found. The early-return pattern via `?` ensures non-existent SBOM IDs produce a 404 before any threshold logic runs.

### Caveat

While the existing 404 behavior is preserved in the endpoint code, no integration test was added to verify this behavior (the required test file `tests/api/advisory_summary.rs` is absent from the diff). The task's test requirements include "Test non-existent SBOM ID returns 404."
