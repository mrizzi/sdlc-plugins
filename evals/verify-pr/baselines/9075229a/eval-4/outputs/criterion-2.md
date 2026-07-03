# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Criterion Text
Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS

## Reasoning

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

While this is hardcoded rather than computed, it does mean that every package -- including those with no vulnerabilities -- will show `vulnerability_count: 0`. The criterion as literally stated ("packages with no vulnerabilities show vulnerability_count: 0") is satisfied, since the value will indeed be 0 for packages without vulnerabilities.

However, it is important to note that this satisfaction is vacuous: the value is 0 for ALL packages regardless of their actual vulnerability count. The hardcoded implementation means this criterion passes only by coincidence, not by correct computation. The real defect is captured in criterion 3 (unique advisory count), which this hardcoding directly violates.

## Evidence
- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `pkg.vulnerability_count == 0`, which would pass with the hardcoded value
