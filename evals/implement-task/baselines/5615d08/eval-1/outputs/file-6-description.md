# File 6: `tests/api/advisory_summary.rs`

**Action**: Create

## What Changes

Create integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Four test cases cover all acceptance criteria and test requirements specified in TC-9201.

## Full File Content

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests the GET /api/v2/sbom/{id}/advisory-summary endpoint, verifying
//! correct severity counts, 404 handling, zero-advisory cases, and
//! deduplication behavior.

use reqwest::StatusCode;
use serde_json::Value;

/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with known advisories at various severity levels
    let app = test_app().await;
    let sbom_id = seed_sbom_with_advisories(
        &app,
        vec![
            ("adv-1", "critical"),
            ("adv-2", "high"),
            ("adv-3", "high"),
            ("adv-4", "medium"),
            ("adv-5", "low"),
        ],
    )
    .await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response status is 200 and counts match the seeded data
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["high"], 2);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 1);
    assert_eq!(body["total"], 5);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    let app = test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .await;

    // Then the response status is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories
    let app = test_app().await;
    let sbom_id = seed_sbom_without_advisories(&app).await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then the response status is 200 and all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM where the same advisory is linked multiple times
    let app = test_app().await;
    let sbom_id = seed_sbom_with_duplicate_advisory_links(
        &app,
        vec![
            ("adv-1", "critical"),
            ("adv-1", "critical"), // duplicate link
            ("adv-2", "high"),
        ],
    )
    .await;

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Then duplicate advisories are counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1); // adv-1 counted once despite two links
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 2); // 2 unique advisories, not 3 links
}
```

## Patterns Followed

- **File location**: `tests/api/advisory_summary.rs` following the pattern of `tests/api/sbom.rs` and `tests/api/advisory.rs`
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test files
- **Test naming**: `test_advisory_summary_<scenario>` following the `test_<endpoint>_<scenario>` convention
- **Error case coverage**: 404 test for non-existent SBOM, matching sibling endpoint tests
- **No parameterized tests**: sibling tests use individual `#[tokio::test]` functions -- this is followed here rather than introducing `rstest`
- **Doc comments**: every test function has a `///` doc comment per skill requirement (constraint 5.11)
- **Given-when-then**: all tests are non-trivial (distinct setup, action, assertion phases) so they include `// Given`, `// When`, `// Then` inline comments per skill requirement (constraint 5.12)
- **Value-based assertions**: asserts on specific field values (`critical`, `high`, etc.), not just count or length
- **Module-level doc comment**: `//!` describing the test file purpose

## Test Coverage Matrix

| Test | Acceptance Criterion | Test Requirement |
|---|---|---|
| `test_advisory_summary_returns_correct_counts` | Returns `{ critical: N, high: N, medium: N, low: N, total: N }` | Valid SBOM with known advisories returns correct severity counts |
| `test_advisory_summary_nonexistent_sbom_returns_404` | Returns 404 when SBOM ID does not exist | Non-existent SBOM ID returns 404 |
| `test_advisory_summary_no_advisories_returns_zeros` | All severity levels default to 0 | SBOM with no advisories returns all zeros |
| `test_advisory_summary_deduplicates_advisory_links` | Counts only unique advisories | Duplicate advisory links are deduplicated in the count |
