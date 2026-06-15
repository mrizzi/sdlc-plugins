# Criterion 6: 404 for non-existent SBOM IDs preserved

**Criterion:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict:** PASS

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` preserves the existing SBOM lookup and 404 behavior. The relevant pre-existing code is visible in the diff context:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

The SBOM fetch occurs before any threshold filtering logic is applied. The `SbomService::fetch()` call uses the `?` operator with `.context()`, which propagates errors as `AppError`. According to the repository conventions (all handlers return `Result<T, AppError>` with `.context()` wrapping), if the SBOM ID does not exist, `SbomService::fetch()` returns an error that maps to a 404 response through the `AppError` error handling chain.

The threshold filtering code is added AFTER the SBOM fetch, so it does not interfere with the existing 404 behavior. The control flow is:
1. Fetch SBOM by ID (returns 404 if not found -- preserved)
2. Aggregate severities (unchanged)
3. Apply threshold filtering (new code, only reached if SBOM exists)
4. Return response

The existing 404 behavior is not modified by this change.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::fetch()` call and its error handling remain unchanged.
- The new threshold filtering code is appended after the existing SBOM lookup, not replacing it.
- No changes to error handling paths that would affect 404 responses.
