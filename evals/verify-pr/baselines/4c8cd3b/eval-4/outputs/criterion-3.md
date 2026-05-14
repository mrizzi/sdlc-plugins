# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects the count of unique advisories affecting a package, computed via a correlated subquery joining through `sbom_package`, `sbom_advisory`, and `advisory` tables, with deduplication using `COUNT(DISTINCT a.id)`.

### Evidence from PR diff

In `modules/fundamental/src/package/service/mod.rs`, the implementation shows:

```diff
+                vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is hardcoded to `0` for every package. There is no subquery implementation. The `// TODO: implement subquery` comment explicitly acknowledges the missing implementation.

The Implementation Notes in the task description specified:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

This subquery was never implemented. The count does not reflect unique advisories — it reflects nothing, as it is always zero regardless of actual data.

### Test Evidence

The test `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`. This test would FAIL with the current implementation since the hardcoded value is always `0`.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds shared advisories across SBOMs and asserts `vulnerability_count == 2`. This test would also FAIL with the current implementation.

### Conclusion

This criterion is not satisfied. The core feature — computing the actual vulnerability count via a database subquery — is missing entirely. The implementation is a stub with a TODO comment, meaning the primary business logic of this task has not been implemented.
