# Criterion 3

**Text:** The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Classification:** LEGITIMATE

## Evidence

The task description specifies that the vulnerability count should be computed via a correlated subquery:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` is:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The value is hardcoded to `0` with an explicit `// TODO: implement subquery` comment. No database query, no join through `sbom_package` / `sbom_advisory` / `advisory` tables, and no `COUNT(DISTINCT ...)` logic exists anywhere in the diff.

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` asserts `vulnerability_count == 2` for a package with shared advisories, which would FAIL at runtime because the value is always 0.

Similarly, `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`, which would also FAIL at runtime.

## Verdict: FAIL

The subquery to compute the vulnerability count has not been implemented. The value is hardcoded to 0, meaning this criterion is entirely unmet. The core business logic of this task is missing.
