# File 3: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests covering all acceptance criteria and test requirements for the advisory severity summary endpoint.

## Detailed Changes

Create a new test file with four test functions:

```rust
use reqwest::StatusCode;
use serde_json::Value;
use uuid::Uuid;

// Test helper imports (matching sibling test files like tests/api/advisory.rs)
use crate::common::setup_test_server;

/// Test that a valid SBOM with known advisories returns correct severity counts.
///
/// Covers acceptance criteria:
/// - GET /api/v2/sbom/{id}/advisory-summary returns { critical, high, medium, low, total }
/// - Counts only unique advisories (deduplicates by advisory ID)
#[tokio::test]
async fn test_get_severity_summary_with_advisories() {
    let server = setup_test_server().await;

    // Ingest a test SBOM and link advisories with known severities:
    // - 2 Critical, 1 High, 3 Medium, 0 Low
    let sbom_id = server.ingest_test_sbom("test-sbom-with-advisories").await;
    server.link_advisory(sbom_id, "ADV-001", "Critical").await;
    server.link_advisory(sbom_id, "ADV-002", "Critical").await;
    server.link_advisory(sbom_id, "ADV-003", "High").await;
    server.link_advisory(sbom_id, "ADV-004", "Medium").await;
    server.link_advisory(sbom_id, "ADV-005", "Medium").await;
    server.link_advisory(sbom_id, "ADV-006", "Medium").await;

    let resp = server
        .client
        .get(format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Test that a non-existent SBOM ID returns 404.
///
/// Covers acceptance criteria:
/// - Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
#[tokio::test]
async fn test_get_severity_summary_not_found() {
    let server = setup_test_server().await;
    let fake_id = Uuid::new_v4();

    let resp = server
        .client
        .get(format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .unwrap();

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test that an SBOM with no advisories returns all zeros.
///
/// Covers acceptance criteria:
/// - All severity levels default to 0 when no advisories exist at that level
#[tokio::test]
async fn test_get_severity_summary_empty() {
    let server = setup_test_server().await;
    let sbom_id = server.ingest_test_sbom("test-sbom-empty").await;

    let resp = server
        .client
        .get(format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Test that duplicate advisory links are deduplicated in the count.
///
/// Covers test requirement:
/// - Duplicate advisory links are deduplicated in the count
#[tokio::test]
async fn test_get_severity_summary_deduplicates() {
    let server = setup_test_server().await;
    let sbom_id = server.ingest_test_sbom("test-sbom-dedup").await;

    // Link the same advisory twice (simulating duplicate join table entries)
    server.link_advisory(sbom_id, "ADV-100", "High").await;
    server.link_advisory(sbom_id, "ADV-100", "High").await; // duplicate
    server.link_advisory(sbom_id, "ADV-101", "Low").await;

    let resp = server
        .client
        .get(format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    // ADV-100 should only be counted once despite duplicate link
    assert_eq!(body["high"], 1);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 2);
}
```

## Conventions Applied

- **File location**: `tests/api/advisory_summary.rs`, following the sibling pattern of `tests/api/advisory.rs`, `tests/api/sbom.rs`.
- **Test naming**: `test_<action>_<scenario>` pattern (e.g., `test_get_severity_summary_with_advisories`).
- **Assertions**: Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests.
- **Test database**: Uses a real PostgreSQL test database via `setup_test_server()` (matching existing test infrastructure).
- **Four test cases**: Directly maps to the four test requirements in the task description.
- **Deduplication test**: Explicitly links the same advisory ID twice and verifies the count is 1, not 2.

## Note on Test Helpers

The exact test helper API (`setup_test_server`, `ingest_test_sbom`, `link_advisory`) would need to be verified against the actual test infrastructure. The patterns shown here are representative; actual helper method names would be confirmed by inspecting `tests/api/sbom.rs` and `tests/api/advisory.rs` at implementation time.
