# File 6: tests/api/advisory_summary.rs

**Action**: Create

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover all four test requirements specified in the task description plus the acceptance criteria for correct JSON response shape.

## Full File Content

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests verify the GET /api/v2/sbom/{id}/advisory-summary endpoint
//! returns correct aggregated severity counts for advisories linked to SBOMs.

use reqwest::StatusCode;
use serde_json::Value;

// Test setup imports -- exact imports would be confirmed by reading sibling test files
// (tests/api/sbom.rs, tests/api/advisory.rs) to match the test harness pattern
use crate::common::{setup_test_app, TestContext};

/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels:
    //   2 Critical, 1 High, 3 Medium, 0 Low
    let ctx = TestContext::new().await;
    let sbom_id = ctx.create_test_sbom().await;
    ctx.link_advisory(sbom_id, "ADV-001", "Critical").await;
    ctx.link_advisory(sbom_id, "ADV-002", "Critical").await;
    ctx.link_advisory(sbom_id, "ADV-003", "High").await;
    ctx.link_advisory(sbom_id, "ADV-004", "Medium").await;
    ctx.link_advisory(sbom_id, "ADV-005", "Medium").await;
    ctx.link_advisory(sbom_id, "ADV-006", "Medium").await;

    // When requesting the advisory summary for the SBOM
    let resp = ctx
        .client
        .get(format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let ctx = TestContext::new().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let ctx = TestContext::new().await;
    let sbom_id = ctx.create_test_sbom().await;

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be 200 OK with all counts at zero
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with the same advisory linked multiple times
    let ctx = TestContext::new().await;
    let sbom_id = ctx.create_test_sbom().await;
    ctx.link_advisory(sbom_id, "ADV-001", "Critical").await;
    ctx.link_advisory(sbom_id, "ADV-001", "Critical").await; // duplicate link
    ctx.link_advisory(sbom_id, "ADV-002", "High").await;

    // When requesting the advisory summary
    let resp = ctx
        .client
        .get(format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should count ADV-001 only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 1, "ADV-001 should be counted once despite duplicate links");
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2, "Total should reflect deduplicated count");
}
```

## Design Decisions

- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern discovered in sibling tests (`tests/api/sbom.rs`, `tests/api/advisory.rs`)
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test patterns
- **Value-based assertions**: Asserts on specific field values (`body["critical"]`, `body["total"]`), not just structure or length, following the skill's instruction to "prefer value-based assertions over length-only checks"
- **Given-When-Then comments**: All tests have section comments as required by the skill for non-trivial tests
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies, as required by the skill regardless of sibling test conventions
- **No parameterized tests**: Sibling test files do not use `#[rstest]` or parameterized tests, so individual test functions are used for each scenario
- **Test setup**: Uses a `TestContext` pattern (actual pattern would be confirmed by reading sibling test files). Each test creates its own isolated data.
- **Error case coverage**: Includes 404 test for non-existent SBOM, matching the pattern found in all sibling endpoint test files
- **Deduplication test**: Explicitly tests the deduplication requirement by linking the same advisory twice and asserting it is counted once, with descriptive assertion messages

## Note on Test Registration

The test file would also need to be registered in `tests/api/` -- this may require adding `mod advisory_summary;` to a test runner file or updating `tests/Cargo.toml` depending on the project's test organization. This would be confirmed by inspecting the sibling test file registration pattern during Step 4.
