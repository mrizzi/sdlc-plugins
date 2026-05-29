## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

### Verdict: FAIL

### Analysis

The task description specifies that `vulnerability_count` should be computed using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery uses `COUNT(DISTINCT a.id)` to ensure that advisories shared across multiple SBOMs are not double-counted.

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows that the vulnerability count is **hardcoded to 0**:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly confirms that the subquery has not been implemented. The code does not query the `sbom_package`, `sbom_advisory`, or `advisory` tables at all. There is no deduplication logic because there is no counting logic whatsoever.

This is a critical functional gap. The field exists in the struct (Criterion 1 passes), but its value is never computed from actual data. Any package with vulnerabilities will incorrectly report a count of 0.

### Test Implications

The test file `tests/api/package_vuln_count.rs` includes:

1. `test_package_with_vulnerabilities_has_count` -- asserts `vulnerability_count == 3` for a package with 3 advisories. This test **will fail** because the hardcoded value is 0, not 3.
2. `test_vulnerability_count_deduplicates_across_sboms` -- asserts `vulnerability_count == 2` for a package with shared advisories. This test **will fail** because the hardcoded value is 0, not 2.
3. `test_package_without_vulnerabilities_has_zero_count` -- asserts `vulnerability_count == 0`. This test will pass trivially because the hardcoded value happens to match.

The fact that the tests are written to verify the correct behavior but the implementation does not support them confirms the criterion is not satisfied.

### Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No join queries to `sbom_package`, `sbom_advisory`, or `advisory` tables exist in the diff.
- The TODO comment explicitly marks the implementation as incomplete.
- Two of three test assertions will fail at runtime due to the hardcoded value.
