# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that the `vulnerability_count` field accurately reflects the number of unique advisory records affecting a package, deduplicated across multiple SBOMs. The task description specifies this should be computed via a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id
```

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` is hardcoded to `0` for every package, regardless of how many advisories actually affect it. The TODO comment explicitly acknowledges that the subquery has not been implemented. This means:

1. Packages WITH vulnerabilities will incorrectly report `vulnerability_count: 0`
2. There is no deduplication logic because there is no counting logic at all
3. The `COUNT(DISTINCT a.id)` subquery specified in the implementation notes has not been written

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories across 3 SBOMs and asserts `vulnerability_count == 2`. This test would FAIL against the current implementation because the hardcoded value returns 0 instead of 2.

Similarly, `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`. This would also fail.

## Evidence
- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- No subquery, no JOIN, no COUNT(DISTINCT) logic exists in the diff
- Test assertions in `tests/api/package_vuln_count.rs` expect non-zero values (3 and 2) that the hardcoded 0 cannot satisfy
