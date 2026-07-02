# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Evidence

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` with a TODO comment:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

No subquery exists. The task description specified that the count should be computed via:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
  JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
  JOIN advisory a ON sa.advisory_id = a.id
  WHERE sp.package_id = p.id
```

This subquery -- which uses `COUNT(DISTINCT a.id)` to deduplicate advisories across multiple SBOMs -- has not been implemented at all. The `vulnerability_count` is always 0 regardless of actual advisory data.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories shared across 3 SBOMs and expects `vulnerability_count == 2`. This test would fail at runtime because the hardcoded value returns 0.

## Conclusion

This criterion is not met. There is no deduplication logic because there is no query logic at all. The core feature -- computing vulnerability counts from the database -- is entirely unimplemented.
