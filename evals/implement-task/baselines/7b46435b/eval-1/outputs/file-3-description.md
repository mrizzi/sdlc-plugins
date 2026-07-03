# File 3: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests
hit a real PostgreSQL test database, consistent with the project's test infrastructure
in `tests/api/`.

## Detailed Changes

Create a new test file with 4 test functions covering all Test Requirements:

```rust
use axum::http::StatusCode;

// Test setup imports following sibling test patterns (advisory.rs, sbom.rs)
// Use the same test harness, database seeding, and HTTP client setup

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels:
    //   2 Critical, 3 High, 1 Medium, 0 Low
    // (seed the test database with the SBOM and linked advisories via sbom_advisory join table)

    // When requesting the advisory summary for the SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the response body contains the correct severity counts
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await;

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM that exists but has no linked advisories

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", empty_sbom_id))
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
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM linked to the same advisory multiple times in the sbom_advisory join table
    //   (e.g., advisory A1 at Critical severity linked twice)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_with_dupes_id))
        .send()
        .await;

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the duplicate advisory is counted only once
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1); // Not 2, despite two links to the same advisory
    assert_eq!(summary.total, 1);
}
```

## Conventions Applied

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization and field-level assertions, matching `tests/api/advisory.rs` and `tests/api/sbom.rs` patterns.
- **Response validation**: Validates individual field values (not just counts or lengths), following the SKILL.md requirement to prefer value-based assertions over length-only checks.
- **Error cases**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`, matching sibling test patterns.
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`).
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies.
- **Given/When/Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- **File placement**: In `tests/api/` directory alongside `advisory.rs` and `sbom.rs`.
- **Async tests**: Uses `#[tokio::test]` for async test functions, consistent with the async endpoint handler pattern.

## Notes

- Tests use a real PostgreSQL test database, following the project convention. Setup code would seed the database with known SBOMs and advisories via the sbom_advisory join table.
- The deduplication test specifically creates duplicate links in the join table to verify the DISTINCT/HashSet logic in the service method.
- The `tests/Cargo.toml` may need to be updated to include the new test file in the test suite, depending on how the test harness discovers test modules. This would be verified during implementation.
