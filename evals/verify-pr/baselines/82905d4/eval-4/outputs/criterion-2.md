# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Result: PARTIAL PASS (with concern)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows the service layer setting:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

This hardcodes `vulnerability_count: 0` for ALL packages, not just packages with no vulnerabilities. While packages with no vulnerabilities will correctly show `vulnerability_count: 0`, this is achieved by accident rather than by design -- the value is hardcoded to 0 regardless of actual vulnerability count.

The test file `tests/api/package_vuln_count.rs` includes a test `test_package_without_vulnerabilities_has_zero_count` that asserts `vulnerability_count == 0` for a package with no vulnerabilities. This test would pass because the value is always hardcoded to 0.

However, the hardcoded 0 means the implementation is fundamentally incomplete -- it does not actually compute vulnerability counts. The `// TODO: implement subquery` comment confirms this is a stub, not a real implementation.

## Verdict

While the test for zero-count packages would technically pass, this criterion is only trivially satisfied because the implementation is a stub. The real subquery was never implemented. This is a concern that affects criterion 3 more directly.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- hardcoded `vulnerability_count: 0`
- The `TODO` comment explicitly acknowledges the subquery is not implemented
- File: `tests/api/package_vuln_count.rs` -- test for zero count exists but would pass trivially
