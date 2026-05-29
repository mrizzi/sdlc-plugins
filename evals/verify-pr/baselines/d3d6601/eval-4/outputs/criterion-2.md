# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (trivially, due to hardcoded zero)

## Analysis

In the PR diff for `modules/fundamental/src/package/service/mod.rs`, the `vulnerability_count` field is hardcoded to `0`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

This means ALL packages will show `vulnerability_count: 0`, regardless of whether they have vulnerabilities or not. While packages with no vulnerabilities will indeed show zero, this is a degenerate case -- the value is always zero, not because of a correct computation but because the implementation is incomplete.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` would pass with this hardcoded value, but only coincidentally.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line with `vulnerability_count: 0`
- The `// TODO: implement subquery` comment confirms this is a placeholder, not a real implementation.

## Conclusion

This criterion technically passes for the zero-vulnerability case, but only because the value is hardcoded to zero for ALL packages. The hardcoded zero is an implementation shortcut, not a correct computation. This criterion's satisfaction is incidental rather than intentional.
