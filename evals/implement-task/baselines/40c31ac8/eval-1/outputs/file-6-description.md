# File 6: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Sibling Reference

Follows the patterns established by:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Key test patterns extracted from siblings:
- Tests hit a real PostgreSQL test database
- Status code assertions: `assert_eq!(resp.status(), StatusCode::OK)`
- Error case: `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for non-existent IDs
- Response body deserialization followed by field-level value assertions
- Test naming: `test_<endpoint>_<scenario>` pattern

## Detailed Changes

```rust
use axum::http::StatusCode;
use serde_json::Value;
// ... other test infrastructure imports matching sibling test files

/// Verifies that a valid SBOM with known advisories returns the correct
/// severity counts broken down by critical, high, medium, and low levels.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test SBOM and link advisories via the test database)
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "medium").await;

    // When requesting the advisory summary for the SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response contains the correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 4);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for the non-existent SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then a 404 Not Found response is returned
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity
/// counts as zero and a total of zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated
/// in the severity count, so each advisory is counted only once regardless
/// of how many times it appears in the sbom_advisory join table.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with a duplicate advisory link (same advisory linked twice)
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "high").await;
    // Link the same advisory again to simulate a duplicate
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["high"], 1); // Not 2, despite two links
    assert_eq!(body["total"], 1);
}
```

## Convention Conformance

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization -- matches sibling test pattern
- **Response validation**: Asserts on specific field values (not just collection lengths) -- matches the "prefer value-based assertions" requirement
- **Error case**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` -- matches sibling error case pattern
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`)
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies
- **Given-When-Then**: All tests include `// Given`, `// When`, `// Then` section comments (all are non-trivial with distinct setup/action/assertion phases)
- **Parameterized tests**: Not used -- individual test functions are written because each test has a different setup (different fixture creation), and sibling test files would need to be checked for `#[rstest]` usage before introducing parameterized tests

## Notes

- The exact test infrastructure (app setup, fixture creation helpers) would be determined by reading sibling test files with Serena. The helper functions shown (`setup_test_app`, `create_test_sbom`, `create_test_advisory`, `link_advisory_to_sbom`) represent the conceptual test setup and would be adapted to match the actual test infrastructure.
- The `tests/Cargo.toml` may need to be checked for any additional test dependencies, but this is a low-risk check since sibling tests already exist.
