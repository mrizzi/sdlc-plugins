# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved in the PR. The handler retains the pre-existing fetch-and-check pattern:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    ...;
```

This code path (visible in the diff context lines at lines 31-33) existed before the PR and continues to work unchanged. The `SbomService::fetch` method returns an error when the SBOM ID does not exist, and the `?` operator propagates this as an `AppError`, which the Axum framework renders as a 404 response (based on the repository's error handling conventions described in `common/src/error.rs`).

The PR's changes (adding the `threshold` parameter and filtering logic) are applied only after the SBOM fetch succeeds, so they do not interfere with the 404 path.

However, while the existing behavior is preserved, the test file `tests/api/advisory_summary.rs` is missing from the diff, so the task's test requirement "Test non-existent SBOM ID returns 404" is not covered by a new test. This is a test coverage gap but does not affect the functional criterion itself, since the existing behavior is unchanged.

## Evidence

- `get.rs` lines 31-33: `SbomService::new(&db).fetch(sbom_id.id).await` -- unchanged fetch logic
- The threshold filtering at lines 41-58 executes only after successful SBOM fetch
- No changes to `common/src/error.rs` or `SbomService` in the diff
- Repository convention: `AppError` implements `IntoResponse` for error mapping (per `common/src/error.rs`)
