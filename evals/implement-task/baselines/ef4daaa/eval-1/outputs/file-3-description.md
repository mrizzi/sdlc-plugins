# File 3: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Covers all four test cases specified in the Test Requirements: valid SBOM with known advisories, non-existent SBOM (404), SBOM with no advisories (all zeros), and deduplication of advisory links.

## Files inspected before writing

Before creating this file, the following sibling test files would be inspected:

- `tests/api/advisory.rs` -- PRIMARY SIBLING: `mcp__serena_backend__get_symbols_overview` to understand test setup patterns (how advisories are created in the test database), assertion style, response deserialization, and test naming conventions
- `tests/api/sbom.rs` -- SECONDARY SIBLING: to understand how SBOM entities are created for testing, and how SBOM-scoped endpoint tests are structured (since our endpoint is SBOM-scoped)
- `tests/api/search.rs` -- TERTIARY SIBLING: for additional pattern confirmation
- `tests/Cargo.toml` -- to check for `rstest` or other parameterized test dependencies

## Conventions applied

- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Response deserialization: `.json::<SeveritySummary>()` after asserting status
- Test naming: `test_<endpoint>_<scenario>` pattern
- Test setup: Uses real PostgreSQL test database; creates test SBOMs and advisories via ingestor/service layer
- Value-based assertions: Asserts on actual field values (e.g., `assert_eq!(summary.critical, 2)`), not just collection lengths
- Doc comments on every test function (AI-generated test standard per SKILL.md Step 7)
- Given-When-Then section comments for non-trivial tests

## Detailed changes

```rust
use axum::http::StatusCode;
use common::model::SeveritySummary;
// Additional imports for test setup, HTTP client, and test database utilities
// (exact imports would be determined by inspecting sibling test files)

/// Verifies that a valid SBOM with known advisories returns the correct severity
/// counts, with each severity level accurately reflecting the linked advisories.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM linked to advisories with known severity levels:
    // 2 Critical, 3 High, 1 Medium, 0 Low
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "critical").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "high").await;
    create_test_advisory(&app, sbom_id, "medium").await;

    // When requesting the advisory summary for the SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should contain the correct severity breakdown
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found status, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for the non-existent SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns a summary with all
/// severity counts set to zero and a total of zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links (same advisory linked to the same SBOM
/// multiple times) are deduplicated, so each unique advisory is counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with a single advisory linked twice (duplicate join entries)
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "high").await;
    // Create a duplicate link for the same advisory to the same SBOM
    link_advisory_to_sbom(&app, advisory_id, sbom_id).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 1);
    // Other severity levels should be zero
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
}
```

## Key design decisions

1. **Value-based assertions**: Each test asserts on specific field values (`assert_eq!(summary.critical, 2)`) rather than just checking the response status or field presence. This ensures regressions in the aggregation logic produce meaningful failure messages.
2. **Given-When-Then comments**: All four tests have distinct setup, action, and assertion phases, so all include `// Given`, `// When`, `// Then` section comments.
3. **Doc comments**: Every test function has a `///` doc comment explaining what it verifies, per the SKILL.md Step 7 requirement for AI-generated tests.
4. **Deduplication test setup**: The deduplication test creates a single advisory and links it twice to the same SBOM, then verifies the count is 1 (not 2). This directly tests AC-3 (counts only unique advisories).
5. **Not parameterized**: These four tests have different setup requirements (different numbers of advisories, existence vs. non-existence of SBOM, duplicate link creation), making parameterization inappropriate per the Meszaros heuristic. Each test has a distinct setup phase.

## Integration points

- Tests hit the `GET /api/v2/sbom/{id}/advisory-summary` endpoint (file 2)
- Uses `SeveritySummary` for response deserialization (file 1)
- Test setup creates SBOMs and advisories via the existing test infrastructure (patterns observed in `tests/api/sbom.rs` and `tests/api/advisory.rs`)
- The test file would need to be registered in `tests/Cargo.toml` if the test harness requires explicit module declaration
