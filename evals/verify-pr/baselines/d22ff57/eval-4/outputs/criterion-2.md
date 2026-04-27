# Criterion 2

**Text:** Packages with no vulnerabilities show `vulnerability_count: 0`

**Classification:** LEGITIMATE

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability_count is hardcoded:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

This means ALL packages -- regardless of whether they have vulnerabilities or not -- will return `vulnerability_count: 0`. While packages with no vulnerabilities would technically show 0, this is an accidental correctness resulting from a stub implementation, not from actual logic that queries the database.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` would pass at runtime only because the value is always hardcoded to 0, not because the logic correctly determines the package has no vulnerabilities.

However, the criterion as stated ("packages with no vulnerabilities show 0") is trivially satisfied by the current implementation even though it is a stub.

## Verdict: PASS (with caveat)

The criterion is technically satisfied, but only because the hardcoded value of 0 happens to match the expected output for vulnerability-free packages. This is degenerate satisfaction -- the implementation is a stub. The real test of this criterion is criterion 3 (subquery-based counting), which fails.
