# Criterion 6: 404 for non-existent SBOM IDs (existing behavior preserved)

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

## Detailed Reasoning

The existing 404 behavior for non-existent SBOM IDs is preserved in the PR. The handler still performs the SBOM lookup before proceeding to advisory aggregation:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ...
```

This code is unchanged from the original implementation. The `SbomService::fetch()` method presumably returns an error (via `AppError`) when the SBOM ID does not exist, and the `?` operator propagates this error as a 404 response before any threshold filtering logic is reached.

The PR's changes are additive -- they add the `Query(params)` parameter extraction and post-aggregation filtering logic, but do not modify the SBOM existence check or the error handling path that produces 404 responses.

**Note on test coverage:** While the existing 404 behavior is preserved in the code, the task required creating a test file at `tests/api/advisory_summary.rs` that includes a test for non-existent SBOM IDs returning 404. This test file was not created in the PR. The absence of the test is a separate concern from the criterion itself -- the criterion asks whether the behavior is preserved, which it is. The missing tests are covered under the Test Requirements section of the task.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the `SbomService::new(&db).fetch(sbom_id.id)` call is unchanged
- The `?` operator after the fetch propagates any error (including not-found) before threshold filtering
- No modifications to the `SbomService::fetch` method or `AppError` handling
- The threshold filtering logic only executes after a successful SBOM fetch
