# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The task's implementation notes specify a correlated subquery to compute the vulnerability count:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

The `COUNT(DISTINCT a.id)` is critical for deduplication -- a package may appear in multiple SBOMs that share the same advisory, and the count must reflect unique advisories only.

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this subquery. Instead, it hardcodes the value to zero:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges the implementation is incomplete. The correlated subquery joining through `sbom_package -> sbom_advisory -> advisory` tables with `COUNT(DISTINCT ...)` was never written.

This means:
- Packages with actual vulnerabilities will incorrectly show `vulnerability_count: 0`
- The deduplication logic (using `DISTINCT`) is entirely absent
- The test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`, which would FAIL at runtime since the implementation always returns 0

This is a critical implementation gap. The core business logic requested by the task was not implemented.
