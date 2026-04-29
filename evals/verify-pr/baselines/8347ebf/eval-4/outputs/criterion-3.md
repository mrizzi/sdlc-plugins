# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that the `vulnerability_count` field be computed by counting unique advisories through the `sbom_package -> sbom_advisory -> advisory` join chain, using `COUNT(DISTINCT a.id)` to deduplicate advisories that appear across multiple SBOMs.

The implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this subquery. Instead, the vulnerability count is hardcoded to `0` for every package:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual computation is not implemented. This means:

1. Packages with known vulnerabilities will incorrectly show `vulnerability_count: 0`
2. There is no deduplication logic because there is no counting logic at all
3. The correlated subquery specified in the Implementation Notes (`SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`) is entirely absent

The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` for a package with 3 advisories, but the implementation would return `0`. Similarly, `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` for a deduplication scenario, but would receive `0`.

Both of these tests would fail at runtime, contradicting the stated "all CI checks pass" -- which suggests either the tests are not being run or the test infrastructure seeds no data. Regardless, the code does not implement the required behavior.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line 31: `vulnerability_count: 0, // TODO: implement subquery`
- Missing: correlated subquery joining `sbom_package`, `sbom_advisory`, and `advisory` tables
- Missing: `COUNT(DISTINCT a.id)` for deduplication
- Test expectations in `tests/api/package_vuln_count.rs` would fail:
  - `test_package_with_vulnerabilities_has_count`: expects 3, would get 0
  - `test_vulnerability_count_deduplicates_across_sboms`: expects 2, would get 0
