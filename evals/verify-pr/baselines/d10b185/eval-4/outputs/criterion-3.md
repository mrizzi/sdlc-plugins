# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes the `vulnerability_count` to 0 for every package:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual vulnerability counting logic has NOT been implemented. The task's Implementation Notes specify a correlated subquery that should be used:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery uses `COUNT(DISTINCT a.id)` to ensure unique advisory counting across multiple SBOMs. The current implementation does none of this -- it returns 0 regardless of how many advisories exist for a given package.

Consequences of this defect:
1. Packages with known vulnerabilities will incorrectly report `vulnerability_count: 0`
2. The deduplication requirement (unique advisories across SBOMs) is entirely unaddressed
3. The test `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`, which would FAIL at runtime since the implementation always returns 0
4. The test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` for a package with shared advisories, which would also FAIL at runtime

This is a critical implementation gap -- the core business logic of the feature is missing.
