<!-- SYNTHETIC TEST DATA — base-branch version of tests/api/purl_recommend.rs for eval testing; simulates `git show main:tests/api/purl_recommend.rs` output -->

```rust
use crate::common::TestContext;
use axum::http::StatusCode;
use common::model::paginated::PaginatedResults;
use common::purl::PurlSummary;

/// Verifies that basic PURL recommendations return fully qualified PURLs.
#[test_context(TestContext)]
#[tokio::test]
async fn test_recommend_purls_basic(ctx: &TestContext) {
    // Given a package with known PURLs in the database
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?repository_url=https://repo1.maven.org&type=jar").await;

    // When requesting recommendations for the base PURL
    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;

    // Then recommendations are returned with fully qualified PURLs
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PurlSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
    assert_eq!(
        body.items[0].purl,
        "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"
    );
}

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

/// Verifies that recommendations for an unknown PURL return an empty list.
#[test_context(TestContext)]
#[tokio::test]
async fn test_recommend_purls_unknown_returns_empty(ctx: &TestContext) {
    // When requesting recommendations for a PURL not in the database
    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/com.example/nonexistent").await;

    // Then an empty paginated result is returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PurlSummary> = resp.json().await;
    assert_eq!(body.items.len(), 0);
    assert_eq!(body.total, 0);
}

/// Verifies that recommendations respect pagination parameters.
#[test_context(TestContext)]
#[tokio::test]
async fn test_recommend_purls_pagination(ctx: &TestContext) {
    // Given 5 versioned PURLs for the same package
    for i in 1..=5 {
        ctx.seed_purl(&format!(
            "pkg:maven/org.apache/commons-lang3@3.{}?repository_url=https://repo1.maven.org&type=jar",
            i
        )).await;
    }

    // When requesting with limit=2
    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

    // Then only 2 items are returned but total reflects all versions
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PurlSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
    assert_eq!(body.total, 5);
}
```
