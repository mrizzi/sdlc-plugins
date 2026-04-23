# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The task's Implementation Notes specify a correlated subquery for computing the vulnerability count:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

The `COUNT(DISTINCT a.id)` is critical for ensuring unique advisories are counted (avoiding duplicates when the same advisory appears across multiple SBOMs).

However, examining the diff for `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is simply hardcoded to zero:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

There is no subquery, no database join, no `COUNT(DISTINCT ...)` logic anywhere in the diff. The `// TODO: implement subquery` comment explicitly confirms this has not been implemented.

Since no counting logic exists at all, the deduplication requirement cannot be met. The test `test_vulnerability_count_deduplicates_across_sboms` in the test file asserts `pkg.vulnerability_count == 2`, which would fail against the hardcoded `0` value.

This criterion FAILS because the subquery for computing unique advisory counts has not been implemented.
