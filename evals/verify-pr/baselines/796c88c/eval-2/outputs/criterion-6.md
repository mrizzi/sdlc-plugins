# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## What was checked

Inspected the PR diff for changes to the SBOM lookup logic that might affect the existing 404 behavior.

## Evidence

The existing handler code (visible in the diff context) includes:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

The diff does not modify the SBOM fetch logic. The `.fetch()` call and its error handling (using `.context()` wrapping with `AppError`) remain unchanged. The PR only adds code AFTER the SBOM fetch to filter the advisory summary by threshold.

Since the existing 404 behavior for non-existent SBOM IDs is implemented upstream of the new code (in the `SbomService::fetch` method which returns an error for missing SBOMs), and the PR does not modify that path, the existing behavior is preserved.

However, no test was added to verify this behavior is preserved (the test file `tests/api/advisory_summary.rs` is entirely missing from the diff). The acceptance criterion asks that the behavior be "preserved" which it is -- the existing code path is untouched.

## Verdict: PASS

The existing 404 behavior for non-existent SBOM IDs is preserved. The PR does not modify the SBOM fetch logic, so the existing error handling remains intact. Note: while no new test was added for this behavior, the criterion asks about behavior preservation, which is satisfied by the unchanged code path.
