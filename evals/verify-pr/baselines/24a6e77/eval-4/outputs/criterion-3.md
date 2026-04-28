# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task description specifies that the `vulnerability_count` should be computed by joining through `sbom_package -> sbom_advisory -> advisory` tables using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

The use of `COUNT(DISTINCT a.id)` is critical -- it ensures that if the same advisory appears across multiple SBOMs for the same package, it is counted only once.

However, the PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is **hardcoded to 0** with an explicit `// TODO: implement subquery` comment. No subquery has been implemented. No database join is performed. The count does not reflect unique advisories because the count does not reflect anything at all -- it is always zero regardless of the actual data.

This means:
- A package with 3 unique advisories would incorrectly show `vulnerability_count: 0`
- A package with advisories shared across multiple SBOMs would incorrectly show `vulnerability_count: 0`
- The deduplication requirement is entirely unaddressed

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` seeds a package with 2 shared advisories across 3 SBOMs and asserts `vulnerability_count == 2`. This test would FAIL at runtime because the hardcoded zero would return 0 instead of 2.

Similarly, `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`. This test would also FAIL at runtime (returning 0 instead of 3).

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- No subquery implementation exists anywhere in the PR diff
- The TODO comment explicitly acknowledges the implementation is missing
- Tests `test_package_with_vulnerabilities_has_count` and `test_vulnerability_count_deduplicates_across_sboms` would fail at runtime

## Conclusion

This criterion is definitively NOT satisfied. The core functionality of the feature -- computing actual vulnerability counts from the database -- has not been implemented. The hardcoded zero is a placeholder, not a working implementation.
