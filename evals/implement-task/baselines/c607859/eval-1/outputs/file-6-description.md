# File 6: tests/api/advisory_summary.rs

**Action**: CREATE

## Context

New integration test file for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests
hit a real PostgreSQL test database, consistent with the existing test infrastructure in
`tests/api/`.

## Sibling Pattern Reference

Examining `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` for success assertions
- Tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 assertions
- Response body is deserialized with `resp.json::<T>().await` (or equivalent)
- Test functions are named `test_<endpoint>_<scenario>`
- Tests create fixture data in the test database before making HTTP requests
- Each test is an `async` function with `#[tokio::test]` attribute
- Test setup typically involves ingesting test SBOMs and advisories via the service layer

## File Contents

```rust
use reqwest::StatusCode;

// Test helper imports (test client, fixture creation utilities, etc.)
// Following sibling test file import patterns

/// Verifies that the advisory summary endpoint returns correct severity counts
/// for an SBOM with known advisories at different severity levels.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories: 2 critical, 1 high, 3 medium, 0 low
    let client = setup_test_client().await;
    let sbom_id = create_test_sbom(&client).await;
    create_test_advisory(&client, sbom_id, "critical").await;
    create_test_advisory(&client, sbom_id, "critical").await;
    create_test_advisory(&client, sbom_id, "high").await;
    create_test_advisory(&client, sbom_id, "medium").await;
    create_test_advisory(&client, sbom_id, "medium").await;
    create_test_advisory(&client, sbom_id, "medium").await;

    // When requesting the advisory severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response should contain correct counts per severity
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 status, consistent with other SBOM endpoint behavior.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let client = setup_test_client().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await
        .unwrap();

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns a severity summary
/// with all counts at zero.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    let client = setup_test_client().await;
    let sbom_id = create_test_sbom(&client).await;

    // When requesting the advisory severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated
/// in the severity count, so each advisory is counted only once.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with the same advisory linked twice
    let client = setup_test_client().await;
    let sbom_id = create_test_sbom(&client).await;
    let advisory_id = create_test_advisory(&client, sbom_id, "high").await;
    // Create a duplicate link for the same advisory
    create_duplicate_advisory_link(&client, sbom_id, advisory_id).await;

    // When requesting the advisory severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 1);
}
```

## Design Decisions

- **Four test functions**: one for each test requirement in the task spec.
- **Value-based assertions**: asserts on specific count values (e.g., `assert_eq!(summary.critical, 2)`), not just length checks. This follows the SKILL.md guidance to "prefer value-based assertions over length-only checks."
- **Given-When-Then comments**: all tests have section comments for navigability, following the SKILL.md requirement for non-trivial tests.
- **Doc comments on every test function**: follows the SKILL.md mandatory requirement that "every test function must have a documentation comment."
- **Test naming**: follows `test_<endpoint>_<scenario>` pattern from sibling tests.
- **Assertion style**: uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching the sibling test pattern.
- **404 test included**: consistent with sibling test files that all include 404 tests.
- **No parameterized tests**: the four test cases exercise fundamentally different scenarios (valid data, 404, empty, deduplication) with different setups and assertions, so individual test functions are more appropriate than parameterized tests per the Meszaros heuristic.

## Test Coverage Matrix

| Test Requirement | Test Function | Verified |
|---|---|---|
| Valid SBOM with known advisories returns correct counts | `test_advisory_summary_valid_sbom` | Yes -- asserts all 5 fields |
| Non-existent SBOM ID returns 404 | `test_advisory_summary_nonexistent_sbom` | Yes -- asserts StatusCode::NOT_FOUND |
| SBOM with no advisories returns all zeros | `test_advisory_summary_empty_sbom` | Yes -- asserts all 5 fields are 0 |
| Duplicate advisory links are deduplicated | `test_advisory_summary_deduplication` | Yes -- asserts count is 1 not 2 |

## Note on tests/Cargo.toml

The `tests/Cargo.toml` may need to be updated to include the new test file in its test
targets, depending on how the test harness discovers test files. If tests are auto-discovered
via directory scanning, no change is needed. If they are explicitly listed, a new `[[test]]`
entry would be added. This would be verified during the actual implementation by inspecting
the existing `tests/Cargo.toml` configuration.
