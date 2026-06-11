# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint,
covering all four test requirements specified in the task.

## Detailed Changes

Create a new test file with the following contents:

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests the GET /api/v2/sbom/{id}/advisory-summary endpoint, verifying
//! correct severity counting, 404 handling, empty results, and deduplication.

use actix_http::StatusCode;
use test_context::TestContext;
// Additional imports would be confirmed from sibling test files (advisory.rs, sbom.rs)

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Seeds the database with an SBOM linked to advisories of known severities and
/// asserts that each severity level count matches the expected values.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM linked to advisories with known severities:
    // - 2 critical, 1 high, 3 medium, 1 low
    let ctx = TestContext::setup().await;
    let sbom_id = ctx.create_test_sbom().await;
    ctx.link_advisory(sbom_id, "ADV-001", "critical").await;
    ctx.link_advisory(sbom_id, "ADV-002", "critical").await;
    ctx.link_advisory(sbom_id, "ADV-003", "high").await;
    ctx.link_advisory(sbom_id, "ADV-004", "medium").await;
    ctx.link_advisory(sbom_id, "ADV-005", "medium").await;
    ctx.link_advisory(sbom_id, "ADV-006", "medium").await;
    ctx.link_advisory(sbom_id, "ADV-007", "low").await;

    // When requesting the advisory summary for the SBOM
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should return 200 with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 2, "expected 2 critical advisories");
    assert_eq!(body["high"], 1, "expected 1 high advisory");
    assert_eq!(body["medium"], 3, "expected 3 medium advisories");
    assert_eq!(body["low"], 1, "expected 1 low advisory");
    assert_eq!(body["total"], 7, "expected 7 total advisories");
}

/// Verifies that a non-existent SBOM ID returns a 404 status code.
///
/// Ensures the endpoint is consistent with other SBOM endpoints in returning
/// 404 for unknown resource IDs.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let ctx = TestContext::setup().await;
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await;

    // Then the response should return 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
///
/// Ensures all severity counts default to 0 and total is 0 when no
/// advisories are linked to the SBOM.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let ctx = TestContext::setup().await;
    let sbom_id = ctx.create_test_sbom().await;

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should return 200 with all zeros
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 0, "expected 0 critical advisories");
    assert_eq!(body["high"], 0, "expected 0 high advisories");
    assert_eq!(body["medium"], 0, "expected 0 medium advisories");
    assert_eq!(body["low"], 0, "expected 0 low advisories");
    assert_eq!(body["total"], 0, "expected 0 total advisories");
}

/// Verifies that duplicate advisory links are deduplicated in the count.
///
/// Seeds the database with an SBOM linked to the same advisory multiple times
/// (via duplicate entries in the sbom_advisory join table) and asserts that
/// each advisory is counted only once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links
    let ctx = TestContext::setup().await;
    let sbom_id = ctx.create_test_sbom().await;
    // Link the same advisory three times
    ctx.link_advisory(sbom_id, "ADV-001", "critical").await;
    ctx.link_advisory_duplicate(sbom_id, "ADV-001", "critical").await;
    ctx.link_advisory_duplicate(sbom_id, "ADV-001", "critical").await;
    // Link a different advisory once
    ctx.link_advisory(sbom_id, "ADV-002", "high").await;

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then duplicates should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 1, "expected 1 critical (deduplicated from 3 links)");
    assert_eq!(body["high"], 1, "expected 1 high advisory");
    assert_eq!(body["total"], 2, "expected 2 total unique advisories");
}
```

**Note**: The exact test setup helpers (`TestContext`, `create_test_sbom`, `link_advisory`),
imports, and HTTP client API would be confirmed by reading the actual sibling test files
(`tests/api/advisory.rs`, `tests/api/sbom.rs`) via Serena or Read. The test structure
above follows the conventions discovered from sibling analysis:

- `#[tokio::test]` for async integration tests
- `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
- Value-based assertions on specific fields (not just length checks)
- `test_<endpoint>_<scenario>` naming pattern

## Test Conventions Applied

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling tests
- **Response validation**: validates specific field values (`critical`, `high`, `medium`, `low`, `total`) with descriptive messages
- **Error case**: includes 404 test matching the sibling pattern
- **Test naming**: `test_advisory_summary_<scenario>` following `test_<endpoint>_<scenario>` convention
- **Documentation**: every test function has a `///` doc comment explaining what it verifies (AI-generated standard)
- **Given-when-then**: section comments in each non-trivial test for navigability
- **Value assertions**: asserts on actual severity count values, not just list lengths
- **Test organization**: all tests for this endpoint in a single file, matching sibling file organization
