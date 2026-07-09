# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The implementation notes specify the required subquery:

```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is NOT implemented anywhere in the diff. The `// TODO: implement subquery` comment explicitly acknowledges that the work is incomplete.

## Reasoning

This criterion requires that the count reflects unique advisories and avoids double-counting across multiple SBOMs. The implementation does not compute any count at all -- it returns a hardcoded `0` for every package regardless of how many advisories exist. There is no subquery, no join through `sbom_package -> sbom_advisory -> advisory`, and no `COUNT(DISTINCT ...)` logic.

The TODO comment in the code is direct evidence that the developer acknowledged this work remains to be done. The vulnerability count is not computed from the database; it is a static placeholder value.

Additionally, the test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` and `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2`, but the implementation will always return 0. These tests would fail at runtime if properly executed, further confirming the implementation is incomplete.

This criterion unambiguously FAILS.
