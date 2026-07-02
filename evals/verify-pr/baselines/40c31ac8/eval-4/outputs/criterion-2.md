## Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

### Result: FAIL

### Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded to zero for ALL packages:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

While this technically produces `0` for packages with no vulnerabilities, it does so by accident -- the value is hardcoded to `0` for every package regardless of actual vulnerability state. The `// TODO: implement subquery` comment explicitly acknowledges the implementation is incomplete.

A correct implementation would compute the count via a subquery joining `sbom_package`, `sbom_advisory`, and `advisory` tables, which would naturally return `0` for packages with no linked advisories. Instead, the current code simply maps every package to `vulnerability_count: 0` without any database query.

### Conclusion

This criterion is NOT genuinely satisfied. While the output happens to be `0` for non-vulnerable packages, this is a side effect of a hardcoded stub, not a correct implementation. The TODO comment confirms the real logic has not been written.
