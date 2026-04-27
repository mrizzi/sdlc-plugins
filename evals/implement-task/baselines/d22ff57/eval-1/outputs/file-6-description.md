# File 6: tests/api/advisory_summary.rs

## Action: CREATE

## Summary

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests
cover all four test requirements from the task description plus deduplication verification.

## Full File Content

```rust
use reqwest::StatusCode;
use serde::Deserialize;

/// Response struct for deserializing the severity summary endpoint response.
#[derive(Debug, Deserialize, PartialEq, Eq)]
struct SeveritySummaryResponse {
    critical: u32,
    high: u32,
    medium: u32,
    low: u32,
    total: u32,
}

/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_severity_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels:
    //   2 Critical, 1 High, 3 Medium, 0 Low
    let sbom_id = setup_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "Critical"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
        ("ADV-005", "Medium"),
        ("ADV-006", "Medium"),
    ])
    .await;

    // When requesting the advisory summary for the SBOM
    let resp = client()
        .get(format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .unwrap();

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the severity counts match the expected values
    let summary: SeveritySummaryResponse = resp.json().await.unwrap();
    assert_eq!(summary.critical, 2, "expected 2 Critical advisories");
    assert_eq!(summary.high, 1, "expected 1 High advisory");
    assert_eq!(summary.medium, 3, "expected 3 Medium advisories");
    assert_eq!(summary.low, 0, "expected 0 Low advisories");
    assert_eq!(summary.total, 6, "expected 6 total advisories");
}

/// Verifies that requesting a severity summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_nonexistent_sbom() {
    // Given an SBOM ID that does not exist in the database
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client()
        .get(format!("/api/v2/sbom/{nonexistent_id}/advisory-summary"))
        .send()
        .await
        .unwrap();

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_severity_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client()
        .get(format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .unwrap();

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And all severity counts are 0
    let summary: SeveritySummaryResponse = resp.json().await.unwrap();
    assert_eq!(
        summary,
        SeveritySummaryResponse {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        },
        "all severity counts should be zero for an SBOM with no advisories"
    );
}

/// Verifies that duplicate advisory links in the sbom_advisory join table are
/// deduplicated so each advisory is counted only once.
#[tokio::test]
async fn test_severity_summary_deduplication() {
    // Given an SBOM where the same advisory is linked multiple times
    //   ADV-001 (Critical) appears 3 times in the join table
    //   ADV-002 (High) appears 2 times in the join table
    let sbom_id = setup_sbom_with_duplicate_advisory_links(vec![
        ("ADV-001", "Critical", 3), // 3 duplicate links
        ("ADV-002", "High", 2),     // 2 duplicate links
    ])
    .await;

    // When requesting the advisory summary
    let resp = client()
        .get(format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .unwrap();

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And each advisory is counted only once despite multiple links
    let summary: SeveritySummaryResponse = resp.json().await.unwrap();
    assert_eq!(summary.critical, 1, "ADV-001 should be counted once despite 3 links");
    assert_eq!(summary.high, 1, "ADV-002 should be counted once despite 2 links");
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2, "total should reflect unique advisories only");
}
```

## Design Decisions

- **Value-based assertions:** Each test asserts on specific field values (not just `summary.total` or collection length), so failures reveal exactly which severity level is wrong.
- **Struct-level comparison:** The empty SBOM test uses full struct comparison via `assert_eq!` with `PartialEq` to verify all fields are zero in a single assertion.
- **Descriptive messages:** Each `assert_eq!` includes a message string explaining the expected outcome.
- **Given-When-Then structure:** All tests use section comments to make the test flow navigable, following the skill spec requirement for non-trivial tests.
- **Doc comments:** Every test function has a `///` doc comment explaining what it verifies.
- **Deduplication test:** Explicitly tests the deduplication requirement by setting up duplicate join table entries and verifying counts reflect unique advisories.

## Conventions Applied

- **Test location:** File lives in `tests/api/` alongside `advisory.rs`, `sbom.rs`, and `search.rs`.
- **Assertion style:** Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling tests.
- **Test naming:** Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_severity_summary_valid_sbom`).
- **Async tests:** Uses `#[tokio::test]` for async integration tests.
- **Response deserialization:** Deserializes JSON response body into a typed struct for field-level assertions.

## Helper Functions (assumed to exist or to be created)

- `setup_sbom_with_advisories(advisories: Vec<(&str, &str)>) -> Id` -- Creates an SBOM and links it to advisories with the given IDs and severity levels. This follows whatever test fixture pattern exists in the sibling test files.
- `setup_sbom_with_duplicate_advisory_links(advisories: Vec<(&str, &str, usize)>) -> Id` -- Creates an SBOM with duplicate join table entries for testing deduplication.
- `client() -> TestClient` -- Returns a configured HTTP test client pointing at the test server. This helper likely already exists in the test infrastructure used by sibling tests.

Note: The exact setup/teardown and client helper implementations would be determined by reading the existing test infrastructure in `tests/api/sbom.rs` and `tests/api/advisory.rs` during actual implementation.
