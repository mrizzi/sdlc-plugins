# Criterion 7: Remove `test_recommend_purls_with_qualifiers`

## Criterion Text
Remove `test_recommend_purls_with_qualifiers` (no longer applicable).

## Evidence from PR Diff

### Base-branch version (`tests/api/purl_recommend.rs`)
The base branch contained a test function `test_recommend_purls_with_qualifiers` (lines 30-48) that verified qualifier details were returned as separate entries:
```rust
/// Verifies that PURL recommendations include qualifier details when present.
#[test_context(TestContext)]
#[tokio::test]
async fn test_recommend_purls_with_qualifiers(ctx: &TestContext) {
    // Given PURLs with different qualifiers for the same package version
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

    // Then both qualifier variants are returned as separate entries
    assert_eq!(body.items.len(), 2);
    assert!(body.items[0].purl.contains("repository_url="));
    assert!(body.items[1].purl.contains("repository_url="));
    assert_ne!(body.items[0].purl, body.items[1].purl);
}
```

### PR diff
The diff shows this entire function removed (lines prefixed with `-`):
```diff
-/// Verifies that PURL recommendations include qualifier details when present.
-#[test_context(TestContext)]
-#[tokio::test]
-async fn test_recommend_purls_with_qualifiers(ctx: &TestContext) {
-    ...
-}
```

The function is entirely absent from the PR-branch version of the file.

## Verdict: PASS

The `test_recommend_purls_with_qualifiers` test function was completely removed from `tests/api/purl_recommend.rs`, as required by the task. This is appropriate because qualifier-specific behavior no longer exists in the endpoint.
