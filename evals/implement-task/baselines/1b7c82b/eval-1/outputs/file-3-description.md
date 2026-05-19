# File 3: tests/api/advisory_summary.rs

## Action: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover all four test requirements from the task description: valid SBOM with known advisories, non-existent SBOM, SBOM with no advisories, and deduplication of advisory links.

## Detailed Changes

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known advisories returns the correct
/// severity counts per level and the correct total.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels seeded in the test database
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_advisories(&app, vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "High"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
        ("ADV-005", "Low"),
    ]).await;

    // When requesting the advisory summary for the SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 1);
    assert_eq!(body.high, 2);
    assert_eq!(body.medium, 1);
    assert_eq!(body.low, 1);
    assert_eq!(body.total, 5);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a test app with no SBOM matching the given ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for the non-existent SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// where all severity counts and the total are zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response is 200 OK with all counts at zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that when the same advisory is linked to an SBOM multiple times
/// (via duplicate entries in the sbom_advisory join table), it is counted
/// only once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM with a duplicate advisory link (same advisory linked twice)
    let app = setup_test_app().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&app, vec![
        ("ADV-001", "Critical"),
        ("ADV-001", "Critical"),  // duplicate link
        ("ADV-002", "High"),
    ]).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the duplicate is not double-counted
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 1);  // ADV-001 counted once despite duplicate link
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 2);  // only 2 unique advisories
}
```

### Design Decisions

- **No parameterized tests**: Sibling test analysis shows the project does not use `#[rstest]` or parameterized test patterns. Each test case is a separate function, following the existing convention.
- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the sibling convention in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Value-based assertions**: Each test asserts on specific field values (not just `total` or length), so test failures reveal exactly which severity count is wrong.
- **404 test**: Follows the sibling pattern of testing non-existent IDs return 404.
- **Doc comments on every test**: Every test function has a `///` doc comment explaining what it verifies, per implement-task requirements.
- **Given-when-then comments**: All four tests are non-trivial (they have setup, action, and assertion phases), so they include `// Given`, `// When`, `// Then` section comments.
- **Test naming**: Follows `test_<feature>_<scenario>` pattern consistent with sibling test files.
- **Integration test setup**: Uses the same test app setup pattern as sibling tests, hitting a real PostgreSQL test database.

### Conventions Applied

- File placed in `tests/api/` directory alongside sibling test files
- Uses `#[tokio::test]` for async test execution
- Test helper functions (`setup_test_app`, `seed_sbom_with_advisories`, etc.) follow established patterns
- Status code checked before body deserialization
