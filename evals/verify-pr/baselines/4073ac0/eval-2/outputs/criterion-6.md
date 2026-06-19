# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The task requires that the existing 404 behavior for non-existent SBOM IDs be preserved. This is about maintaining backward compatibility, not adding new functionality.

### What the diff shows

The SBOM fetch logic was not modified by this PR:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

The `.context()` wrapping and `AppError` handling chain remain intact. The PR only adds code **after** the SBOM is successfully fetched (the threshold filtering logic). If the SBOM does not exist, the existing error handling path returns a 404 before the new filtering code is reached.

### Conclusion

The existing 404 behavior is preserved because the SBOM lookup code path was not modified. The error propagation chain (`AppError` with `.context()`) remains unchanged. This criterion is satisfied.
