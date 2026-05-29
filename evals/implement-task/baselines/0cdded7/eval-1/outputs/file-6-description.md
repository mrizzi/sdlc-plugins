# File 6: Create `tests/api/advisory_summary.rs`

## Action: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all acceptance criteria and test requirements from the task.

## Detailed Changes

This is a new file. The complete contents would be:

```rust
use actix_http::StatusCode;
use serde::Deserialize;
use test_context::test_context;

#[derive(Debug, Deserialize)]
struct SeveritySummaryResponse {
    critical: u32,
    high: u32,
    medium: u32,
    low: u32,
    total: u32,
}

/// Test that a valid SBOM with known advisories returns correct severity counts
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    let server = TestServer::new().await;

    // Set up test data: create an SBOM and link advisories with known severities
    // (2 Critical, 1 High, 3 Medium, 0 Low)
    let sbom_id = server.ingest_test_sbom("test-sbom-1").await;
    server.link_advisory(sbom_id, "ADV-001", "Critical").await;
    server.link_advisory(sbom_id, "ADV-002", "Critical").await;
    server.link_advisory(sbom_id, "ADV-003", "High").await;
    server.link_advisory(sbom_id, "ADV-004", "Medium").await;
    server.link_advisory(sbom_id, "ADV-005", "Medium").await;
    server.link_advisory(sbom_id, "ADV-006", "Medium").await;

    let resp = server
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummaryResponse = resp.json().await;
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 3);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 6);
}

/// Test that a non-existent SBOM ID returns 404
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    let server = TestServer::new().await;

    let resp = server
        .get("/api/v2/sbom/non-existent-id/advisory-summary")
        .await;

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test that an SBOM with no advisories returns all zeros
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let server = TestServer::new().await;

    // Create an SBOM with no linked advisories
    let sbom_id = server.ingest_test_sbom("test-sbom-empty").await;

    let resp = server
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummaryResponse = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}

/// Test that duplicate advisory links are deduplicated in the count
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    let server = TestServer::new().await;

    let sbom_id = server.ingest_test_sbom("test-sbom-dedup").await;
    // Link the same advisory twice -- should be counted only once
    server.link_advisory(sbom_id, "ADV-001", "Critical").await;
    server.link_advisory(sbom_id, "ADV-001", "Critical").await;
    server.link_advisory(sbom_id, "ADV-002", "High").await;

    let resp = server
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummaryResponse = resp.json().await;
    assert_eq!(body.critical, 1, "duplicate advisory should be counted only once");
    assert_eq!(body.high, 1);
    assert_eq!(body.total, 2, "total should reflect deduplicated count");
}
```

## Conventions Applied

- **Test framework**: Uses `#[tokio::test]` for async tests, matching `tests/api/advisory.rs` and `tests/api/sbom.rs`
- **Test server setup**: Uses `TestServer::new().await` to spin up a test instance with a real PostgreSQL test database
- **HTTP assertions**: Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching the established pattern
- **Response deserialization**: Uses `resp.json::<T>().await` to deserialize the response body
- **Test naming**: Descriptive function names following `test_<feature>_<scenario>` pattern
- **Test coverage**: One test per test requirement from the task description:
  1. `test_severity_summary_with_advisories` -- valid SBOM with known advisories returns correct counts
  2. `test_severity_summary_sbom_not_found` -- non-existent SBOM ID returns 404
  3. `test_severity_summary_no_advisories` -- SBOM with no advisories returns all zeros
  4. `test_severity_summary_deduplicates_advisories` -- duplicate advisory links are deduplicated
- **Assertion messages**: Includes descriptive messages on key assertions for debugging clarity
