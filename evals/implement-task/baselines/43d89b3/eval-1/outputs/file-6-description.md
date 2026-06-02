# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Contents

```rust
use reqwest::StatusCode;
// Additional imports for test setup, SeveritySummary, test helpers, etc.

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels:
    // - 2 Critical advisories
    // - 3 High advisories
    // - 1 Medium advisory
    // - 0 Low advisories
    // (create test SBOM and link advisories via the test database)

    // When requesting the advisory summary for the SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that requesting a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = /* non-existent ID */;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories
    // (create test SBOM without any advisory links)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with the same advisory linked multiple times
    // (create test SBOM, link one Critical advisory twice via sbom_advisory)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 1);
    assert_eq!(summary.total, 1);
}
```

## Design Decisions
- Tests hit a real PostgreSQL test database, matching the project's integration test approach (not mocked).
- Each test has a `///` doc comment explaining what it verifies (required by SKILL.md for AI-generated tests).
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments for navigability.
- Assertions are value-based (`assert_eq!` on specific count values), not length-only checks, ensuring failures reveal what changed.
- Test naming follows `test_<endpoint>_<scenario>` pattern: `test_advisory_summary_valid_sbom`, `test_advisory_summary_not_found`, etc.
- Response validation checks both status code and deserialized body fields, matching sibling test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

## Conventions Applied
- Test file location: `tests/api/` with one file per feature, matching `sbom.rs`, `advisory.rs`, `search.rs`.
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by JSON deserialization and field assertions.
- Error case: dedicated 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Test naming: `test_<feature>_<scenario>` pattern.
- Test setup: fixtures created via service layer / direct DB operations within each test.

## Note on test module registration
If `tests/api/` uses a `mod.rs` or the test harness expects explicit module declaration, a `mod advisory_summary;` line may need to be added to `tests/api/mod.rs` (or the equivalent). This would be an out-of-scope file flagged during Step 9's scope containment check and approved by the user before committing.
