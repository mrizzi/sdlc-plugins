# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that the vulnerability count computation uses `COUNT(DISTINCT a.id)` or an equivalent deduplication mechanism to ensure that advisories shared across multiple SBOMs are not double-counted.

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` with a `// TODO: implement subquery` comment. No subquery has been implemented at all -- there is no join through `sbom_package`, `sbom_advisory`, and `advisory` tables, and therefore no `DISTINCT` deduplication logic.

Since the counting logic does not exist, it is impossible for the count to reflect unique advisories. The criterion is entirely unmet.

The test file `tests/api/package_vuln_count.rs` does include a test `test_vulnerability_count_deduplicates_across_sboms` that seeds a package with shared advisories across SBOMs and asserts `vulnerability_count == 2`, but this test would fail at runtime because the hardcoded value of 0 would never match the expected count of 2.

This criterion FAILS because the deduplication subquery has not been implemented.
