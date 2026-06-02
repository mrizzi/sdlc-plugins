# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (with caveats)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that the `vulnerability_count` field is hardcoded to `0`:

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

Because the value is hardcoded to `0` for all packages (with a TODO comment indicating the subquery is not yet implemented), packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is a trivial satisfaction of the criterion -- the value is always 0 regardless of actual vulnerability status.

The test file `tests/api/package_vuln_count.rs` includes a test `test_package_without_vulnerabilities_has_zero_count` that validates this behavior:

```rust
async fn test_package_without_vulnerabilities_has_zero_count(ctx: &TestContext) {
    let pkg_id = ctx.seed_package("pkg-safe", "MIT").await;
    let resp = ctx.get("/api/v2/package").await;
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    let pkg = body.items.iter().find(|p| p.id == pkg_id).unwrap();
    assert_eq!(pkg.vulnerability_count, 0);
}
```

This test would pass with the current implementation since the value is always 0. Note that this criterion passes only because the hardcoded value happens to be 0 -- it does not validate that the system correctly computes a zero count from actual data.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- hardcoded `vulnerability_count: 0`
- File: `tests/api/package_vuln_count.rs` -- test asserts zero count for package with no vulnerabilities
- The criterion is technically satisfied but only because the hardcoded default is 0
