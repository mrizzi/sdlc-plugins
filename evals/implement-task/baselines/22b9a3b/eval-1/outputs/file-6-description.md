# File 6: tests/api/advisory_summary.rs

## Action: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements specified in the task.

## Sibling Reference

Modeled after `tests/api/advisory.rs` and `tests/api/sbom.rs` which:
- Use `#[tokio::test]` for async test functions
- Hit a real PostgreSQL test database
- Use `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
- Set up test data, make HTTP requests, and assert responses

## Detailed Changes

```rust
use axum::http::StatusCode;
use serde_json::Value;

// Test helper imports -- following the pattern from sibling test files
// (exact imports depend on the test harness setup in the project)

/// Test that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Setup: Create test SBOM and link advisories with known severities
    // - 2 Critical advisories
    // - 3 High advisories  
    // - 1 Medium advisory
    // - 0 Low advisories
    let app = test_app().await;

    let sbom_id = create_test_sbom(&app).await;
    create_and_link_advisory(&app, sbom_id, "critical").await;
    create_and_link_advisory(&app, sbom_id, "critical").await;
    create_and_link_advisory(&app, sbom_id, "high").await;
    create_and_link_advisory(&app, sbom_id, "high").await;
    create_and_link_advisory(&app, sbom_id, "high").await;
    create_and_link_advisory(&app, sbom_id, "medium").await;

    // Act: Call the severity summary endpoint
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Assert: Verify status and response body
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Test that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    let app = test_app().await;

    let resp = app
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .await;

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let app = test_app().await;

    // Setup: Create an SBOM with no linked advisories
    let sbom_id = create_test_sbom(&app).await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Test that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    let app = test_app().await;

    let sbom_id = create_test_sbom(&app).await;

    // Create one advisory and link it to the SBOM multiple times
    let advisory_id = create_advisory(&app, "high").await;
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;  // Duplicate link
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;  // Another duplicate

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    // Despite 3 links, there is only 1 unique advisory
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
    assert_eq!(body["critical"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
}
```

## Design Notes

- **Test helper functions**: Functions like `test_app()`, `create_test_sbom()`, `create_and_link_advisory()`, `create_advisory()`, and `link_advisory_to_sbom()` are assumed to exist or would be created as test helpers, following the patterns established in sibling test files. The exact implementation depends on the project's test setup infrastructure.
- **Four test cases**: Each maps directly to a test requirement from the task:
  1. Valid SBOM with known advisories returns correct severity counts
  2. Non-existent SBOM ID returns 404
  3. SBOM with no advisories returns all zeros
  4. Duplicate advisory links are deduplicated in the count
- **Real database**: Tests use the actual PostgreSQL test database, consistent with the project convention (not mocked).
- **JSON assertions**: Use `serde_json::Value` to parse and assert individual fields, ensuring the response shape matches the API contract.
- **Test file registration**: The test file may also need to be registered in `tests/api/mod.rs` or referenced in `tests/Cargo.toml` depending on the project's test configuration. This would be verified by examining the sibling test setup.
