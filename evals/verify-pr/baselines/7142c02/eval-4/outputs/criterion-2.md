# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Status: PASS (trivially, due to hardcoding defect)

## Analysis

The service layer in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for ALL packages:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

This means packages with no vulnerabilities will indeed show `vulnerability_count: 0`, but only because every package shows 0 regardless of actual vulnerability count. The criterion is technically satisfied, but only as a side effect of the hardcoding defect -- not because there is correct logic distinguishing packages with and without vulnerabilities.

A test exists (`test_package_without_vulnerabilities_has_zero_count`) that asserts `vulnerability_count == 0` for a package with no vulnerabilities, which would pass given the current hardcoded implementation.

## Evidence

- `vulnerability_count: 0` is hardcoded in the service layer
- The test for zero-count packages would pass, but only because ALL packages return 0

## Verdict

PASS -- The criterion is technically met (zero-vuln packages show 0), though this is a consequence of the hardcoding defect rather than correct implementation logic. The broader correctness issue is captured in Criterion 3.
