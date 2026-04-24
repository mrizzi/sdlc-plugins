# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Status: FAIL

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded to zero:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task description specifies that a correlated subquery should be used to count distinct advisories:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id
```

No such subquery is implemented. The `vulnerability_count` is always `0` regardless of actual advisory data. This means:
- Packages WITH vulnerabilities will incorrectly show a count of 0.
- There is no deduplication logic because there is no counting logic at all.

The TODO comment explicitly acknowledges this is unfinished. This criterion **fails**.
