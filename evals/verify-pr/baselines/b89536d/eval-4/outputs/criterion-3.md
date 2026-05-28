# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task description specifies that the vulnerability count should be computed using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this subquery. Instead, the vulnerability count is hardcoded to zero:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the implementation is incomplete. The count does not reflect unique advisories because no advisory counting logic exists at all. Every package will return `vulnerability_count: 0` regardless of how many advisories are associated with it.

This means:
- Packages with vulnerabilities will incorrectly show 0
- The deduplication logic (COUNT DISTINCT) is entirely absent
- The test `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` for a package with 3 advisories, which would fail at runtime since the hardcoded value is 0
- The test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`, which would also fail at runtime

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No join through `sbom_package`, `sbom_advisory`, or `advisory` tables exists in the diff
- No `COUNT(DISTINCT ...)` or equivalent SeaORM query appears anywhere in the changes
- The TODO comment is explicit proof the implementation is incomplete
