# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Result: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects unique advisories, meaning the count should use `COUNT(DISTINCT a.id)` through the join chain `sbom_package -> sbom_advisory -> advisory` as described in the Implementation Notes.

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is hardcoded to `0` for every package. The correlated subquery specified in the Implementation Notes was never implemented:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

Without this subquery, the field cannot reflect the actual count of unique advisories. Packages with known vulnerabilities will incorrectly show `vulnerability_count: 0`.

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` asserts that a package with 2 unique advisories across 3 SBOMs shows `vulnerability_count == 2`. This test would FAIL because the hardcoded value is always 0, not 2.

Similarly, `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` for a package linked to 3 advisories, which would also FAIL with the hardcoded 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0` is hardcoded
- The `// TODO: implement subquery` comment confirms the feature is not implemented
- The deduplication test would fail: expects 2, gets 0
- The basic count test would fail: expects 3, gets 0
