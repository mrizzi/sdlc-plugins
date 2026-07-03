# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The task requires that the existing 404 behavior for non-existent SBOM IDs is preserved after the changes.

### Code Inspection

In `modules/fundamental/src/advisory/endpoints/get.rs`, the handler still includes the SBOM fetch with error handling:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    ...
```

This code is present in both the pre-change and post-change versions of the handler (it appears in the diff context lines, not as added or removed lines). The existing error handling pattern that returns 404 when the SBOM is not found remains intact.

The changes in this PR only affect the code **after** the SBOM fetch succeeds -- adding the threshold filtering logic. The SBOM lookup and its 404 error path are untouched.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, lines 31-33 of the diff (context lines showing unchanged SBOM fetch)
- **Behavior:** The SBOM fetch logic is unchanged; the existing 404 behavior is preserved
- **Scope of change:** The PR modifications begin after `let summary = AdvisoryService::new(&db).aggregate_severities(sbom.id)`, leaving the SBOM existence check intact
- **Note:** While the existing 404 behavior is preserved, no integration test was added to verify this (the test file `tests/api/advisory_summary.rs` is entirely absent from the diff). However, this criterion asks about behavior preservation, not test coverage.
