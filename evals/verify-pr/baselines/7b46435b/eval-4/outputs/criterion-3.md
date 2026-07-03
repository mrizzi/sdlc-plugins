# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that the `vulnerability_count` field reflects the actual number of unique vulnerability advisories affecting each package, computed by joining through `sbom_package`, `sbom_advisory`, and `advisory` tables, with deduplication to avoid double-counting advisories that appear across multiple SBOMs.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the implementation hardcodes the vulnerability count to zero:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the required subquery has not been implemented. The task's Implementation Notes specified the following subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is entirely absent from the implementation. The `vulnerability_count` is always `0` regardless of how many advisories are associated with the package.

### Test Contradiction

The tests in `tests/api/package_vuln_count.rs` expect non-zero counts for packages with vulnerabilities:

- `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` for a package seeded with 3 advisories
- `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` for a package seeded with 2 unique advisories across 3 SBOMs

Both of these tests would fail at runtime because the implementation always returns 0. The fact that CI is reported as passing suggests these tests may not be wired into the test harness, or the eval fixture reports CI as passing regardless.

### Conclusion

This criterion is NOT satisfied. The implementation is incomplete -- it provides a stub (`vulnerability_count: 0`) rather than the actual computed count. The core feature described in the task (computing vulnerability counts via database joins with deduplication) has not been implemented.
