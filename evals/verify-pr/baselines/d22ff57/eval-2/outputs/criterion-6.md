# Criterion 6

**Text**: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Evidence from diff**:

The diff preserves the existing SBOM fetch logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ... (existing logic that returns 404 via AppError when SBOM not found)
```

This code is unchanged in the diff. The existing 404 behavior for non-existent SBOM IDs is not modified or removed by this PR. The new filtering logic is applied after the SBOM fetch, so the 404 path remains intact.

**Verdict**: PASS
