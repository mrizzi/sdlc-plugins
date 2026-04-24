# File 3: tests/api/advisory_summary.rs

**Action**: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests verify all four acceptance criteria and all four test requirements from the task description.

## Conventions Applied

- **Test location**: Placed in `tests/api/` alongside sibling test files `sbom.rs`, `advisory.rs`, `search.rs`
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests
- **Error cases**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` per sibling convention
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`)
- **Test setup**: Uses real PostgreSQL test database with fixture data per repository convention
- **No parameterized tests**: Sibling tests do not use `rstest`; individual test functions used per convention
- **Doc comments**: Every test function has a `///` doc comment per SKILL.md requirement
- **Given-When-Then**: Section comments added for non-trivial tests per SKILL.md requirement

## Detailed Changes

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels:
    // - 2 Critical advisories
    // - 3 High advisories
    // - 1 Medium advisory
    // - 0 Low advisories
    let app = test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "Critical"),
        ("ADV-003", "High"),
        ("ADV-004", "High"),
        ("ADV-005", "High"),
        ("ADV-006", "Medium"),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should return 200 with correct counts
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let app = test_app().await;
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .await;

    // Then the response should return 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no advisories linked
    let app = test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should return 200 with all counts at zero
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)
    let app = test_app().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&app, vec![
        ("ADV-001", "Critical"),  // first link
        ("ADV-001", "Critical"),  // duplicate link -- same advisory
        ("ADV-002", "High"),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response should count each advisory only once
    assert_eq!(resp.status(), StatusCode::OK);

    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 1, "ADV-001 should be counted only once despite duplicate links");
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2, "total should reflect unique advisories only");
}
```

## Design Decisions

1. **Value-based assertions**: Per SKILL.md, tests assert on actual field values (e.g., `assert_eq!(body["critical"], 2)`) rather than just checking response length or status. This ensures test failures reveal *what* changed.
2. **Four test functions**: Each maps to one of the four test requirements in the task description.
3. **Assertion messages**: The deduplication test includes assertion messages to clarify intent when a failure occurs.
4. **Fixture helpers**: `seed_sbom_with_advisories`, `seed_sbom_without_advisories`, and `seed_sbom_with_duplicate_advisories` are helper functions that would be implemented to set up the test database. Their exact implementation depends on existing test utilities in the codebase.
5. **`serde_json::Value` for body**: Flexible deserialization that avoids coupling tests to the exact `SeveritySummary` struct, matching the pragmatic style seen in integration tests.

## Notes

- The exact test setup mechanism (`test_app()`, database seeding) would be determined by inspecting the existing test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) during actual implementation.
- The `tests/Cargo.toml` may need to be updated to include the new test file as a test target, depending on how the test harness is configured (auto-discovery vs explicit listing).
