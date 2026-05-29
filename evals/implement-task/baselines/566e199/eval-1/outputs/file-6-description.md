# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose
Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that requesting the advisory summary for an SBOM with known advisories
/// returns correct severity counts matching the seeded test data.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with seeded advisories at known severity levels
    // (e.g., 2 Critical, 3 High, 1 Medium, 0 Low)
    let server = create_test_server().await;
    let sbom_id = seed_sbom_with_advisories(&server, vec![
        ("adv-1", "Critical"),
        ("adv-2", "Critical"),
        ("adv-3", "High"),
        ("adv-4", "High"),
        ("adv-5", "High"),
        ("adv-6", "Medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = server
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response is 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting the advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let server = create_test_server().await;
    let fake_id = Id::from("non-existent-sbom-id");

    // When requesting the advisory summary
    let resp = server
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary where
/// all severity counts are zero and the total is zero.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    let server = create_test_server().await;
    let sbom_id = seed_sbom_without_advisories(&server).await;

    // When requesting the advisory summary
    let resp = server
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response is 200 OK with all zeros
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory-to-SBOM links are deduplicated in the
/// severity count, so the same advisory linked twice does not inflate the total.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM where the same advisory is linked twice
    let server = create_test_server().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&server, vec![
        ("adv-1", "High"),
        ("adv-1", "High"),  // duplicate link
        ("adv-2", "Low"),
    ]).await;

    // When requesting the advisory summary
    let resp = server
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the counts reflect unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1);  // adv-1 counted once
    assert_eq!(summary.low, 1);   // adv-2 counted once
    assert_eq!(summary.total, 2); // 2 unique advisories
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.medium, 0);
}
```

### Conventions followed

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test files `advisory.rs` and `sbom.rs`.
- **Response validation**: asserts on specific field values (not just collection lengths).
- **Error cases**: includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Test naming**: follows `test_<endpoint_action>_<scenario>` pattern.
- **Test setup**: uses test server setup function with real PostgreSQL test database, consistent with `tests/api/` sibling tests.
- **Documentation**: every test function has a `///` doc comment.
- **Given-When-Then**: all tests include `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases.
- **Parameterized tests**: not used here because each test exercises distinct setup scenarios (different seeding patterns) with different assertion logic. If sibling tests use `#[rstest]`, the valid-counts test could potentially be parameterized, but the varying seed data makes individual tests clearer.
