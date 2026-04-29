# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (partial — hardcoded)

## Reasoning

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that the `vulnerability_count` field is set to `0` for all packages:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

This means packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is achieved by hardcoding the value to `0` for ALL packages, not by computing it via a subquery. While the specific criterion "packages with no vulnerabilities show 0" is technically satisfied, it is satisfied only because every package returns 0 — the implementation is incomplete.

The `// TODO: implement subquery` comment explicitly acknowledges that the actual computation is not implemented. This is a significant concern addressed in criterion 3.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- The value is hardcoded to `0` with a TODO comment indicating the subquery is not implemented
- Test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `vulnerability_count == 0`, which would pass with the hardcoded value
