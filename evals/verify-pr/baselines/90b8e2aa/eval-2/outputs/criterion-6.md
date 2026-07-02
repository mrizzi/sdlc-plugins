# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing SBOM lookup logic is preserved unchanged in the diff. The handler still fetches the SBOM first and returns an error if it does not exist.

### Evidence from the Diff

The handler code shows (unchanged lines):

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

The `.fetch()` method is called before any threshold filtering occurs. Based on the existing codebase conventions documented in `common/src/error.rs`, the `SbomService::fetch()` method returns an `AppError` (which maps to 404) when the SBOM is not found. This code path is not modified by the PR.

### Context

The diff only adds the threshold parameter extraction and filtering logic after the SBOM fetch succeeds. The SBOM existence check is a prerequisite for the threshold filtering, so the 404 behavior for non-existent SBOMs is preserved.

### Note on Test Coverage

While the existing 404 behavior is preserved in the code, no integration test was added to verify this behavior for the advisory-summary endpoint specifically. The task's Test Requirements include "Test non-existent SBOM ID returns 404" but no test file was created. However, the criterion itself is about the endpoint behavior, which is preserved.

### Conclusion

The 404 behavior for non-existent SBOM IDs is maintained. The handler's control flow ensures the SBOM must exist before threshold filtering is applied.
