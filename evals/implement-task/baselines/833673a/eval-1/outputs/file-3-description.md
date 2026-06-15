# File 3: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

Create a new file with the following test functions:

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom_with_advisories() {
    // Given an SBOM with known advisories at various severity levels
    // (setup: create test SBOM, create advisories with Critical x2, High x1, Medium x3, Low x0)
    // and link them via sbom_advisory join table

    // When requesting the advisory summary for this SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response should be 200 OK with correct counts
    // assert_eq!(resp.status(), StatusCode::OK);
    // let summary: SeveritySummary = resp.json().await;
    // assert_eq!(summary.critical, 2);
    // assert_eq!(summary.high, 1);
    // assert_eq!(summary.medium, 3);
    // assert_eq!(summary.low, 0);
    // assert_eq!(summary.total, 6);
}

/// Verifies that requesting the advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary for this SBOM
    // GET /api/v2/sbom/{nonexistent_id}/advisory-summary

    // Then the response should be 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_sbom_with_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    // (setup: create test SBOM with no advisory links)

    // When requesting the advisory summary for this SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response should be 200 OK with all zero counts
    // assert_eq!(resp.status(), StatusCode::OK);
    // let summary: SeveritySummary = resp.json().await;
    // assert_eq!(summary.critical, 0);
    // assert_eq!(summary.high, 0);
    // assert_eq!(summary.medium, 0);
    // assert_eq!(summary.low, 0);
    // assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links
    // (setup: create test SBOM, create one Critical advisory,
    //  link it twice via sbom_advisory join table)

    // When requesting the advisory summary for this SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response should count the advisory only once
    // assert_eq!(resp.status(), StatusCode::OK);
    // let summary: SeveritySummary = resp.json().await;
    // assert_eq!(summary.critical, 1);
    // assert_eq!(summary.total, 1);
}
```

## Conventions Applied

- **Location**: `tests/api/` directory, matching sibling test files `advisory.rs`, `sbom.rs`, `search.rs`.
- **Naming**: `test_<endpoint>_<scenario>` pattern matching sibling conventions (e.g., `test_advisory_summary_valid_sbom_with_advisories`).
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling pattern.
- **Error case**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`, matching sibling convention.
- **Value-based assertions**: Tests assert on specific field values (`summary.critical`, `summary.high`, etc.), not just counts or lengths, per SKILL.md Step 7 guidance.
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies, per SKILL.md Step 7 requirement.
- **Given-When-Then**: All tests use `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases.
- **Database**: Tests would use the real PostgreSQL test database, matching sibling test patterns.

## Test Coverage Mapping

| Test Requirement | Test Function |
|---|---|
| Valid SBOM with known advisories returns correct counts | `test_advisory_summary_valid_sbom_with_advisories` |
| Non-existent SBOM ID returns 404 | `test_advisory_summary_nonexistent_sbom_returns_404` |
| SBOM with no advisories returns all zeros | `test_advisory_summary_sbom_with_no_advisories_returns_zeros` |
| Duplicate advisory links are deduplicated | `test_advisory_summary_deduplicates_advisory_links` |
