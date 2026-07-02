# File 3: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Pre-implementation Inspection

Before creating this file, inspect sibling test files to confirm test patterns:
- Use `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` to see the test structure, setup patterns, assertion style, and naming conventions
- Use `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` to confirm the pattern holds across test files
- Read the test setup mechanism to understand how test databases are seeded and how the HTTP test client is constructed
- Check if sibling tests use `#[rstest]` / `#[case]` for parameterized tests -- if not, do not introduce them

## Planned Content

```rust
use reqwest::StatusCode;
// Import test utilities, server setup, fixture helpers based on what siblings use

/// Verifies that an SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM linked to advisories with known severities
    // (seed test DB with an SBOM and linked advisories:
    //  2 critical, 3 high, 1 medium, 0 low = 6 total)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("adv-1", "critical"),
        ("adv-2", "critical"),
        ("adv-3", "high"),
        ("adv-4", "high"),
        ("adv-5", "high"),
        ("adv-6", "medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response contains correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await
        .unwrap();

    // Then a 404 status is returned
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

    // When requesting the advisory summary
    let resp = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&app, vec![
        ("adv-1", "critical"),
        ("adv-1", "critical"),  // duplicate link
        ("adv-2", "high"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then counts reflect unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 1);  // adv-1 counted once despite two links
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);  // 2 unique advisories, not 3 links
}
```

## Design Decisions

- **Value-based assertions**: Per SKILL.md, tests assert on specific field values (`assert_eq!(summary.critical, 2)`) rather than just checking collection lengths
- **Doc comments on every test**: Per SKILL.md, every test function gets a `///` doc comment explaining what it verifies, even if sibling tests do not have them
- **Given-When-Then structure**: Per SKILL.md, non-trivial tests include `// Given`, `// When`, `// Then` section comments for navigability
- **Four test functions**: One for each test requirement in the task description
- **Assertion style**: Follows sibling pattern of `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization and field-level assertions
- **404 test**: Follows sibling pattern of testing with a non-existent ID and asserting `StatusCode::NOT_FOUND`

## Notes

- The exact test setup functions (`setup_test_app`, `seed_sbom_with_advisories`, etc.) will be based on patterns found in sibling test files during inspection
- The `tests/api/` directory may need its `mod.rs` updated to include the new test module, or tests may be auto-discovered -- would verify by checking how `sbom.rs` and `advisory.rs` are registered
- If sibling tests use `#[rstest]`, would consider parameterizing the severity count test cases; if not, individual test functions are used (as shown above)

## Conventions Applied

- Test naming: `test_<endpoint>_<scenario>` pattern
- Assertion style: `assert_eq!(resp.status(), StatusCode::...)` pattern
- Response validation: Deserialize body and assert specific field values
- Error case coverage: Includes 404 test for non-existent entity
