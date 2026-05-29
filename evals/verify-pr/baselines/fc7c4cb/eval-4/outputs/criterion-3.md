# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The criterion requires that the vulnerability count reflects unique advisories, avoiding double-counting when the same advisory appears across multiple SBOMs for the same package. The task description specifies using a correlated subquery with `COUNT(DISTINCT a.id)` joining through `sbom_package -> sbom_advisory -> advisory`.

### Evidence from the diff

In `modules/fundamental/src/package/service/mod.rs`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

There is no subquery implementation at all. The vulnerability count is hardcoded to `0` for every package. The `TODO` comment explicitly states the subquery has not been implemented.

### What was expected

Per the task's implementation notes, the expected implementation was:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

This subquery, or its SeaORM equivalent, is entirely absent from the diff. Without it:

- Packages with vulnerabilities will incorrectly report `0`
- The deduplication requirement (using `DISTINCT`) is not addressed
- The join chain through `sbom_package -> sbom_advisory -> advisory` does not exist

### Test implication

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 shared advisories across 3 SBOMs and asserts `vulnerability_count == 2`. With the hardcoded value of 0, this test would fail at runtime.

Similarly, `test_package_with_vulnerabilities_has_count` seeds 3 advisories and asserts `vulnerability_count == 3`, which would also fail with the hardcoded 0.

This criterion is clearly not met.
