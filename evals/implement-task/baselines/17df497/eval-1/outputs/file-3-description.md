# File 3: tests/api/advisory_summary.rs

**Action:** CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests verify correct severity counting, 404 handling, zero-advisory defaults, and deduplication.

## Detailed Changes

### Test Functions

```rust
use axum::http::StatusCode;
use crate::advisory::model::severity_summary::SeveritySummary;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at various severity levels seeded in the test database
    // (e.g., 2 Critical, 3 High, 1 Medium, 0 Low)
    let sbom_id = setup_sbom_with_advisories(vec![
        ("adv-1", "Critical"),
        ("adv-2", "Critical"),
        ("adv-3", "High"),
        ("adv-4", "High"),
        ("adv-5", "High"),
        ("adv-6", "Medium"),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the severity counts match the seeded data
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory summary for that ID
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And all severity counts are zero
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = setup_sbom_with_advisories(vec![
        ("adv-1", "Critical"),
        ("adv-1", "Critical"),  // duplicate link
        ("adv-2", "High"),
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And duplicate advisories are counted only once
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // adv-1 counted once, not twice
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);  // 2 unique advisories, not 3
}
```

### Design Decisions

- **Real database tests**: integration tests hit a real PostgreSQL test database, matching the convention in sibling `tests/api/` files.
- **Separate test file**: `advisory_summary.rs` is a new file rather than appending to `advisory.rs`, since the endpoint is semantically distinct (SBOM-scoped aggregation vs. advisory CRUD).
- **Value-based assertions**: each test asserts on specific field values (e.g., `assert_eq!(summary.critical, 2)`) rather than just checking response length or status, following the skill's guidance to prefer value-based assertions.
- **Given-When-Then comments**: non-trivial tests include section comments for navigability.
- **Doc comments on every test**: each test function has a `///` doc comment explaining what it verifies.

### Conventions Applied

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling tests
- **Error case coverage**: 404 test for non-existent SBOM ID, matching sibling patterns
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`)
- **Test organization**: one test file for the advisory summary endpoint group
