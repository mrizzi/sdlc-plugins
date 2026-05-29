# File 6: Create `tests/api/advisory_summary.rs`

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Pre-Change Analysis

Before creating, read the sibling test files to understand test patterns:
- `tests/api/advisory.rs` — how advisory-related tests set up test data, make HTTP requests, and assert responses
- `tests/api/sbom.rs` — how SBOM-related tests create test SBOMs and validate status codes

## Full File Content

```rust
use axum::http::StatusCode;
use serde_json::Value;

// Test infrastructure imports (matching sibling test files)
use crate::common::test_app;

#[tokio::test]
async fn test_severity_summary_valid_sbom() {
    // Setup: create a test SBOM and link advisories with known severities
    // - 2 Critical advisories
    // - 3 High advisories  
    // - 1 Medium advisory
    // - 0 Low advisories
    let app = test_app().await;
    let sbom_id = app.create_test_sbom().await;
    app.link_advisory(sbom_id, "adv-1", "critical").await;
    app.link_advisory(sbom_id, "adv-2", "critical").await;
    app.link_advisory(sbom_id, "adv-3", "high").await;
    app.link_advisory(sbom_id, "adv-4", "high").await;
    app.link_advisory(sbom_id, "adv-5", "high").await;
    app.link_advisory(sbom_id, "adv-6", "medium").await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

#[tokio::test]
async fn test_severity_summary_nonexistent_sbom() {
    let app = test_app().await;

    let resp = app
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .await;

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Setup: create an SBOM with no linked advisories
    let app = test_app().await;
    let sbom_id = app.create_test_sbom().await;

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

#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Setup: link the same advisory to an SBOM multiple times
    let app = test_app().await;
    let sbom_id = app.create_test_sbom().await;
    app.link_advisory(sbom_id, "adv-dup", "high").await;
    app.link_advisory(sbom_id, "adv-dup", "high").await; // duplicate
    app.link_advisory(sbom_id, "adv-dup", "high").await; // duplicate

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    // Should count adv-dup only once despite 3 links
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Design Notes

- All four test cases from the task's "Test Requirements" section are covered
- Uses `assert_eq!(resp.status(), StatusCode::OK)` and `StatusCode::NOT_FOUND` matching the pattern in `tests/api/advisory.rs` and `tests/api/sbom.rs`
- Test data setup follows the test infrastructure patterns seen in sibling test files
- The deduplication test specifically verifies the acceptance criterion that duplicate advisory links are counted only once
