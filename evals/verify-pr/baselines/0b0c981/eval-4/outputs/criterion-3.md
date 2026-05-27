# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Criterion Text
> The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Evidence

In `modules/fundamental/src/package/service/mod.rs`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task requires a correlated subquery:
```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is **not implemented**. The vulnerability count is hardcoded to `0` with an explicit `TODO` comment acknowledging the missing implementation.

## Reasoning

The core feature of this task -- computing the actual vulnerability count by joining through the `sbom_package`, `sbom_advisory`, and `advisory` tables -- is entirely absent from the implementation. The `TODO` comment in the code confirms this is an intentional placeholder, not a completed implementation.

Because the count is hardcoded to zero:
- Packages with known vulnerabilities will incorrectly report zero.
- There is no deduplication logic because there is no counting logic at all.
- The test `test_package_with_vulnerabilities_has_count` (which expects `vulnerability_count == 3`) would fail.
- The test `test_vulnerability_count_deduplicates_across_sboms` (which expects `vulnerability_count == 2`) would fail.

This is a **blocking failure**. The criterion is not met.
