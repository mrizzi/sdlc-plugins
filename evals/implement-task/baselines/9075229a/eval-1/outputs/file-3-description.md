# File 3: tests/api/advisory_summary.rs

## Action: CREATE

## Purpose
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the four test requirements from the task description.

## Detailed Changes

Create a new integration test file following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom_with_advisories() {
    // Given an SBOM with advisories at known severity levels:
    // 2 Critical, 1 High, 3 Medium, 0 Low
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "medium").await;
    create_test_advisory(&app, sbom_id, "medium").await;
    create_test_advisory(&app, sbom_id, "medium").await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 status, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for a non-existent SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_empty_sbom_returns_all_zeros() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_by_advisory_id() {
    // Given an SBOM with duplicate links to the same advisory
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "high").await;
    // Link the same advisory to the SBOM a second time
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Conventions Applied
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` for status checks, then deserializes body and checks individual field values -- matching sibling test patterns in `tests/api/advisory.rs`.
- **Value-based assertions**: Asserts on specific severity count values (not just `total > 0` or `items.len()`), so failures reveal what changed.
- **404 test**: Dedicated test for non-existent resource returning 404, present in all sibling test files.
- **Test naming**: `test_advisory_summary_<scenario>` following the `test_<endpoint>_<scenario>` pattern.
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies.
- **Given/When/Then**: Non-trivial tests use section comments for navigability.
- **Test setup**: Each test creates its own fixtures via helper functions (`create_test_sbom`, `create_test_advisory`), matching the pattern of per-test setup in sibling files.
- **File placement**: In `tests/api/` alongside `advisory.rs`, `sbom.rs`, and `search.rs`.
