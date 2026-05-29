# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task description specifies that the `vulnerability_count` should be computed via a correlated subquery joining through `sbom_package`, `sbom_advisory`, and `advisory` tables, using `COUNT(DISTINCT a.id)` to ensure unique advisory counts.

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` is hardcoded to `0` with a `// TODO: implement subquery` comment. No subquery was implemented. No join through `sbom_package`, `sbom_advisory`, or `advisory` tables is present. There is no `COUNT(DISTINCT ...)` logic anywhere in the diff.

This means:
1. Packages with actual vulnerabilities will incorrectly report 0 vulnerabilities.
2. There is no deduplication logic because there is no counting logic at all.
3. The implementation is fundamentally incomplete for this criterion.

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` asserts `vulnerability_count == 2` for a package seeded with shared advisories. With the hardcoded zero, this test would FAIL at runtime.

Similarly, `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`, which would also FAIL with the hardcoded zero.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- No subquery implementation exists anywhere in the diff.
- The TODO comment explicitly acknowledges the implementation is missing.
- Tests assert non-zero counts (3 and 2) that would fail against the hardcoded zero.

## Conclusion

This criterion is NOT satisfied. The vulnerability count is hardcoded to zero; no actual counting or deduplication logic has been implemented. This is a critical defect -- the core feature requested by the task is not functional.
