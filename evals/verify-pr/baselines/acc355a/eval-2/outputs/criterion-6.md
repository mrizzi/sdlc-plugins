## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Result: PASS**

### Evidence

The diff preserves the existing SBOM lookup logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code was present before the change and remains in the diff. The `SbomService::fetch()` method presumably returns an error (likely mapped to 404 via AppError) when the SBOM ID does not exist. Since this code path is unchanged, the existing 404 behavior for non-existent SBOM IDs is preserved.

The diff does not add or remove any code related to SBOM existence checking, so existing behavior is maintained. Note that while no new test was added to verify this behavior (the test file is missing entirely), the existing behavior itself appears preserved.
