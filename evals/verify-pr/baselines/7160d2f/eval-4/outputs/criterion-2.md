# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (with caveat)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows the service layer mapping:

```rust
+        let items = items.into_iter().map(|p| {
+            PackageSummary {
+                id: p.id,
+                name: p.name,
+                version: p.version,
+                license: p.license,
+                vulnerability_count: 0, // TODO: implement subquery
+            }
+        }).collect();
```

The field is hardcoded to `0` for ALL packages, not just those without vulnerabilities. This means packages with no vulnerabilities will correctly show `vulnerability_count: 0`. However, this is only because the value is hardcoded -- there is no actual query computing vulnerability counts.

A test also verifies this behavior:

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

This test would pass with the hardcoded value, but it does not truly validate the criterion in a meaningful way since the value is always 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- hardcoded `vulnerability_count: 0`
- File: `tests/api/package_vuln_count.rs` -- test `test_package_without_vulnerabilities_has_zero_count` asserts `vulnerability_count == 0`
- The zero-count case technically passes, but only because the subquery is not implemented (see Criterion 3)
