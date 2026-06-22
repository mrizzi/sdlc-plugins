# File 5: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

Create a new integration test file following the patterns in sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs`.

```rust
use axum::http::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
///
/// Seeds an SBOM with advisories of known severities and asserts that the response
/// contains the exact expected counts for each severity level and total.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories:
    //   2 Critical, 1 High, 3 Medium, 0 Low
    let client = setup_test_client().await;
    let sbom_id = seed_sbom_with_advisories(&client, vec![
        ("adv-1", "Critical"),
        ("adv-2", "Critical"),
        ("adv-3", "High"),
        ("adv-4", "Medium"),
        ("adv-5", "Medium"),
        ("adv-6", "Medium"),
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let client = setup_test_client().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no advisories linked
    let client = setup_test_client().await;
    let sbom_id = seed_sbom_with_advisories(&client, vec![]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response is 200 OK with all zeros
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
///
/// When the same advisory is linked to an SBOM multiple times (via the
/// sbom_advisory join table), it should be counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links
    let client = setup_test_client().await;
    let sbom_id = seed_sbom_with_duplicate_advisories(&client, vec![
        ("adv-1", "High"),
        ("adv-1", "High"),  // duplicate
        ("adv-2", "Medium"),
        ("adv-2", "Medium"),  // duplicate
        ("adv-2", "Medium"),  // another duplicate
    ]).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then duplicates are deduplicated -- only unique advisories counted
    assert_eq!(resp.status(), StatusCode::OK);
    let body: serde_json::Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 1);    // adv-1 counted once
    assert_eq!(body["medium"], 1);  // adv-2 counted once
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2);   // 2 unique advisories
}
```

## Conventions followed

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization -- matching sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs`
- **Response validation**: Validates individual field values (not just length or existence) -- satisfies SKILL.md requirement "prefer value-based assertions over length-only checks"
- **Error cases**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` -- matching sibling test pattern
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`)
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies, per SKILL.md requirements
- **Given-When-Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments
- **Test setup**: Uses test client and database seeding helpers, consistent with sibling integration tests
- **Parameterized tests**: Not used -- would first check if sibling tests use `#[rstest]`. If not found in siblings, individual test functions are used (which is the case here -- four distinct scenarios with different setup requirements)

## Notes

- The exact test setup functions (`setup_test_client`, `seed_sbom_with_advisories`) would be adapted from the patterns found in sibling test files via Serena inspection
- The `seed_sbom_with_duplicate_advisories` helper creates intentional duplicate join table entries to test deduplication
- If `tests/Cargo.toml` needs updating to include the new test file as a test target, that would be flagged as an out-of-scope change in Step 9 for user approval
