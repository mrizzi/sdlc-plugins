# File 3: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.
Tests cover the four scenarios specified in the task's Test Requirements section.

## Detailed Changes

```rust
use reqwest::StatusCode;
// Additional imports for test setup, SeveritySummary struct, test helpers, etc.

/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with 2 Critical, 1 High, 1 Medium, and 0 Low advisories
    // (created via test fixtures in the test database)
    let sbom_id = create_test_sbom_with_advisories(vec![
        ("ADV-001", Severity::Critical),
        ("ADV-002", Severity::Critical),
        ("ADV-003", Severity::High),
        ("ADV-004", Severity::Medium),
    ]).await;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 4);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await
        .unwrap();

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let sbom_id = create_test_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with all counts at zero
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
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = create_test_sbom_with_advisory_links(vec![
        ("ADV-001", Severity::Critical),
        ("ADV-001", Severity::Critical),  // duplicate link
        ("ADV-002", Severity::High),
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then duplicates are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 1);  // ADV-001 counted once despite two links
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);  // 2 unique advisories, not 3 links
}
```

## Test conventions followed

- File placed in `tests/api/` directory (matches `sbom.rs`, `advisory.rs` siblings)
- `#[tokio::test]` attribute for async tests
- Test names follow `test_<endpoint>_<scenario>` pattern
- Status assertions use `assert_eq!(resp.status(), StatusCode::OK)` (matches sibling pattern)
- Response bodies deserialized and individual fields asserted (value-based, not length-only)
- Both success and error scenarios covered
- Doc comment on every test function explaining what it verifies
- Given-when-then section comments inside each test body (tests have distinct setup/action/assert phases)
- Tests are self-contained with no ordering dependencies
