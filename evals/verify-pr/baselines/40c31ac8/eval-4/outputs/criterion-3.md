## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

### Result: FAIL

### Evidence

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes the vulnerability count to zero:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

There is no subquery, no join across `sbom_package` / `sbom_advisory` / `advisory` tables, and no `COUNT(DISTINCT ...)` logic. The task description specifies the count should use `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`, but none of this SQL logic exists in the diff.

The test `test_vulnerability_count_deduplicates_across_sboms` in the new test file seeds a package with 2 unique advisories shared across 3 SBOMs and asserts `vulnerability_count == 2`. This test would fail at runtime because the implementation always returns `0`.

### Conclusion

This criterion is not met. The deduplication logic has not been implemented at all. The TODO comment confirms the subquery is missing entirely.
