# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task description specifies that the vulnerability count must be computed via a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery uses `COUNT(DISTINCT a.id)` to ensure advisories shared across multiple SBOMs are counted only once.

However, the PR diff shows that the vulnerability count is hardcoded to `0`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `TODO` comment explicitly acknowledges that the subquery has not been implemented. Since no subquery exists at all, the count does not reflect unique advisories -- it reflects nothing. The count is always 0 regardless of the actual number of advisories affecting the package.

This means:
- Packages with vulnerabilities will incorrectly show 0
- The deduplication requirement (COUNT DISTINCT) is not implemented
- The test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`, but with the hardcoded value of 0 this test would fail at runtime

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No subquery joining `sbom_package`, `sbom_advisory`, and `advisory` tables exists anywhere in the diff
- The test at `tests/api/package_vuln_count.rs` line 98 asserts `pkg.vulnerability_count == 2`, which would fail against the hardcoded 0
- The test at line 74 asserts `pkg.vulnerability_count == 3`, which would also fail against the hardcoded 0
