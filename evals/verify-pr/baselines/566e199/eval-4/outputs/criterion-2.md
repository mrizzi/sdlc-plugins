# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (superficially) / FAIL (substantively)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows the following implementation:

```rust
let items = items.into_iter().map(|p| {
    PackageSummary {
        id: p.id,
        name: p.name,
        version: p.version,
        license: p.license,
        vulnerability_count: 0, // TODO: implement subquery
    }
}).collect();
```

The `vulnerability_count` is hardcoded to `0` for ALL packages, regardless of whether they have vulnerabilities or not. This means packages with no vulnerabilities will indeed show `vulnerability_count: 0`, which technically satisfies this specific criterion in isolation. However, the hardcoding is the root cause of criterion 3's failure -- the value is always 0, not because there are no vulnerabilities, but because the subquery was never implemented.

While this criterion narrowly passes (zero-vulnerability packages do show 0), the implementation is only accidentally correct for this case. The value is not derived from any actual data lookup.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment explicitly acknowledges the subquery is not implemented.
- Test `test_package_without_vulnerabilities_has_zero_count` asserts `vulnerability_count == 0`, which would pass only because the value is hardcoded to 0 for all packages.
