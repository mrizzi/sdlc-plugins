# File 3: tests/api/advisory_summary.rs

## Action: CREATE

## Purpose
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint,
covering all four test requirements specified in the task.

## Sibling Reference
Follows the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs` --
uses `assert_eq!(resp.status(), StatusCode::OK)` pattern, hits a real
PostgreSQL test database, follows `test_<endpoint>_<scenario>` naming.

## Detailed Changes

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test data: create SBOM, create advisories with specific severities,
    //  link them via sbom_advisory join table)
    let sbom_id = setup_test_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "High"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
        ("ADV-005", "Low"),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should contain correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);
    assert_eq!(summary.high, 2);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 1);
    assert_eq!(summary.total, 5);
}

/// Verifies that a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_test_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
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

/// Verifies that duplicate advisory links are deduplicated in severity counts.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = setup_test_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-001", "Critical"),  // duplicate link
        ("ADV-002", "High"),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then duplicate advisories should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // ADV-001 counted once despite duplicate link
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);     // only 2 unique advisories
}
```

## Notes
- All four test functions have `///` doc comments (required by SKILL.md Step 7).
- All tests use given-when-then section comments since they have distinct setup, action, and assertion phases.
- Tests use value-based assertions (checking specific counts), not just length checks.
- Tests follow `test_<endpoint>_<scenario>` naming convention from sibling test files.
- The `setup_test_sbom_with_advisories` helper is pseudocode -- the actual implementation would follow the test database setup patterns used in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- The exact test client setup, database fixture creation, and import paths would be adapted from the sibling test files during actual implementation.
- The test for deduplication specifically verifies acceptance criterion "Counts only unique advisories (deduplicates by advisory ID)" by linking the same advisory ID twice.
