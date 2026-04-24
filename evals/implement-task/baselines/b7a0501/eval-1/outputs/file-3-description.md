# File 3: Create `tests/api/advisory_summary.rs`

## Action: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering
all four test requirements from the task description.

## Sibling Reference

- `tests/api/advisory.rs` -- Advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/search.rs` -- Search endpoint integration tests

These siblings show the pattern: tests hit a real PostgreSQL test database, use
`assert_eq!(resp.status(), StatusCode::OK)` for status checks, deserialize response
bodies for field-level assertions, and follow `test_<endpoint>_<scenario>` naming.

## Detailed Changes

```rust
use actix_http::StatusCode;
use serde::Deserialize;

// Test-local struct to deserialize the response
#[derive(Deserialize)]
struct SeveritySummaryResponse {
    critical: u32,
    high: u32,
    medium: u32,
    low: u32,
    total: u32,
}

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (setup: ingest test SBOM and link advisories with known severities)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "High"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
    ]).await;

    // When requesting the advisory summary for the SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should contain correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummaryResponse = resp.json().await;
    assert_eq!(body.critical, 1);
    assert_eq!(body.high, 2);
    assert_eq!(body.medium, 1);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 4);
}

/// Verifies that a non-existent SBOM ID returns a 404 response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let fake_id = "nonexistent-sbom-id";

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .await;

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummaryResponse = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&app, vec![
        ("ADV-001", "Critical"),
        ("ADV-001", "Critical"),  // duplicate
        ("ADV-002", "High"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummaryResponse = resp.json().await;
    assert_eq!(body.critical, 1);  // ADV-001 counted once, not twice
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 2);  // 2 unique advisories, not 3
}
```

## Conventions Applied

- **Test naming**: `test_advisory_summary_<scenario>` -- follows `test_<endpoint>_<scenario>` pattern
  from sibling tests.
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
  and field-level assertions -- matches sibling test pattern.
- **Value-based assertions**: Asserts on specific field values (e.g., `critical == 1`), not just
  counts or lengths, per SKILL.md requirements.
- **Error cases**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies
  (AI-generated standard per SKILL.md).
- **Given-When-Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- **Real database**: Tests use the project's test database infrastructure, not mocks.

## Notes

- The exact test setup helper functions (`setup_test_app`, `seed_sbom_with_advisories`, etc.)
  would be determined by inspecting sibling test files (`sbom.rs`, `advisory.rs`) via Serena.
  In a real implementation, these would match the project's existing test utilities.
- The test module may also need to be registered in `tests/api/mod.rs` or `tests/Cargo.toml`
  depending on the test harness configuration.
