# Criterion 8: Add `test_recommend_purls_dedup` to verify deduplication after qualifier removal

## Criterion Text
Add `test_recommend_purls_dedup` to verify deduplication after qualifier removal.

## Evidence from PR Diff

### New function in `tests/api/purl_recommend.rs`
The PR adds a new test function `test_recommend_purls_dedup`:
```rust
/// Verifies that removing qualifiers deduplicates entries that were previously distinct.
#[test_context(TestContext)]
#[tokio::test]
async fn test_recommend_purls_dedup(ctx: &TestContext) {
    // Given PURLs with different qualifiers for the same package version
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;

    // When requesting recommendations (qualifiers stripped, dedup applied)
    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;

    // Then only one entry is returned (deduplicated after qualifier removal)
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PurlSummary> = resp.json().await;
    assert_eq!(body.items.len(), 1);
    assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
}
```

### Test design
The test seeds two PURLs for the same package version (`@3.12`) but with different `repository_url` qualifiers (`repo1` vs `repo2`). It then requests recommendations and asserts:
1. Only 1 item is returned (confirming deduplication occurred)
2. The returned PURL is the versioned form without qualifiers

This test directly validates the deduplication behavior introduced by the `dedup_by(|a, b| a.purl == b.purl)` call in the service layer.

## Verdict: PASS

The `test_recommend_purls_dedup` function was added to `tests/api/purl_recommend.rs` and correctly verifies that entries previously distinct due to different qualifiers are collapsed into a single entry after qualifier removal.
