# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task.

## Detailed Changes

Create a new test file with the following test cases:

```rust
use reqwest::StatusCode;
use test_context::test_context;

use crate::common::TestContext;

/// Test that a valid SBOM with known advisories returns correct severity counts.
#[test_context(TestContext)]
#[tokio::test]
async fn test_severity_summary_returns_correct_counts(ctx: &TestContext) {
    // Arrange: ingest test SBOM and link advisories with known severities
    // (1 Critical, 2 High, 1 Medium, 0 Low)
    let sbom_id = ctx.ingest_test_sbom().await;
    ctx.link_advisory(sbom_id, "CVE-2024-001", "Critical").await;
    ctx.link_advisory(sbom_id, "CVE-2024-002", "High").await;
    ctx.link_advisory(sbom_id, "CVE-2024-003", "High").await;
    ctx.link_advisory(sbom_id, "CVE-2024-004", "Medium").await;

    // Act
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Assert
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 2);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 4);
}

/// Test that a non-existent SBOM ID returns 404.
#[test_context(TestContext)]
#[tokio::test]
async fn test_severity_summary_returns_404_for_unknown_sbom(ctx: &TestContext) {
    let resp = ctx
        .client
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .send()
        .await
        .expect("request failed");

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test that an SBOM with no advisories returns all zeros.
#[test_context(TestContext)]
#[tokio::test]
async fn test_severity_summary_returns_zeros_when_no_advisories(ctx: &TestContext) {
    let sbom_id = ctx.ingest_test_sbom().await;

    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Test that duplicate advisory links are deduplicated in the count.
#[test_context(TestContext)]
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories(ctx: &TestContext) {
    let sbom_id = ctx.ingest_test_sbom().await;
    // Link the same advisory twice
    ctx.link_advisory(sbom_id, "CVE-2024-001", "Critical").await;
    ctx.link_advisory(sbom_id, "CVE-2024-001", "Critical").await;

    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 1);
    assert_eq!(body["total"], 1);
}
```

## Conventions Applied

- **Test file location**: `tests/api/advisory_summary.rs`, following the existing pattern of `tests/api/sbom.rs`, `tests/api/advisory.rs`, and `tests/api/search.rs`.
- **Test framework**: Uses `#[tokio::test]` for async tests and `test_context` for test fixture setup/teardown, matching existing tests.
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with existing integration tests.
- **Test naming**: Descriptive names following `test_<feature>_<scenario>` convention.
- **Coverage**: All four test requirements from the task are covered: correct counts, 404 for unknown SBOM, all zeros for empty, and deduplication.
