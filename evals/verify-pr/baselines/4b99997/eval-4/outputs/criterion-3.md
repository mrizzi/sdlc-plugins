# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Result: FAIL

## Analysis

The task description specifies that the vulnerability count should be computed using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

This query uses `COUNT(DISTINCT a.id)` to ensure unique advisories are counted even when a package appears in multiple SBOMs.

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` is:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

There is **no subquery at all**. The vulnerability count is hardcoded to `0` with an explicit `TODO` comment indicating the subquery has not been implemented. Without any database query, there is no deduplication logic, no join through the `sbom_package`, `sbom_advisory`, and `advisory` tables, and no `DISTINCT` clause.

This criterion is entirely unmet. The core computation that this feature is supposed to deliver does not exist in the PR.
