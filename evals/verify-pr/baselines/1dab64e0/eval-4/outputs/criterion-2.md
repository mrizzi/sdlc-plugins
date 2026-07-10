# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (vacuous)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that the `vulnerability_count` field is hardcoded to `0`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to `0` for ALL packages, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is only vacuously true -- the criterion is satisfied not because the implementation correctly identifies packages without vulnerabilities, but because every package unconditionally returns 0.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts this behavior:

```rust
assert_eq!(pkg.vulnerability_count, 0);
```

This test would pass with the hardcoded value, but it does not validate that the zero comes from an actual computation rather than a placeholder.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Line:** `vulnerability_count: 0, // TODO: implement subquery`
- The hardcoded value satisfies the literal criterion but does so without any actual vulnerability computation logic.

## Conclusion

This criterion is technically satisfied by the current code, but the satisfaction is vacuous -- it passes only because the hardcoded default happens to match the expected output for the zero-vulnerability case. The missing subquery implementation (flagged in criterion 3) means this criterion's PASS is misleading in isolation.
