# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Criterion:** The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Result: FAIL**

## Reasoning

The task's Implementation Notes specify that a correlated subquery should be used to compute the vulnerability count:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

The `COUNT(DISTINCT a.id)` is critical -- it ensures that the same advisory appearing across multiple SBOMs for the same package is only counted once.

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows that no subquery was implemented at all. Instead, the vulnerability count is hardcoded to `0`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges this is unfinished. The deduplication logic specified in the criterion (unique advisories only, no duplicates from multiple SBOMs) is completely absent from the implementation. This criterion is definitively not satisfied.
