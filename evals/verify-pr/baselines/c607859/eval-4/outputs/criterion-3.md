# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that the `vulnerability_count` field be computed by counting distinct advisories, avoiding double-counting when the same advisory appears across multiple SBOMs linked to a package. The task description specifies the expected implementation:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

The PR diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+            vulnerability_count: 0, // TODO: implement subquery
```

No subquery is implemented. The vulnerability count is hardcoded to 0 for every package. The `// TODO: implement subquery` comment explicitly confirms the correlated subquery was never written. This means:

1. The count does NOT reflect unique advisories -- it reflects nothing, as it is always 0
2. The deduplication logic (`COUNT(DISTINCT ...)`) was never implemented
3. Packages with known vulnerabilities will incorrectly report 0

Additionally, the test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` expects `vulnerability_count` to equal 2 for a package with shared advisories across SBOMs. With the hardcoded value of 0, this test would fail at runtime, confirming the implementation is incomplete.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No JOIN or subquery logic exists anywhere in the diff
- The task-specified correlated subquery was never implemented
- Test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`, which would fail with the hardcoded 0
- Test `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`, which would also fail
