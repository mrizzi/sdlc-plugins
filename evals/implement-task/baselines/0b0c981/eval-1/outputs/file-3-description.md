# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all test requirements from the task.

## Detailed Changes

Create a new file with the following content:

```rust
use trustify_test::TestApp;
use reqwest::StatusCode;

/// Test helper: expected response shape
#[derive(Debug, serde::Deserialize, PartialEq)]
struct SeveritySummary {
    critical: u32,
    high: u32,
    medium: u32,
    low: u32,
    total: u32,
}

/// Test 1: Valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    let app = TestApp::new().await;

    // Setup: create an SBOM and link advisories with known severities.
    // (Use test fixtures or direct DB insertion to create:
    //   - 2 Critical advisories
    //   - 3 High advisories
    //   - 1 Medium advisory
    //   - 0 Low advisories)
    let sbom_id = app.create_test_sbom().await;
    app.link_advisory_to_sbom(sbom_id, "critical").await;
    app.link_advisory_to_sbom(sbom_id, "critical").await;
    app.link_advisory_to_sbom(sbom_id, "high").await;
    app.link_advisory_to_sbom(sbom_id, "high").await;
    app.link_advisory_to_sbom(sbom_id, "high").await;
    app.link_advisory_to_sbom(sbom_id, "medium").await;

    let response = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(response.status(), StatusCode::OK);

    let summary: SeveritySummary = response.json().await.expect("invalid JSON");
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Test 2: Non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    let app = TestApp::new().await;

    let response = app
        .client()
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .send()
        .await
        .expect("request failed");

    assert_eq!(response.status(), StatusCode::NOT_FOUND);
}

/// Test 3: SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    let app = TestApp::new().await;

    let sbom_id = app.create_test_sbom().await;

    let response = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(response.status(), StatusCode::OK);

    let summary: SeveritySummary = response.json().await.expect("invalid JSON");
    assert_eq!(
        summary,
        SeveritySummary {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    );
}

/// Test 4: Duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    let app = TestApp::new().await;

    let sbom_id = app.create_test_sbom().await;
    // Link the same advisory twice — should only count once.
    let advisory_id = app.create_test_advisory("high").await;
    app.link_existing_advisory_to_sbom(sbom_id, advisory_id).await;
    app.link_existing_advisory_to_sbom(sbom_id, advisory_id).await;

    let response = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    assert_eq!(response.status(), StatusCode::OK);

    let summary: SeveritySummary = response.json().await.expect("invalid JSON");
    // Same advisory linked twice should only count once.
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 1);
}
```

## Rationale
- Covers all four test requirements from the task description.
- Follows the integration test pattern: tests live in `tests/api/` and hit a real PostgreSQL database via `TestApp`.
- Uses `tokio::test` for async test execution, consistent with the Axum + tokio stack.
- Test helper struct `SeveritySummary` is defined locally for deserialization (avoids importing from the main crate in integration tests, which is a common Rust pattern).
- The exact test setup helpers (`create_test_sbom`, `link_advisory_to_sbom`, `create_test_advisory`, `link_existing_advisory_to_sbom`) are pseudocode — the actual implementation should use whatever test fixtures and setup utilities exist in the project's test infrastructure. These would need to be confirmed by inspecting existing test files like `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- The deduplication test (Test 4) specifically creates the same advisory and links it twice, verifying the count is 1 not 2.

## Note
The exact test setup API (TestApp methods, fixture creation) must be adapted to match the project's existing test utilities. The patterns shown above are illustrative; the actual helpers should be discovered from `tests/api/sbom.rs` and `tests/api/advisory.rs`.
