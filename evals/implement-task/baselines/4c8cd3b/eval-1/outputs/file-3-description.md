# File 3: tests/api/advisory_summary.rs

**Action:** CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all test requirements from the task.

## Detailed Changes

Create a new file with integration tests. The tests hit a real PostgreSQL test database following the established test convention.

```rust
use reqwest::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisory severity distribution:
    //   2 Critical, 1 High, 3 Medium, 0 Low
    let sbom_id = setup_sbom_with_advisories(vec![
        ("ADV-001", "Critical"),
        ("ADV-002", "Critical"),
        ("ADV-003", "High"),
        ("ADV-004", "Medium"),
        ("ADV-005", "Medium"),
        ("ADV-006", "Medium"),
    ])
    .await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(summary["critical"], 2);
    assert_eq!(summary["high"], 1);
    assert_eq!(summary["medium"], 3);
    assert_eq!(summary["low"], 0);
    assert_eq!(summary["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = "nonexistent-sbom-id";

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .unwrap();

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let sbom_id = setup_sbom_with_advisories(vec![]).await;

    // When requesting the advisory summary
    let resp = client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response is 200 OK with all zeros
    assert_eq!(resp.status(), StatusCode::OK);

    let summary: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(summary["critical"], 0);
    assert_eq!(summary["high"], 0);
    assert_eq!(summary["medium"], 0);
    assert_eq!(summary["low"], 0);
    assert_eq!(summary["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)
    let sbom_id = setup_sbom_with_advisories_duplicated(vec![
        ("ADV-001", "Critical"),
        ("ADV-001", "Critical"),  // duplicate link
        ("ADV-002", "High"),
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

    let summary: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(summary["critical"], 1);  // ADV-001 counted once despite duplicate link
    assert_eq!(summary["high"], 1);
    assert_eq!(summary["medium"], 0);
    assert_eq!(summary["low"], 0);
    assert_eq!(summary["total"], 2);  // 2 unique advisories, not 3 links
}
```

## Conventions Applied

- **Test location:** Integration tests in `tests/api/` with a domain-specific filename, consistent with `sbom.rs`, `advisory.rs`, `search.rs`.
- **Assertion style:** Uses `assert_eq!(resp.status(), StatusCode::OK)` pattern followed by body deserialization, matching sibling test files.
- **Test naming:** Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`).
- **Error case coverage:** Includes a 404 test for non-existent SBOM ID, consistent with sibling test files.
- **Documentation:** Every test function has a `///` doc comment explaining what it verifies (AI-generated test standard from SKILL.md).
- **Given-When-Then:** Non-trivial tests include `// Given`, `// When`, `// Then` section comments for navigability.
- **Value-based assertions:** Tests assert on specific field values (e.g., `assert_eq!(summary["critical"], 2)`) rather than just checking response shape or count, ensuring failures reveal what changed.
