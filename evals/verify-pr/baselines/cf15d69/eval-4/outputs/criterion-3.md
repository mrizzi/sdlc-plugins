# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that the `vulnerability_count` field contains a computed count of unique (deduplicated) vulnerability advisories associated with each package. The task description specifies that this count should be computed via a correlated subquery joining through `sbom_package`, `sbom_advisory`, and `advisory` tables with `COUNT(DISTINCT a.id)`.

The PR diff in `modules/fundamental/src/package/service/mod.rs` reveals that no such subquery exists. Instead, the value is hardcoded:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the core logic for this feature is not implemented. The count does not reflect any advisories at all -- it is always zero regardless of the actual vulnerability data in the database.

This has cascading test failures:
- `test_package_with_vulnerabilities_has_count` asserts `pkg.vulnerability_count == 3` but will get `0` -- FAIL at runtime
- `test_vulnerability_count_deduplicates_across_sboms` asserts `pkg.vulnerability_count == 2` but will get `0` -- FAIL at runtime

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Code:** `vulnerability_count: 0, // TODO: implement subquery`
- **Missing implementation:** No `SELECT COUNT(DISTINCT a.id)` subquery, no join to `sbom_package`/`sbom_advisory`/`advisory` tables, no deduplication logic of any kind
- **Test failures:** 2 of 3 tests will fail at runtime because they assert non-zero vulnerability counts against a hardcoded zero value
