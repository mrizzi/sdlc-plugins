# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## File content

```rust
use reqwest::StatusCode;
use serde::Deserialize;

/// Response struct for deserializing the advisory summary endpoint response.
#[derive(Debug, Deserialize)]
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
    // Given an SBOM with advisories at known severity levels:
    //   2 critical, 1 high, 3 medium, 0 low
    let client = setup_test_client().await;
    let sbom_id = create_test_sbom(&client).await;
    create_test_advisory(&client, &sbom_id, "critical").await;
    create_test_advisory(&client, &sbom_id, "critical").await;
    create_test_advisory(&client, &sbom_id, "high").await;
    create_test_advisory(&client, &sbom_id, "medium").await;
    create_test_advisory(&client, &sbom_id, "medium").await;
    create_test_advisory(&client, &sbom_id, "medium").await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the response should contain correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummaryResponse = resp.json().await.expect("invalid JSON");
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 3);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let client = setup_test_client().await;
    let nonexistent_id = "nonexistent-sbom-id-12345";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await
        .expect("request failed");

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no advisories linked
    let client = setup_test_client().await;
    let sbom_id = create_test_sbom(&client).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummaryResponse = resp.json().await.expect("invalid JSON");
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with the same advisory linked multiple times
    let client = setup_test_client().await;
    let sbom_id = create_test_sbom(&client).await;
    let advisory_id = create_test_advisory(&client, &sbom_id, "high").await;
    // Link the same advisory again (duplicate)
    link_advisory_to_sbom(&client, &sbom_id, &advisory_id).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request failed");

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummaryResponse = resp.json().await.expect("invalid JSON");
    assert_eq!(body.high, 1);
    assert_eq!(body.total, 1);
}
```

Note: `setup_test_client`, `create_test_sbom`, `create_test_advisory`, and `link_advisory_to_sbom` are helper functions that would be implemented based on the test infrastructure patterns found in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`). The actual helper implementations depend on the test database setup used by the project.

## Design decisions

- **Individual test functions**: sibling tests do not use parameterized tests (`#[rstest]`), so each test case is a separate function
- **Value-based assertions**: each test asserts on specific field values (`assert_eq!(body.critical, 2)`) rather than just length checks, per skill requirements
- **Given-when-then comments**: all non-trivial tests include `// Given`, `// When`, `// Then` section comments for readability
- **Doc comments**: every test function has a `///` doc comment explaining what it verifies
- **Deduplication test**: creates the same advisory linked twice and verifies count is 1, directly testing the acceptance criterion

## Conventions applied

- Test file in `tests/api/` directory matching sibling location
- File named `advisory_summary.rs` following resource-based naming (`sbom.rs`, `advisory.rs`)
- Test names follow `test_<endpoint>_<scenario>` pattern
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` and `StatusCode::NOT_FOUND`
- Response body deserialized into typed struct for field-level validation
- Each test manages its own test data setup (no shared mutable state)
