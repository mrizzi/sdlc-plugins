# Criterion 8 (Test Requirement 3): Add test_recommend_purls_dedup

## Criterion Text
Add `test_recommend_purls_dedup` to verify deduplication after qualifier removal.

## Evidence from PR Diff

### New function in `tests/api/purl_recommend.rs`
The `test_recommend_purls_dedup` function was added to the existing test file:

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

The test:
- Seeds two PURLs for the same package version with different `repository_url` qualifiers
- Requests recommendations (which now strip qualifiers and deduplicate)
- Asserts only 1 entry is returned (not 2)
- Asserts the returned PURL is in versioned-without-qualifiers format
- Includes a doc comment and given-when-then inline comments

## Verdict: PASS

The `test_recommend_purls_dedup` function was added and correctly validates the deduplication behavior after qualifier removal.
