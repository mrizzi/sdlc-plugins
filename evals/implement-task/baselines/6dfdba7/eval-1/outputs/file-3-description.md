# File 3: tests/api/advisory_summary.rs

## Action: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all test requirements from the task specification.

## Conventions Applied

- Follows the test pattern from sibling `advisory.rs` and `sbom.rs` in `tests/api/`.
- Tests hit a real PostgreSQL test database (consistent with project testing conventions).
- Uses `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Each test function sets up its own test data, makes an HTTP request, and asserts on the response.

## Detailed Changes

```rust
use reqwest::StatusCode;
use serde_json::Value;
use test_context::TestContext;
// ... other imports matching the existing test infrastructure

/// Test 1: Valid SBOM with known advisories returns correct severity counts
///
/// Covers acceptance criteria:
/// - GET /api/v2/sbom/{id}/advisory-summary returns { critical, high, medium, low, total }
/// - All severity levels default to 0 when no advisories exist at that level
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    let ctx = TestContext::setup().await;

    // Insert test SBOM
    let sbom_id = ctx.ingest_sbom("test-sbom-1").await;

    // Insert advisories with known severities:
    // 2 Critical, 3 High, 1 Medium, 0 Low
    ctx.ingest_advisory(sbom_id, "ADV-001", Severity::Critical).await;
    ctx.ingest_advisory(sbom_id, "ADV-002", Severity::Critical).await;
    ctx.ingest_advisory(sbom_id, "ADV-003", Severity::High).await;
    ctx.ingest_advisory(sbom_id, "ADV-004", Severity::High).await;
    ctx.ingest_advisory(sbom_id, "ADV-005", Severity::High).await;
    ctx.ingest_advisory(sbom_id, "ADV-006", Severity::Medium).await;

    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id)).await;
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);  // Defaults to 0
    assert_eq!(body["total"], 6);
}

/// Test 2: Non-existent SBOM ID returns 404
///
/// Covers acceptance criteria:
/// - Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
#[tokio::test]
async fn test_severity_summary_not_found() {
    let ctx = TestContext::setup().await;

    let fake_id = "00000000-0000-0000-0000-000000000000";
    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id)).await;
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Test 3: SBOM with no advisories returns all zeros
///
/// Covers acceptance criteria:
/// - All severity levels default to 0 when no advisories exist at that level
#[tokio::test]
async fn test_severity_summary_empty() {
    let ctx = TestContext::setup().await;

    // Insert SBOM with no advisories linked
    let sbom_id = ctx.ingest_sbom("test-sbom-empty").await;

    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id)).await;
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Test 4: Duplicate advisory links are deduplicated in the count
///
/// Covers acceptance criteria:
/// - Counts only unique advisories (deduplicates by advisory ID)
#[tokio::test]
async fn test_severity_summary_deduplication() {
    let ctx = TestContext::setup().await;

    let sbom_id = ctx.ingest_sbom("test-sbom-dedup").await;

    // Link the same advisory to the SBOM twice
    let adv_id = ctx.ingest_advisory(sbom_id, "ADV-DUP-001", Severity::High).await;
    ctx.link_advisory_to_sbom(adv_id, sbom_id).await; // duplicate link

    let resp = ctx.get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id)).await;
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["high"], 1);  // Should be 1, not 2
    assert_eq!(body["total"], 1); // Should be 1, not 2
}
```

## Notes

- The exact test infrastructure (TestContext, helper methods) would be determined by inspecting the existing test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`). The above uses plausible method names consistent with the project structure.
- The `tests/Cargo.toml` may need an update to include the new test file in the test binary, depending on how the workspace is configured (some Rust projects auto-discover test files, others require explicit listing).
- All four test requirements from the task specification are covered.
