# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Result: FAIL

## Analysis

This criterion requires that packages with no associated vulnerabilities correctly display a `vulnerability_count` of `0`. At first glance this appears to work because the implementation hardcodes `vulnerability_count: 0` for ALL packages. However, this is an incidental side effect of an incomplete implementation, not correct behavior.

In `modules/fundamental/src/package/service/mod.rs`, the implementation is:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the subquery to compute the actual vulnerability count has not been implemented. The value `0` is hardcoded for every package, regardless of whether they have vulnerabilities or not. While this accidentally produces the correct result for packages with no vulnerabilities, it does so for the wrong reason -- the same hardcoded value is returned for packages WITH vulnerabilities too.

The task's Implementation Notes specify that the count should be computed using a correlated subquery:
```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id
```

This subquery was never implemented. The "correct" zero value for non-vulnerable packages is merely a coincidence of the hardcoded default, not a result of actual computation.

Additionally, the test `test_package_without_vulnerabilities_has_zero_count` would pass only because the hardcoded value happens to be 0, but this test would not catch a regression if the hardcoded value were changed to any other number, because the underlying query logic is absent.

## Verdict

FAIL. The zero count for non-vulnerable packages is a side effect of an incomplete implementation (hardcoded `0` for all packages), not a correctly computed result. The implementation must compute the count via a database subquery for this criterion to be genuinely satisfied.
