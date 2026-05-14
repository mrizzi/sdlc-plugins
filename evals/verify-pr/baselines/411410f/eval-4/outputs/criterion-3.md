# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that the vulnerability_count field accurately reflects the number of unique advisories affecting each package, deduplicating across multiple SBOMs. The Implementation Notes specify using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

However, the PR diff shows that the vulnerability count is hardcoded to 0:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

No subquery has been implemented. The `// TODO: implement subquery` comment explicitly acknowledges this is unfinished work. The count does not reflect unique advisories because no counting is performed at all -- the value is always 0 regardless of the actual advisory data.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with shared advisories across 2 SBOMs and expects `vulnerability_count: 2`, but the current implementation would return 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- The vulnerability_count is hardcoded to `0` -- no database query is performed
- The `// TODO: implement subquery` comment confirms this is intentionally incomplete
- The specified correlated subquery from the Implementation Notes has not been implemented
- Test `test_vulnerability_count_deduplicates_across_sboms` would fail with the current implementation (expects 2, gets 0)
- Test `test_package_with_vulnerabilities_has_count` would also fail (expects 3, gets 0)
