# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all acceptance criteria and test requirements specified in TC-9201.

## Full Contents

```rust
//! Integration tests for the advisory severity summary endpoint.

use reqwest::StatusCode;
use serde_json::Value;
// Additional imports depend on the test harness discovered during pre-implementation inspection.
// Typical imports include:
// - Test setup utilities (TestApp, TestDb, or similar)
// - Entity builders for seeding test data
// - The SeveritySummary struct for typed deserialization

/// Test 1: A valid SBOM with known advisories returns correct severity counts.
///
/// Setup:
///   - Create an SBOM in the test database
///   - Create advisories with known severities:
///     - 2x Critical
///     - 3x High
///     - 1x Medium
///     - 0x Low
///   - Link all advisories to the SBOM via sbom_advisory
///
/// Assertion:
///   - Response status is 200
///   - Body: { critical: 2, high: 3, medium: 1, low: 0, total: 6 }
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // 1. Set up test app and database
    let app = TestApp::spawn().await;

    // 2. Seed test data: SBOM + advisories with known severities
    let sbom_id = app.seed_sbom("test-sbom-1").await;
    app.seed_advisory_linked_to_sbom(sbom_id, "critical").await;
    app.seed_advisory_linked_to_sbom(sbom_id, "critical").await;
    app.seed_advisory_linked_to_sbom(sbom_id, "high").await;
    app.seed_advisory_linked_to_sbom(sbom_id, "high").await;
    app.seed_advisory_linked_to_sbom(sbom_id, "high").await;
    app.seed_advisory_linked_to_sbom(sbom_id, "medium").await;

    // 3. Call the endpoint
    let resp = app
        .client
        .get(&format!("{}/api/v2/sbom/{}/advisory-summary", app.base_url, sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // 4. Assert
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.expect("Failed to parse JSON");
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Test 2: A non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    let app = TestApp::spawn().await;

    let resp = app
        .client
        .get(&format!(
            "{}/api/v2/sbom/{}/advisory-summary",
            app.base_url, "nonexistent-sbom-id"
        ))
        .send()
        .await
        .expect("Failed to send request");

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test 3: An SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let app = TestApp::spawn().await;

    // Seed an SBOM with no linked advisories
    let sbom_id = app.seed_sbom("test-sbom-empty").await;

    let resp = app
        .client
        .get(&format!("{}/api/v2/sbom/{}/advisory-summary", app.base_url, sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.expect("Failed to parse JSON");
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Test 4: Duplicate advisory links are deduplicated in the count.
///
/// Setup:
///   - Create an SBOM
///   - Create one advisory with "high" severity
///   - Link the same advisory to the SBOM multiple times (duplicate join rows)
///
/// Assertion:
///   - The advisory is counted only once: { critical: 0, high: 1, medium: 0, low: 0, total: 1 }
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    let app = TestApp::spawn().await;

    let sbom_id = app.seed_sbom("test-sbom-dedup").await;
    let advisory_id = app.seed_advisory("high").await;

    // Link the same advisory to the SBOM multiple times
    app.link_advisory_to_sbom(advisory_id, sbom_id).await;
    app.link_advisory_to_sbom(advisory_id, sbom_id).await;
    app.link_advisory_to_sbom(advisory_id, sbom_id).await;

    let resp = app
        .client
        .get(&format!("{}/api/v2/sbom/{}/advisory-summary", app.base_url, sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.expect("Failed to parse JSON");
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 1);
}
```

## Design Decisions

1. **Pseudo-code test harness**: The exact test setup (e.g., `TestApp::spawn()`, `app.seed_sbom()`) is placeholder code. During pre-implementation inspection, existing test files in `tests/api/` will be examined to discover the actual test harness API, database seeding patterns, and HTTP client configuration.

2. **`serde_json::Value` for response parsing**: Uses untyped JSON parsing in tests for flexibility. Alternatively, the tests could deserialize directly into `SeveritySummary` for stronger type checking — the decision depends on existing test conventions.

3. **Four tests cover all acceptance criteria**:
   - Test 1: Correct counts for known severities
   - Test 2: 404 for non-existent SBOM
   - Test 3: All zeros for empty SBOM
   - Test 4: Deduplication of advisory links

4. **Test isolation**: Each test creates its own SBOM and advisories, ensuring tests are independent and can run in parallel.

## Notes

- The test file may need to be registered in `tests/api/mod.rs` or a similar test module manifest, depending on how the test suite is organized.
- The exact database seeding mechanism (direct entity insertion, fixture loading, or builder pattern) will be determined during pre-implementation inspection.
- If the existing test suite uses a different HTTP client (e.g., `actix_web::test` instead of `reqwest`), the test code will be adapted accordingly.
