# Criterion 7 (Test Requirement 2): Remove test_recommend_purls_with_qualifiers

## Criterion Text
Remove `test_recommend_purls_with_qualifiers` (no longer applicable).

## Evidence from PR Diff

### Removal in `tests/api/purl_recommend.rs`
The entire `test_recommend_purls_with_qualifiers` function was removed from the diff. The following lines are shown as deleted (prefixed with `-`):

```rust
-/// Verifies that PURL recommendations include qualifier details when present.
-#[test_context(TestContext)]
-#[tokio::test]
-async fn test_recommend_purls_with_qualifiers(ctx: &TestContext) {
-    // Given PURLs with different qualifiers for the same package version
-    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
-    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;
-
-    // When requesting recommendations
-    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;
-
-    // Then both qualifier variants are returned as separate entries
-    assert_eq!(resp.status(), StatusCode::OK);
-    let body: PaginatedResults<PurlSummary> = resp.json().await;
-    assert_eq!(body.items.len(), 2);
-    assert!(body.items[0].purl.contains("repository_url="));
-    assert!(body.items[1].purl.contains("repository_url="));
-    assert_ne!(body.items[0].purl, body.items[1].purl);
-}
```

This function existed in the base branch (lines 30-48 of `tests/api/purl_recommend.rs`) and tested qualifier-specific behavior that no longer exists after the simplification change.

## Verdict: PASS

The `test_recommend_purls_with_qualifiers` function was entirely removed from the test file, as required. This is appropriate since qualifier-specific response behavior no longer exists.
