# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that the `vulnerability_count` field be computed by counting unique (deduplicated) advisories affecting each package. The task description specifies a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the PR diff shows that no such subquery was implemented. In `modules/fundamental/src/package/service/mod.rs`, the `vulnerability_count` is hardcoded to `0`:

```rust
+            vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly confirms the implementation is incomplete. The count does not reflect unique advisories because there is no query logic whatsoever -- the value is always zero regardless of the package's actual advisory associations.

This is the central defect in this PR: the core business logic that the task was designed to implement has not been written.

Additionally, the test `test_package_with_vulnerabilities_has_count` in `tests/api/package_vuln_count.rs` asserts that a package linked to 3 advisories returns `vulnerability_count: 3`, which would fail at runtime since the code always returns 0. Similarly, `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count: 2` for a package with shared advisories, which would also fail.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No JOIN query, no `COUNT(DISTINCT ...)`, no reference to `sbom_package`, `sbom_advisory`, or `advisory` tables anywhere in the diff.
- Tests `test_package_with_vulnerabilities_has_count` and `test_vulnerability_count_deduplicates_across_sboms` will fail at runtime due to the hardcoded zero.
