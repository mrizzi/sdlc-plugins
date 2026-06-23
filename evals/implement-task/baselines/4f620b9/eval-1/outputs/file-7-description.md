# File 7: tests/api/advisory_summary.rs

**Action**: CREATE

**Purpose**: Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

This is a new test file. It follows the patterns established by sibling test files `tests/api/sbom.rs` and `tests/api/advisory.rs`.

### Contents

```rust
// Integration tests for the advisory severity summary endpoint.
//
// Tests follow the same patterns as sibling test files (sbom.rs, advisory.rs):
// - Real PostgreSQL test database
// - assert_eq!(resp.status(), StatusCode::...) for status verification
// - Body deserialization and value-based assertions
// - Individual test functions (no parameterized tests, matching sibling convention)

use axum::http::StatusCode;
// ... other imports matching sibling test file patterns ...
use crate::advisory::model::severity_summary::SeveritySummary;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom_with_advisories() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test data: create SBOM, create advisories with known severities,
    //  link them via sbom_advisory join table)
    // - 2 Critical advisories
    // - 3 High advisories  
    // - 1 Medium advisory
    // - 0 Low advisories

    // When requesting the advisory summary for this SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response should be 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let nonexistent_id = /* a UUID or ID that does not exist in the test database */;

    // When requesting the advisory summary for this SBOM
    // GET /api/v2/sbom/{nonexistent_id}/advisory-summary

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_sbom_no_advisories() {
    // Given an SBOM with no linked advisories
    // (create SBOM but do not link any advisories)

    // When requesting the advisory summary for this SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response should be 200 OK with all zeros
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
///
/// When the same advisory is linked to an SBOM multiple times (e.g., via
/// different vulnerability paths), it should only be counted once.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with a single advisory linked multiple times
    // (create SBOM, create one Critical advisory, insert multiple
    //  sbom_advisory rows linking the same advisory to the SBOM)

    // When requesting the advisory summary for this SBOM
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the advisory should only be counted once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // Not 3 or however many duplicate links
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 1);
}
```

### Additional considerations

- The `tests/api/` directory likely has a `mod.rs` or the test files are registered via `tests/Cargo.toml` configuration. Would need to verify the test registration mechanism and add `mod advisory_summary;` if required.
- Test database setup and teardown patterns would be copied from sibling test files.
- The exact test HTTP client pattern (how requests are made to the test server) would be confirmed by reading `tests/api/sbom.rs` or `tests/api/advisory.rs` during Step 4.

### Conventions Applied

- **File naming**: `advisory_summary.rs` follows sibling pattern (`sbom.rs`, `advisory.rs`, `search.rs`)
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization and value-based assertions
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom_with_advisories`)
- **Error case coverage**: includes 404 test for non-existent SBOM
- **Value-based assertions**: all tests assert on specific field values, not just collection lengths
- **Documentation**: every test function has a `///` doc comment explaining what it verifies
- **Given-when-then structure**: all tests use `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases
- **No parameterized tests**: sibling tests do not use `#[rstest]`, so individual test functions are used
