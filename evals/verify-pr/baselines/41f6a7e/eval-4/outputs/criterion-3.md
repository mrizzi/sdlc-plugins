# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The task requires the `vulnerability_count` to be computed via a correlated subquery that joins through `sbom_package` -> `sbom_advisory` -> `advisory` tables, using `COUNT(DISTINCT a.id)` to ensure advisories shared across multiple SBOMs are not double-counted.

The specified subquery from the Implementation Notes is:

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
- There is no `COUNT(DISTINCT ...)` query anywhere in the diff
- There is no join through `sbom_package`, `sbom_advisory`, or `advisory` tables
- Deduplication across SBOMs cannot occur because no counting takes place

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories shared across 3 SBOMs and expects `vulnerability_count: 2`. With the hardcoded implementation, it would return `0`, failing the assertion.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery` with no subquery implemented
- The `// TODO: implement subquery` comment explicitly confirms the deduplication logic is absent
- Test `test_vulnerability_count_deduplicates_across_sboms` would fail at runtime (asserts `pkg.vulnerability_count == 2` but receives `0`)
- No references to `sbom_package`, `sbom_advisory`, or `advisory` tables appear in the diff
