# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects unique (deduplicated) advisory counts, computed by joining through `sbom_package -> sbom_advisory -> advisory` tables using `COUNT(DISTINCT a.id)`.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the diff shows:

```diff
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` field is **hardcoded to `0`** with an explicit `// TODO: implement subquery` comment. The required correlated subquery described in the task's Implementation Notes:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

...has **not been implemented**. There is no database query computing the vulnerability count at all. The value is always zero, regardless of how many advisories exist for a package.

### Test Evidence

The test `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`. This test would **fail at runtime** because the hardcoded zero would never equal 3.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with shared advisories across SBOMs and asserts `vulnerability_count == 2`. This test would also **fail at runtime** for the same reason.

### Conclusion

This criterion is **not satisfied**. The core feature -- computing the actual vulnerability count from the database -- is missing entirely. The TODO comment confirms the implementation is intentionally incomplete. This is a blocking defect.
