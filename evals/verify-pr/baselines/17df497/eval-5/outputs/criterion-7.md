# Criterion 7 (Test Requirement): Remove `test_recommend_purls_with_qualifiers`

## Criterion Text
Remove `test_recommend_purls_with_qualifiers` (no longer applicable).

## Evidence from PR Diff

### Base-branch version
The base branch contained the function `test_recommend_purls_with_qualifiers`:
```rust
/// Verifies that PURL recommendations include qualifier details when present.
#[test_context(TestContext)]
#[tokio::test]
async fn test_recommend_purls_with_qualifiers(ctx: &TestContext) {
    // Given PURLs with different qualifiers for the same package version
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

    // When requesting recommendations
    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;

    // Then both qualifier variants are returned as separate entries
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PurlSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
    assert!(body.items[0].purl.contains("repository_url="));
    assert!(body.items[1].purl.contains("repository_url="));
    assert_ne!(body.items[0].purl, body.items[1].purl);
}
```

### PR version
The diff shows the entire function removed (lines prefixed with `-`). The function is replaced by `test_recommend_purls_dedup`, which tests the opposite behavior -- that entries previously distinct due to qualifiers are now deduplicated into a single entry.

## Verdict: PASS

The `test_recommend_purls_with_qualifiers` function was fully removed from `tests/api/purl_recommend.rs` as required.
