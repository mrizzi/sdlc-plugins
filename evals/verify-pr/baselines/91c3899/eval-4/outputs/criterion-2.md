# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially)

## Reasoning

The service layer in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for all packages:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to `0`, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is only trivially satisfied -- the hardcoded zero is a placeholder, not the result of a correct query that would return 0 when no advisories exist. The criterion passes on its face, but the implementation is incomplete.

A test (`test_package_without_vulnerabilities_has_zero_count`) exists that asserts `pkg.vulnerability_count == 0`, and this test would pass against the hardcoded implementation.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- Test: `test_package_without_vulnerabilities_has_zero_count` seeds a package with no advisories and asserts `vulnerability_count == 0`
