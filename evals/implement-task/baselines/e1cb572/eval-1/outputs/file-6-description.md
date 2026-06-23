# File 6: tests/api/advisory_summary.rs

**Action:** CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all 4 test requirements from the task description.

## Detailed Changes

```rust
//! Integration tests for the advisory severity summary endpoint.

use reqwest::StatusCode;
// Additional imports would be determined by inspecting sibling test files
// (tests/api/sbom.rs, tests/api/advisory.rs) for test utilities, fixtures,
// and database setup patterns.

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Creates an SBOM with advisories at each severity level and asserts the endpoint
/// returns the exact expected counts per level plus the correct total.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM linked to advisories with known severities:
    //   2 Critical, 3 High, 1 Medium, 0 Low
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisories(&app, sbom_id, &[
        ("critical", 2),
        ("high", 3),
        ("medium", 1),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response status is 200 and counts match
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = uuid::Uuid::new_v4();

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await
        .unwrap();

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_empty_returns_all_zeros() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
///
/// When the same advisory is linked to an SBOM multiple times (via different
/// sbom_advisory join records), it should be counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplicates_by_advisory_id() {
    // Given an SBOM with a single advisory linked twice
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, "high").await;
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await; // duplicate link

    // When requesting the advisory summary
    let resp = app
        .client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Conventions Applied

- **Test location:** File placed in `tests/api/` alongside sibling test files (`sbom.rs`, `advisory.rs`, `search.rs`)
- **File naming:** Named `advisory_summary.rs` following the entity/feature naming convention
- **Assertion style:** Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern matching sibling tests
- **Response validation:** Deserializes JSON body and asserts on specific field values (not just length checks), per skill requirement for value-based assertions
- **Error case coverage:** Includes 404 test with `StatusCode::NOT_FOUND` matching sibling test patterns
- **Test naming:** Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_returns_correct_counts`)
- **Documentation:** Every test function has a `///` doc comment explaining what it verifies, per skill requirement
- **Given-When-Then:** Non-trivial tests include `// Given`, `// When`, `// Then` section comments per skill requirement
- **Test database:** Tests use a real PostgreSQL test database (not mocked), consistent with project convention

## Notes

- The exact test setup functions (`setup_test_app`, `create_test_sbom`, `create_test_advisory`, `link_advisory_to_sbom`) would be derived from inspecting sibling test files to find existing test utilities
- The HTTP client usage pattern (direct `reqwest` vs an app test wrapper) would match whatever pattern `tests/api/sbom.rs` and `tests/api/advisory.rs` use
- Additional test module registration in `tests/api/mod.rs` (if it exists) would be needed -- this would be discovered during Step 4 code inspection
- Parameterized tests were considered for the severity count test but rejected because each test case has meaningfully different setup (empty SBOM, populated SBOM, duplicate links) -- the Meszaros heuristic favors individual tests here
