# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that the `vulnerability_count` is hardcoded to `0`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task description specifies that the count should be computed using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is not implemented. The `vulnerability_count` field always returns `0` regardless of how many advisories are associated with a package. Therefore:

1. The count does NOT reflect unique advisories — it reflects nothing, always returning 0.
2. There is no deduplication logic because there is no counting logic at all.
3. The `// TODO: implement subquery` comment explicitly confirms the implementation is incomplete.

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` asserts `vulnerability_count == 2` for a package with shared advisories, which would FAIL against the current implementation (which always returns 0).

Similarly, `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`, which would also FAIL.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` — `vulnerability_count: 0` is hardcoded
- The TODO comment explicitly states "implement subquery"
- No JOIN logic for `sbom_package`, `sbom_advisory`, or `advisory` tables exists in the diff
- Tests that verify non-zero counts would fail against this implementation
