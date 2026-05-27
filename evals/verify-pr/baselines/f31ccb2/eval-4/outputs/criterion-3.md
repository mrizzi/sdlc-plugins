# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Evidence

In the diff for `modules/fundamental/src/package/service/mod.rs`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is hardcoded to `0`. There is no subquery implemented at all -- no join through `sbom_package`, `sbom_advisory`, or `advisory` tables, and no `COUNT(DISTINCT ...)` logic. The implementation notes specified using:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

None of this logic exists in the diff. The deduplication requirement cannot be satisfied when no counting is performed.

## Test Coverage

The test `test_vulnerability_count_deduplicates_across_sboms` exists and asserts `vulnerability_count == 2`, but this test would fail at runtime since the implementation always returns 0.

## Assessment

This criterion is definitively not met. The core feature -- computing vulnerability counts -- is unimplemented.
