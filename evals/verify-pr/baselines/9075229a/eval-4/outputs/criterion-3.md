# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that `vulnerability_count` be computed by counting unique (distinct) advisories linked to a package through the SBOM join tables. The task's Implementation Notes specify the required approach:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

However, the PR diff for `modules/fundamental/src/package/service/mod.rs` shows that the vulnerability count is hardcoded to zero with an explicit TODO comment:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

No subquery is implemented. The code does not join through `sbom_package`, `sbom_advisory`, or `advisory` tables at all. The field is simply set to the literal value `0` for every package, regardless of how many advisories actually affect it.

This means:
- A package with 5 unique advisories would incorrectly show `vulnerability_count: 0`
- The deduplication requirement (COUNT DISTINCT) is not implemented since no counting happens at all
- The test `test_package_with_vulnerabilities_has_count` asserts `pkg.vulnerability_count == 3` for a package seeded with 3 advisories, which would FAIL at runtime since the hardcoded value is always 0
- The test `test_vulnerability_count_deduplicates_across_sboms` asserts `pkg.vulnerability_count == 2` for a package with shared advisories, which would also FAIL at runtime

The TODO comment confirms this is an incomplete implementation, not a design decision.

## Evidence
- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No join through `sbom_package`, `sbom_advisory`, or `advisory` tables exists in the diff
- No `COUNT(DISTINCT ...)` or equivalent SeaORM query is present
- Tests that assert non-zero vulnerability counts (`test_package_with_vulnerabilities_has_count`, `test_vulnerability_count_deduplicates_across_sboms`) would fail at runtime
