# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Result: FAIL

## Analysis

This criterion requires that the vulnerability count correctly deduplicates advisories that may appear across multiple SBOMs for the same package. The task's Implementation Notes specify using `COUNT(DISTINCT a.id)` in the subquery to ensure uniqueness.

However, the PR diff shows that in `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

No subquery has been implemented at all. There is no database query that joins through `sbom_package`, `sbom_advisory`, and `advisory` tables. There is no `COUNT(DISTINCT ...)` or any deduplication logic whatsoever.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with shared advisories across SBOMs (2 unique advisories across 3 SBOMs) and asserts `vulnerability_count == 2`. This test would FAIL at runtime because the hardcoded value is `0`, not `2`.

## Verdict

FAIL. The subquery that would compute deduplicated advisory counts has not been implemented. The `// TODO: implement subquery` comment in the code confirms this is known-incomplete work. Deduplication logic cannot be verified because the count computation itself does not exist.
