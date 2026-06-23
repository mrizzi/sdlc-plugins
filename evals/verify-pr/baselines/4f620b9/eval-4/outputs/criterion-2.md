# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: FAIL

## Analysis

While the implementation technically returns `vulnerability_count: 0` for all packages, this is because the value is **hardcoded to 0** rather than being computed from actual vulnerability data.

In `modules/fundamental/src/package/service/mod.rs`, the implementation sets:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly confirms the implementation is incomplete. The acceptance criterion requires that the count be derived from data such that packages with no vulnerabilities naturally show 0 as a result of correct computation. The task's Implementation Notes specify a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id
```

No such subquery exists in the implementation. The value is hardcoded, meaning this criterion is satisfied only by accident (all packages return 0), not by correct logic. Packages that **do** have vulnerabilities would also incorrectly show 0.

The test `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`, which would fail against the current hardcoded implementation, further confirming that the intended behavior is not implemented.

This criterion fails because the implementation does not correctly compute the vulnerability count from data -- it merely hardcodes a constant.
