# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Result: PASS

## Reasoning

The diff preserves the existing SBOM lookup behavior. The handler code still calls:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

This fetch call, which exists in the original code, returns an error when the SBOM ID is not found. The diff does not modify this lookup logic -- it only adds threshold filtering after the SBOM has been successfully fetched and advisory severities have been aggregated.

The 404 behavior for non-existent SBOM IDs is an existing capability that is preserved by the changes in this PR. The new threshold filtering code executes only after the SBOM lookup succeeds, so it cannot interfere with the 404 response path.

Note: While the existing behavior is preserved, no integration test for this scenario was added (the task's Test Requirements specified one), though that is a separate concern from whether the behavior itself works.
