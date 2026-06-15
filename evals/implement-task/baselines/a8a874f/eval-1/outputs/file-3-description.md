# File 3: tests/api/advisory_summary.rs

## Action: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests verify correct severity counts, 404 handling, empty SBOM behavior, and deduplication.

## Detailed Changes

Create a new file with four test functions:

```rust
use reqwest::StatusCode;
use serde_json::Value;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with known advisory severities seeded in the test database
    // (e.g., 2 critical, 1 high, 3 medium, 0 low advisories)
    let sbom_id = setup_sbom_with_advisories(vec![
        ("ADV-001", "critical"),
        ("ADV-002", "critical"),
        ("ADV-003", "high"),
        ("ADV-004", "medium"),
        ("ADV-005", "medium"),
        ("ADV-006", "medium"),
    ])
    .await;

    // When requesting the advisory summary for that SBOM
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .unwrap();

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)
    let sbom_id = setup_sbom_with_advisories(vec![
        ("ADV-001", "critical"),
        ("ADV-001", "critical"),  // duplicate
        ("ADV-002", "high"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then duplicates are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await.unwrap();
    assert_eq!(body["critical"], 1);  // ADV-001 counted once despite two links
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2);     // 2 unique advisories, not 3 links
}
```

## Notes on Test Setup

The actual test setup functions (`setup_sbom_with_advisories`, `client`) would follow the patterns established in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`). Before writing the final implementation, I would:

1. Read `tests/api/advisory.rs` and `tests/api/sbom.rs` via Serena to understand:
   - How the test database is initialized and seeded
   - How the HTTP client is constructed
   - How test fixtures (SBOMs, advisories) are created
   - Whether there is a shared test harness module
2. Adapt the setup to use the same fixture creation patterns
3. Register this test module in `tests/Cargo.toml` if needed (see file-7-description.md)

## Conventions Applied

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test patterns
- **Error cases**: Includes a 404 test matching the pattern in sibling tests
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_not_found`)
- **Value-based assertions**: Asserts on specific field values (`body["critical"]`, etc.), not just collection lengths
- **Documentation**: Every test function has a `///` doc comment describing what it verifies
- **Given-When-Then**: Each test has `// Given`, `// When`, `// Then` section comments for navigability
- **Test file naming**: Named `advisory_summary.rs` to distinguish from the existing `advisory.rs` tests
- **Async tests**: Uses `#[tokio::test]` matching the async Axum test pattern
