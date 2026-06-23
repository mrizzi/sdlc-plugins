# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The acceptance criterion requires that the endpoint returns 404 for non-existent SBOM IDs, preserving the existing behavior.

### Code Analysis

In `modules/fundamental/src/advisory/endpoints/get.rs`, the handler fetches the SBOM before performing any filtering:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ... error handling ...
```

This fetch call and its error handling exist in the pre-change code and remain unchanged in the diff. The PR only modifies the code path that executes after a successful SBOM fetch -- adding the threshold parameter extraction and filtering logic. The SBOM existence check happens before any of the new threshold-related code.

### Evidence from the Diff

The diff shows that the SBOM fetch and validation code (lines before the `let summary = ...` call) are untouched context lines, not modified by this PR. The only changes are:
1. Adding the `SummaryParams` struct and `Query(params)` parameter
2. Adding filtering logic after the `aggregate_severities` call
3. Wrapping the response in the filtering match

None of these changes affect the SBOM existence check or the 404 response path.

### Note on Testing

While the existing 404 behavior is preserved in the code, no integration test was added to verify this behavior (the task required creating `tests/api/advisory_summary.rs` which includes a test for non-existent SBOM IDs). However, this criterion is specifically about the endpoint behavior being preserved, not about test coverage, so the behavior criterion itself is satisfied.

### Conclusion

The existing 404 behavior for non-existent SBOM IDs is preserved. The PR's changes are scoped to the post-fetch logic and do not interfere with the SBOM existence check. This criterion is satisfied.
