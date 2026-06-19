# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The criterion requires that `vulnerability_count` reflects the actual number of unique advisories affecting a package, computed via a join through `sbom_package`, `sbom_advisory`, and `advisory` tables with deduplication (COUNT DISTINCT).

The implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this subquery. Instead, the vulnerability count is hardcoded to `0`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual count computation has not been implemented. There is no join, no subquery, no COUNT DISTINCT, and no interaction with the advisory-related tables at all.

The tests written for this criterion would FAIL at runtime:
- `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` but the implementation always returns `0`
- `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` but the implementation always returns `0`

This is a clear FAIL -- the core business logic of the feature is not implemented.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No subquery exists anywhere in the diff
- No references to `sbom_package`, `sbom_advisory`, or `advisory` tables in the diff
- Tests assert non-zero counts that would fail against the hardcoded `0`
