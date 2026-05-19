## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Verdict: PASS

### Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` shows the existing 404 handling is preserved. The handler still fetches the SBOM first:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    ...
```

This existing code path (visible in the diff context lines, not modified by this PR) would return a 404 via `AppError` when the SBOM ID does not exist, as this is the pre-existing behavior described in the task.

The diff does not modify or remove any of the SBOM existence checking logic. The new code is added after the SBOM fetch succeeds, in the advisory severity aggregation section. The flow is:

1. Fetch SBOM by ID (existing) -- returns 404 if not found
2. Aggregate advisory severities (existing)
3. Apply threshold filtering (new)
4. Return response (modified to return filtered result)

The new threshold filtering code is only reached after the SBOM has been successfully fetched, so the 404 behavior for non-existent SBOM IDs is preserved.

**Evidence from the diff:**
- The SBOM fetch code appears in the unchanged context lines of the diff
- No lines related to SBOM fetching or error handling were removed (no `-` prefixed lines in that section)
- The new filtering logic is added after the SBOM fetch, not replacing it

This criterion is satisfied -- the existing 404 behavior is preserved.
