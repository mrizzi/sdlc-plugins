## Criterion 6

**Text:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**What I checked:** The SBOM fetch logic in `modules/fundamental/src/advisory/endpoints/get.rs` to confirm the existing 404 behavior was not altered.

**Code evidence:**

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ... (existing code, not modified in this diff)
```

The SBOM fetch call and its error handling are unchanged in the diff. The diff only adds the `SummaryParams` extraction and the threshold filtering logic after the SBOM has been successfully fetched. If the SBOM does not exist, the existing error handling (presumably returning a 404 via `AppError`) remains intact.

The new code is appended after the existing SBOM fetch and advisory aggregation, so the 404 behavior for non-existent SBOM IDs is preserved.

**Verdict: PASS**

The existing 404 behavior for non-existent SBOM IDs is preserved. The diff does not modify the SBOM fetch or its error handling.
