# File 6: tests/api/advisory_summary.rs

## Change Type: Create

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements specified in the task.

## Detailed Changes

### Full file content

```rust
use axum::http::StatusCode;
use serde_json::Value;

mod common;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Creates a test SBOM linked to advisories of known severities and confirms the
/// endpoint returns the expected count for each severity level.
#[tokio::test]
async fn test_advisory_summary_valid_sbom_with_advisories() {
    // Given an SBOM linked to advisories with known severities:
    // 2 Critical, 1 High, 1 Medium, 0 Low
    let app = common::setup_test_app().await;
    let sbom_id = common::create_test_sbom(&app).await;
    common::create_test_advisory(&app, sbom_id, "critical").await;
    common::create_test_advisory(&app, sbom_id, "critical").await;
    common::create_test_advisory(&app, sbom_id, "high").await;
    common::create_test_advisory(&app, sbom_id, "medium").await;

    // When requesting the advisory summary for the SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should be 200 with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2, "expected 2 critical advisories");
    assert_eq!(body["high"], 1, "expected 1 high advisory");
    assert_eq!(body["medium"], 1, "expected 1 medium advisory");
    assert_eq!(body["low"], 0, "expected 0 low advisories");
    assert_eq!(body["total"], 4, "expected 4 total advisories");
}

/// Verifies that a non-existent SBOM ID returns a 404 response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = common::setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for a non-existent SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = common::setup_test_app().await;
    let sbom_id = common::create_test_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
///
/// If the same advisory is linked to an SBOM multiple times via the sbom_advisory join
/// table, it should only be counted once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate links to the same advisory
    let app = common::setup_test_app().await;
    let sbom_id = common::create_test_sbom(&app).await;
    let advisory_id = common::create_test_advisory(&app, sbom_id, "high").await;
    // Create a duplicate link for the same advisory
    common::link_advisory_to_sbom(&app, advisory_id, sbom_id).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: Value = resp.json().await;
    assert_eq!(body["high"], 1, "duplicate advisory should be counted once");
    assert_eq!(body["total"], 1, "total should reflect deduplicated count");
}
```

## Conventions Applied

- **Test file location**: `tests/api/advisory_summary.rs` -- follows the `tests/api/<domain>.rs` pattern from siblings (`sbom.rs`, `advisory.rs`, `search.rs`)
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` -- matches the exact pattern used in sibling test files
- **Response validation**: Deserialized JSON body with specific field-value assertions (not just length checks) -- follows the "prefer value-based assertions over length-only checks" guidance
- **Error case coverage**: Includes 404 test for non-existent SBOM -- matches sibling pattern where all endpoint tests include a 404 case
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom_with_advisories`) -- matches discovered test naming convention
- **Documentation comments**: Every test function has a `///` doc comment explaining what it verifies
- **Given-When-Then structure**: All non-trivial tests include `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases
- **Test database**: Tests use real PostgreSQL test database through `common::setup_test_app()` -- matches sibling test infrastructure
- **Async tests**: Uses `#[tokio::test]` for async test execution -- matches Axum/async Rust test conventions

## Test Coverage Matrix

| Test Requirement | Test Function | Acceptance Criterion |
|---|---|---|
| Valid SBOM with known advisories returns correct counts | `test_advisory_summary_valid_sbom_with_advisories` | AC 1, 4, 5 |
| Non-existent SBOM ID returns 404 | `test_advisory_summary_nonexistent_sbom_returns_404` | AC 2 |
| SBOM with no advisories returns all zeros | `test_advisory_summary_no_advisories_returns_zeros` | AC 4 |
| Duplicate advisory links are deduplicated | `test_advisory_summary_deduplicates_advisory_links` | AC 3 |

## Notes

- The test module registration in `tests/Cargo.toml` may need to be updated to include the new test file, depending on the project's test configuration. If tests are auto-discovered via `#[cfg(test)]` or glob patterns, no changes are needed.
- The `common` module referenced in the tests represents shared test utilities for setup, teardown, and fixture creation. The actual helper functions (`create_test_sbom`, `create_test_advisory`, `link_advisory_to_sbom`) would need to be added or confirmed to exist in the common test helpers.
