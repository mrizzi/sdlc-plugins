# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved in the PR. The error handling path is unchanged.

### Code Under Review

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .context("Failed to aggregate advisory severities")?;
```

### Assessment

The SBOM fetch logic remains unchanged from the pre-PR code. The `SbomService::fetch()` call returns an error when the SBOM ID does not exist, and the `?` operator propagates it as an `AppError`. Per the repository conventions documented in the repo structure (`common/src/error.rs -- AppError enum, implements IntoResponse`), `AppError` maps to appropriate HTTP status codes including 404 for not-found entities.

The PR's changes are additive (threshold filtering) and do not modify the SBOM lookup or error handling path.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, the `SbomService::new(&db).fetch(sbom_id.id)` call is present in both pre- and post-PR code (unchanged in the diff)
- The `.context()` wrapping and `?` propagation pattern follows the existing project conventions per `common/src/error.rs`
- No modifications to the error handling path are visible in the diff
- The threshold filtering logic is positioned after the SBOM fetch, so it cannot affect the 404 behavior

### Note

While the existing 404 behavior is preserved, the task also required creating integration tests for this behavior in `tests/api/advisory_summary.rs`. That test file is entirely absent from the PR (tracked under Scope Containment).
