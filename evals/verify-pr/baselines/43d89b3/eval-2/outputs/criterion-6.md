# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS (existing behavior preserved, but no test added)

## Analysis

The PR diff shows the existing SBOM lookup logic is preserved:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    ...
```

The existing `SbomService::fetch()` call with its error handling via `.context()` and the `AppError` return type would continue to return a 404 when the SBOM ID does not exist. This is existing behavior that was not modified by the PR.

The diff does not remove or alter the SBOM existence check. The new threshold filtering code executes only after the SBOM has been successfully fetched, so the 404 behavior for non-existent SBOMs is preserved.

However, while the existing behavior is preserved in the code, the task's **Test Requirements** section explicitly requires:
- "Test non-existent SBOM ID returns 404"

The PR diff does not include any test file (`tests/api/advisory_summary.rs` is entirely absent from the diff). This means while the runtime behavior is preserved, there is no test validating it, which the task specifically requires.

**Result:** PASS for the acceptance criterion itself (existing behavior preserved), but the associated test requirement is not met (no test file was created).
