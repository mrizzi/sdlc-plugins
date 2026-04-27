# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Result: FAIL

## Analysis

The PR diff in `modules/fundamental/src/package/service/mod.rs` shows the following implementation:

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

The `vulnerability_count` is **hardcoded to `0`** for ALL packages, regardless of whether they have vulnerabilities or not. The `// TODO: implement subquery` comment explicitly acknowledges that the actual vulnerability counting logic has not been implemented.

While packages with no vulnerabilities would technically show `0`, this is coincidental -- the value is hardcoded, not computed. The criterion implies a working implementation that dynamically returns 0 when there are no vulnerabilities. Since the count is always 0 regardless of actual vulnerability data, this criterion cannot be considered satisfied.

Furthermore, this hardcoded value means that criterion 3 (unique advisory counts) is also necessarily unsatisfied, since no counting logic exists at all.

The implementation is incomplete. The `TODO` comment is explicit evidence that this is a placeholder, not a finished implementation.
