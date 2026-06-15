# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose
Integration tests for the new GET /api/v2/sbom/{id}/advisory-summary endpoint, covering all four test requirements from the task.

## Detailed Changes

Create a new test file with the following content:

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns the correct
/// severity count breakdown.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (setup: create test SBOM, link advisories with specific severities
    //  e.g., 2 Critical, 1 High, 3 Medium, 0 Low)
    let sbom_id = create_test_sbom().await;
    link_advisory(sbom_id, "critical").await;
    link_advisory(sbom_id, "critical").await;
    link_advisory(sbom_id, "high").await;
    link_advisory(sbom_id, "medium").await;
    link_advisory(sbom_id, "medium").await;
    link_advisory(sbom_id, "medium").await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should contain correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 status code,
/// consistent with other SBOM endpoints.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await;

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero
/// severity counts.
#[tokio::test]
async fn test_severity_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let sbom_id = create_test_sbom().await;

    // When requesting the advisory summary
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

/// Verifies that duplicate advisory links for the same advisory are
/// deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = create_test_sbom().await;
    let advisory_id = create_test_advisory("high").await;
    link_advisory_by_id(sbom_id, advisory_id).await;
    link_advisory_by_id(sbom_id, advisory_id).await; // duplicate link

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the advisory should only be counted once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1); // Not 2
    assert_eq!(summary.total, 1); // Not 2
}
```

## Conventions Applied
- **Test location**: placed in `tests/api/` directory following sibling test file pattern (`sbom.rs`, `advisory.rs`)
- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the established pattern from sibling tests
- **Error case coverage**: includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` per sibling test convention
- **Test naming**: follows `test_<endpoint>_<scenario>` pattern (e.g., `test_severity_summary_with_known_advisories`)
- **Value-based assertions**: asserts on actual severity count values (not just lengths/counts), per skill guidance on preferring value-based assertions
- **Documentation**: every test function has a `///` doc comment explaining what it verifies
- **Given-when-then**: all tests use `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases
- **Async tests**: uses `#[tokio::test]` for async test execution, matching the Rust backend testing pattern
- **Real database**: tests hit a real PostgreSQL test database per the project's testing convention (not mocked)

## Test Requirements Coverage
1. Test that a valid SBOM with known advisories returns correct severity counts -- `test_severity_summary_with_known_advisories`
2. Test that a non-existent SBOM ID returns 404 -- `test_severity_summary_nonexistent_sbom_returns_404`
3. Test that an SBOM with no advisories returns all zeros -- `test_severity_summary_no_advisories_returns_zeros`
4. Test that duplicate advisory links are deduplicated in the count -- `test_severity_summary_deduplicates_advisories`
