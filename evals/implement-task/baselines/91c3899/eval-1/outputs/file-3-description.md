# File 3: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the four test requirements from the task description.

## Sibling Reference

Modeled after `tests/api/advisory.rs` and `tests/api/sbom.rs` which:
- Use `#[tokio::test]` for async tests
- Hit a real PostgreSQL test database
- Assert status codes with `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Deserialize response bodies for field-level assertions
- Include 404 tests for non-existent resources
- Follow `test_<endpoint>_<scenario>` naming convention

## Detailed Changes

```rust
use reqwest::StatusCode;
use serde::Deserialize;

/// Response struct for deserializing the advisory severity summary in tests.
#[derive(Debug, Deserialize)]
struct SeveritySummaryResponse {
    critical: u32,
    high: u32,
    medium: u32,
    low: u32,
    total: u32,
}

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with known advisories at different severity levels
    // (setup: create test SBOM and link advisories with known severities via test fixtures)
    let sbom_id = setup_sbom_with_advisories(vec![
        ("advisory-1", "Critical"),
        ("advisory-2", "High"),
        ("advisory-3", "High"),
        ("advisory-4", "Medium"),
    ]).await;

    // When requesting the advisory summary for this SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should be 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummaryResponse = resp.json().await.expect("Failed to parse response");
    assert_eq!(summary.critical, 1, "Expected 1 Critical advisory");
    assert_eq!(summary.high, 2, "Expected 2 High advisories");
    assert_eq!(summary.medium, 1, "Expected 1 Medium advisory");
    assert_eq!(summary.low, 0, "Expected 0 Low advisories");
    assert_eq!(summary.total, 4, "Expected 4 total advisories");
}

/// Verifies that a non-existent SBOM ID returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory summary for this SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary for this SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the response should be 200 OK with all zero counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummaryResponse = resp.json().await.expect("Failed to parse response");
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = setup_sbom_with_advisories(vec![
        ("advisory-1", "Critical"),
        ("advisory-1", "Critical"),  // duplicate link
        ("advisory-2", "High"),
    ]).await;

    // When requesting the advisory summary for this SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("Failed to send request");

    // Then the counts should reflect unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummaryResponse = resp.json().await.expect("Failed to parse response");
    assert_eq!(summary.critical, 1, "Duplicate advisory should be counted once");
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 2, "Total should count unique advisories only");
}
```

## Design Notes

- Every test function has a `///` documentation comment explaining what it verifies (per skill requirement)
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments (per skill requirement)
- Value-based assertions are used (checking specific counts) rather than length-only checks
- Assert messages are included where counts might be ambiguous to aid debugging
- The `SeveritySummaryResponse` test struct mirrors the production `SeveritySummary` for deserialization
- Test naming follows `test_advisory_summary_<scenario>` pattern consistent with sibling test files
- Test setup functions (`setup_sbom_with_advisories`) would be implemented using the project's existing test fixture patterns, seeding the PostgreSQL test database with the necessary SBOM and advisory records linked via the `sbom_advisory` join table
- The deduplication test specifically creates duplicate links to verify the acceptance criterion
