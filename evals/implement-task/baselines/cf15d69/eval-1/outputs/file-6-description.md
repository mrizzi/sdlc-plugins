# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Covers all four test requirements from the task description.

## Detailed Changes

Create a new test file following the patterns found in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns
//! aggregated advisory severity counts for a given SBOM.

use axum::http::StatusCode;
// Additional imports would match sibling test files (test helpers, client setup, etc.)

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (Setup: create test SBOM, create advisories with known severities,
    //  link them via sbom_advisory join table)
    let sbom_id = setup_test_sbom_with_advisories(&[
        ("ADV-001", "critical"),
        ("ADV-002", "high"),
        ("ADV-003", "high"),
        ("ADV-004", "medium"),
        ("ADV-005", "low"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await;

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);
    assert_eq!(summary.high, 2);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 1);
    assert_eq!(summary.total, 5);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let nonexistent_id = "nonexistent-sbom-id";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{nonexistent_id}/advisory-summary"))
        .send()
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_test_sbom_without_advisories().await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
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
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = setup_test_sbom_with_advisories(&[
        ("ADV-001", "critical"),
        ("ADV-001", "critical"),  // duplicate
        ("ADV-002", "high"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await;

    // Then duplicate advisories are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // ADV-001 counted once despite duplicate link
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 2);     // Only 2 unique advisories
}
```

## Convention Conformance

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Response validation**: Asserts on specific field values (not just counts/lengths), per skill requirement to "prefer value-based assertions over length-only checks."
- **Error cases**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling test patterns.
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`).
- **Test organization**: One test file for the new endpoint, placed in `tests/api/` alongside existing endpoint test files.
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies, per skill requirement.
- **Given-When-Then**: Each test has `// Given`, `// When`, `// Then` section comments for navigability, since all tests have distinct setup/action/assertion phases.
- **Parameterized tests**: Not used -- sibling test analysis did not reveal `#[rstest]` usage, and each test case has a distinct setup (different SBOM configurations), making individual tests more appropriate per the Meszaros heuristic.

## Notes

The exact test setup patterns (how to create test SBOMs, link advisories, set up the test client) would be determined by reading `tests/api/sbom.rs` and `tests/api/advisory.rs` during Step 4. The helper functions (`setup_test_sbom_with_advisories`, etc.) represent the intended logic; actual implementation would match the test infrastructure found in the codebase.

The `tests/Cargo.toml` may need to be updated to include the new test file if it uses an explicit test file list rather than auto-discovery. This would be verified during Step 4 and flagged in Step 9 scope containment if an out-of-scope file modification is needed.
