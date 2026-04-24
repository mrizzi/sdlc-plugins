## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

**Criterion**: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved).

**Result**: PASS

**Reasoning**:

The diff shows the existing SBOM lookup logic is preserved:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

The pre-existing handler already fetched the SBOM and presumably returned a 404 (via `AppError`) if the SBOM was not found. The diff does not modify this lookup or error-handling path. The new threshold filtering logic occurs after the SBOM fetch, so it does not interfere with the 404 behavior.

However, the task also specifies under "Test Requirements" that there should be a test for non-existent SBOM IDs returning 404. No test file (`tests/api/advisory_summary.rs`) was created in this diff, so this behavior is untested even though it is preserved in the code.

**Verdict**: PASS -- The existing 404 behavior for non-existent SBOM IDs is preserved in the implementation, though it lacks test coverage (addressed separately under test requirements).
