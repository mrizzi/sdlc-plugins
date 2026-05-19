# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially, due to hardcoded value)

## Reasoning

The service layer in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for all packages:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to 0, packages with no vulnerabilities will trivially show `vulnerability_count: 0`. However, this is a side effect of the incomplete implementation rather than a correct implementation of the zero-vulnerability case. The subquery that should compute the actual count has not been implemented (as indicated by the TODO comment).

A proper implementation would compute the count via a correlated subquery and naturally return 0 for packages without advisories. Nevertheless, the observable behavior for this specific criterion -- packages with no vulnerabilities showing 0 -- is technically satisfied.

## Evidence
- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0` hardcoded
- The TODO comment explicitly acknowledges the subquery is not implemented
- Test `test_package_without_vulnerabilities_has_zero_count` asserts `vulnerability_count == 0`, which would pass against the hardcoded value
