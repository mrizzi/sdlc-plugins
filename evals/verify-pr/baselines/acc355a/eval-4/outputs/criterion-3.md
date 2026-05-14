# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded to zero:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task's Implementation Notes specify the required approach:

> Use a correlated subquery to count advisories: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

This subquery has NOT been implemented. The `TODO: implement subquery` comment explicitly acknowledges the implementation is incomplete.

## Reasoning

The criterion requires that the count reflects unique advisories only, with no duplicates from multiple SBOMs. Since `vulnerability_count` is hardcoded to `0` for every package regardless of actual advisory data, it does not reflect any advisory counts at all -- let alone deduplicated ones. The core logic that this criterion tests (the `COUNT(DISTINCT a.id)` correlated subquery) is entirely missing.

The tests in `tests/api/package_vuln_count.rs` assert specific non-zero counts:
- `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3`
- `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2`

Both of these tests would fail at runtime because the service always returns 0.

This criterion clearly FAILS.
