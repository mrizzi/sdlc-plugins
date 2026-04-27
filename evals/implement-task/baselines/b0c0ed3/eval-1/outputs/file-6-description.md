# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task specification.

## Detailed Changes

Create a new file with the following content:

```rust
use axum::http::StatusCode;
use serde_json::Value;

// Test harness imports — matches pattern from sibling test files (advisory.rs, sbom.rs)
use crate::common::TestApp;

/// Test that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    let app = TestApp::new().await;

    // Setup: ingest an SBOM and link advisories with known severities.
    let sbom_id = app.ingest_test_sbom("test-sbom-1").await;
    app.link_advisory_to_sbom(&sbom_id, "ADV-001", "Critical").await;
    app.link_advisory_to_sbom(&sbom_id, "ADV-002", "High").await;
    app.link_advisory_to_sbom(&sbom_id, "ADV-003", "High").await;
    app.link_advisory_to_sbom(&sbom_id, "ADV-004", "Medium").await;
    app.link_advisory_to_sbom(&sbom_id, "ADV-005", "Low").await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 2);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 5);
}

/// Test that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    let app = TestApp::new().await;

    let resp = app
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .await;

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty() {
    let app = TestApp::new().await;

    // Setup: ingest an SBOM with no linked advisories.
    let sbom_id = app.ingest_test_sbom("test-sbom-empty").await;

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
async fn test_advisory_summary_deduplication() {
    let app = TestApp::new().await;

    let sbom_id = app.ingest_test_sbom("test-sbom-dedup").await;

    // Link the same advisory twice to the SBOM.
    app.link_advisory_to_sbom(&sbom_id, "ADV-DUP-001", "Critical").await;
    app.link_advisory_to_sbom(&sbom_id, "ADV-DUP-001", "Critical").await;
    // And a distinct advisory.
    app.link_advisory_to_sbom(&sbom_id, "ADV-DUP-002", "Low").await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    // ADV-DUP-001 should be counted only once despite two links.
    assert_eq!(body["critical"], 1);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 2);
}
```

## Design Decisions

- **Test harness**: Uses the same `TestApp` pattern observed in `tests/api/sbom.rs` and `tests/api/advisory.rs`. The exact helper method names (`ingest_test_sbom`, `link_advisory_to_sbom`) are hypothetical but follow the project's test setup conventions. During actual implementation, these would be verified against the real test harness.
- **Real database**: Tests hit a real PostgreSQL test database per the project convention (no mocking).
- **Assertions**: Use `assert_eq!(resp.status(), StatusCode::...)` matching sibling tests.
- **JSON parsing**: Uses `serde_json::Value` for flexible assertion on response body fields.

## Convention Conformance

- File placed in `tests/api/` alongside `sbom.rs`, `advisory.rs`, `search.rs`.
- `#[tokio::test]` async test functions per project convention.
- Status code assertions match the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Each test is independent, sets up its own data, and makes a single logical assertion group.

## Note

The test file may also need to be registered in `tests/api/mod.rs` (if one exists) via `mod advisory_summary;`. This would be verified during actual implementation by inspecting the test module structure. If tests are auto-discovered (no `mod.rs`), no additional registration is needed.
