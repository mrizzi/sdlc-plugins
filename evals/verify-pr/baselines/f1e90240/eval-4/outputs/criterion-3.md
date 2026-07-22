# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task requires that `vulnerability_count` be computed by joining through `sbom_package -> sbom_advisory -> advisory` tables, using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

The `COUNT(DISTINCT a.id)` is critical: it ensures that if the same advisory appears in multiple SBOMs for the same package, it is counted only once.

However, the PR implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this subquery at all:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The value is hardcoded to `0` with an explicit `// TODO: implement subquery` comment acknowledging the missing implementation. No database query is constructed to count advisories, let alone deduplicate them across SBOMs.

Furthermore, the test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` seeds a package with 2 unique advisories across 3 SBOMs and expects `vulnerability_count == 2`. This test would FAIL at runtime because the implementation always returns 0.

Similarly, `test_package_with_vulnerabilities_has_count` seeds 3 advisories and expects count 3, which would also FAIL at runtime.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Line:** `vulnerability_count: 0, // TODO: implement subquery`
- **Missing:** No subquery, no join through `sbom_package`/`sbom_advisory`/`advisory` tables, no `COUNT(DISTINCT)` logic
- **Test that would fail:** `test_vulnerability_count_deduplicates_across_sboms` expects count 2, gets 0
- **Test that would fail:** `test_package_with_vulnerabilities_has_count` expects count 3, gets 0

## Conclusion

This criterion is definitively NOT satisfied. The core feature -- computing the actual vulnerability count from database relationships -- is entirely unimplemented. The TODO comment in the code confirms this is a known gap. This is the primary defect in this PR: the feature's essential logic is missing.
