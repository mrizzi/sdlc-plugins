# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

## Criterion

Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved).

## Verdict: PASS

## Reasoning

The criterion specifies that existing 404 behavior for non-existent SBOM IDs must be preserved. This is about backward compatibility of existing error handling, not a new feature.

The diff shows the existing SBOM lookup code is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The `SbomService::fetch()` call with the `?` operator propagates errors via `AppError`. Based on the repository conventions documented in `repo-backend.md`, the `AppError` enum implements `IntoResponse` (in `common/src/error.rs`), and `fetch()` would return an error (mapped to 404) when the SBOM ID does not exist.

The PR diff does not modify this lookup logic -- it only adds new code after the existing SBOM fetch and advisory aggregation. The 404 behavior for non-existent SBOM IDs is preserved.

**Note:** While the existing 404 behavior is preserved, the task also requires a test for this case (`Test non-existent SBOM ID returns 404`) in the Test Requirements section. No test file was created at all (see the missing test file gap), so this behavior is untested by the PR even though it is functionally preserved.

## Evidence

- The SBOM fetch code in the handler is unchanged between the base and PR versions
- The `SbomService::fetch()` call and its error propagation are not modified by the diff
- The `AppError` type (imported at line 4) handles 404 responses per repository convention
