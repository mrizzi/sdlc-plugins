# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` correctly reflects the count of unique advisories affecting each package, computed by joining through `sbom_package`, `sbom_advisory`, and `advisory` tables, with deduplication across multiple SBOMs.

The actual implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this query. Instead, it hardcodes the value to `0`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the required correlated subquery has not been implemented. The task's Implementation Notes specify:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

This subquery is entirely absent from the diff. There is no join to `sbom_package`, `sbom_advisory`, or `advisory` tables. There is no `COUNT(DISTINCT ...)` operation. The vulnerability count is simply hardcoded to zero.

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` asserts `pkg.vulnerability_count == 2` for a package seeded with shared advisories across SBOMs. This test would FAIL with the hardcoded implementation since 0 != 2.

Similarly, `test_package_with_vulnerabilities_has_count` asserts `pkg.vulnerability_count == 3` for a package with 3 advisories. This test would also FAIL since 0 != 3.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- `vulnerability_count: 0` is hardcoded -- no subquery is implemented
- The `// TODO: implement subquery` comment confirms the implementation is incomplete
- The required correlated subquery from the Implementation Notes is entirely missing
- Tests that assert non-zero vulnerability counts would fail with this implementation
- This is a fundamental implementation gap, not a minor issue
