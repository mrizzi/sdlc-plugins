# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The acceptance criterion requires that `vulnerability_count` reflects a computed count of unique advisories, with deduplication across multiple SBOMs. The task's Implementation Notes specify a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows the vulnerability count is **hardcoded to 0** with an explicit TODO comment:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The subquery to compute unique advisory counts has NOT been implemented. Every package will return `vulnerability_count: 0` regardless of whether it has vulnerabilities. This means:

1. Packages WITH vulnerabilities will incorrectly show 0
2. No deduplication logic exists because no counting logic exists at all
3. The `TODO` comment explicitly acknowledges the implementation is incomplete

The integration test `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`. This test would FAIL against the current implementation (which always returns 0), confirming the criterion is not met.

Similarly, `test_vulnerability_count_deduplicates_across_sboms` seeds a package with shared advisories across SBOMs and expects deduplication. This test would also FAIL since the count is hardcoded to 0 rather than 2.

This is a critical correctness gap -- the core feature described in the task summary is not implemented.

## Evidence
- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- Missing: Correlated subquery joining `sbom_package -> sbom_advisory -> advisory`
- Tests that would fail: `test_package_with_vulnerabilities_has_count` (expects 3, gets 0), `test_vulnerability_count_deduplicates_across_sboms` (expects 2, gets 0)
