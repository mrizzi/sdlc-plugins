# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that the `vulnerability_count` field reflects unique advisories, computed via a correlated subquery joining through `sbom_package`, `sbom_advisory`, and `advisory` tables with `COUNT(DISTINCT a.id)` to avoid duplicates from multiple SBOMs.

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is hardcoded to `0` for ALL packages. The subquery described in the Implementation Notes has NOT been implemented. The `// TODO: implement subquery` comment explicitly acknowledges this omission.

This means:
- Packages WITH known vulnerabilities will incorrectly show `vulnerability_count: 0`
- Deduplication across SBOMs is not implemented because no query exists at all
- The test `test_package_with_vulnerabilities_has_count` (which asserts `vulnerability_count == 3`) would FAIL at runtime

The test file `tests/api/package_vuln_count.rs` includes a deduplication test:

```rust
async fn test_vulnerability_count_deduplicates_across_sboms(ctx: &TestContext) {
    let pkg_id = ctx.seed_package_with_shared_advisories("pkg-dedup", 2, 3).await;
    let resp = ctx.get("/api/v2/package").await;
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    let pkg = body.items.iter().find(|p| p.id == pkg_id).unwrap();
    assert_eq!(pkg.vulnerability_count, 2);
}
```

This test asserts `vulnerability_count == 2`, but the implementation returns `0` for all packages, so this test would fail at runtime.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0` hardcoded with `// TODO: implement subquery`
- No correlated subquery joining `sbom_package` -> `sbom_advisory` -> `advisory` tables exists in the diff
- No `COUNT(DISTINCT a.id)` logic is present anywhere in the diff
- Test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` but implementation returns `0`
- Test `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` but implementation returns `0`
