# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The task requires that `vulnerability_count` is computed by joining through `sbom_package` -> `sbom_advisory` -> `advisory` tables and counting distinct advisories. The implementation notes specify the subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the PR does not implement any subquery at all. The vulnerability count is hardcoded to `0`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Since no computation exists:
- There is no `COUNT(DISTINCT ...)` query
- There is no join through `sbom_package`, `sbom_advisory`, or `advisory` tables
- Deduplication across SBOMs cannot be verified because no counting occurs

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories shared across 3 SBOMs and expects `vulnerability_count: 2`. With the hardcoded implementation, it would return `0`, failing the assertion.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- no subquery, `vulnerability_count: 0` hardcoded
- The `// TODO: implement subquery` comment confirms the deduplication logic is not implemented
- Test `test_vulnerability_count_deduplicates_across_sboms` asserts `pkg.vulnerability_count == 2` but would receive `0`

## Result: FAIL
