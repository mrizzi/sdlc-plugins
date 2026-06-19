# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the 4 test cases defined in the task's Test Requirements.

## Detailed Changes

### Inspect before writing

Before creating this file, inspect sibling test files to confirm test patterns:
- Read `tests/api/advisory.rs` to see:
  - Test setup and teardown patterns (database seeding, fixtures)
  - HTTP client usage (how requests are made to the test server)
  - Status code assertion pattern (`assert_eq!(resp.status(), StatusCode::OK)`)
  - Response body deserialization pattern
  - 404 error test pattern
  - Test naming convention
- Read `tests/api/sbom.rs` to see cross-module test patterns
- Check `tests/Cargo.toml` for test dependencies

### New file content

```rust
//! Integration tests for the advisory severity summary endpoint.

use reqwest::StatusCode;

// Import test utilities, fixtures, and the SeveritySummary type
// (exact imports to be determined from sibling test file inspection)

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_severity_counts() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test database with SBOM and linked advisories: 2 Critical, 1 High, 3 Medium, 0 Low)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the response contains correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.expect("invalid JSON");
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .send()
        .await
        .expect("request failed");

    // Then a 404 status is returned
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    // (seed test database with SBOM but no advisory links)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.expect("invalid JSON");
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links
    // (seed test database with SBOM linked to the same advisory multiple times)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.expect("invalid JSON");
    assert_eq!(summary.total, 1); // Only 1 unique advisory despite duplicate links
    assert_eq!(summary.critical, 1); // Assuming the test advisory is Critical severity
}
```

### Notes

- The exact test setup (database seeding, fixture creation, HTTP client initialization) will be adapted from the patterns observed in `tests/api/advisory.rs` and `tests/api/sbom.rs`
- Every test function has a `///` doc comment per skill requirement
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments per skill requirement
- Tests assert on specific values (not just counts) per skill guidance on value-based assertions
- The test for deduplication specifically verifies that `total` reflects unique advisory count
- If sibling tests use `#[rstest]` or parameterized patterns, consider using them for the multiple test scenarios — but only if siblings use them
- The `tests/Cargo.toml` may need updating to include the new test file — check if test files are auto-discovered or explicitly listed
