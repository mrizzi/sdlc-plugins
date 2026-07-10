# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task description specifies that `vulnerability_count` should be computed via a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery would join through `sbom_package`, `sbom_advisory`, and `advisory` tables and use `COUNT(DISTINCT a.id)` to ensure unique advisory counts (no duplicates from multiple SBOMs).

However, the PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+        let items = items.into_iter().map(|p| {
+            PackageSummary {
+                id: p.id,
+                name: p.name,
+                version: p.version,
+                license: p.license,
+                vulnerability_count: 0, // TODO: implement subquery
+            }
+        }).collect();
```

The `vulnerability_count` is hardcoded to `0` with an explicit `// TODO: implement subquery` comment. No subquery, no join logic, and no `COUNT(DISTINCT ...)` computation exists anywhere in the diff. The core functionality that this acceptance criterion requires -- computing unique advisory counts -- is entirely unimplemented.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Critical line:** `vulnerability_count: 0, // TODO: implement subquery`
- **Missing:** No `SELECT COUNT(DISTINCT ...)` subquery
- **Missing:** No join through `sbom_package`, `sbom_advisory`, `advisory` tables
- **Missing:** No deduplication logic of any kind
- The `TODO` comment is an explicit acknowledgment by the author that this work is incomplete

The test `test_vulnerability_count_deduplicates_across_sboms` in the new test file asserts `pkg.vulnerability_count == 2`, but with the hardcoded value of 0, this test would fail at runtime, contradicting the claim that all CI checks pass. This suggests the test file was added but may not be wired into the test suite, or the test fixtures in the eval scenario are synthetic.

## Conclusion

This criterion is definitively NOT satisfied. The entire subquery implementation is missing. The hardcoded `vulnerability_count: 0` means the count never reflects any advisories at all, let alone unique ones. This is the most critical gap in the PR.
