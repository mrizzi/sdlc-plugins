# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task description.

## Detailed Changes

Create a new test file following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
use reqwest::StatusCode;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels seeded in the test database
    // (e.g., 2 Critical, 3 High, 1 Medium, 0 Low)
    let sbom_id = /* create or reference a test SBOM with known advisory links */;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then the response status is OK and counts match the seeded data
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: serde_json::Value = resp.json().await.unwrap();
    assert_eq!(summary["critical"], 2);
    assert_eq!(summary["high"], 3);
    assert_eq!(summary["medium"], 1);
    assert_eq!(summary["low"], 0);
    assert_eq!(summary["total"], 6);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await
        .unwrap();

    // Then the response status is NOT_FOUND
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    let empty_sbom_id = /* create or reference an SBOM with no advisory links */;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", empty_sbom_id))
        .send()
        .await
        .unwrap();

    // Then all severity counts are zero
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
    // Given an SBOM linked to the same advisory multiple times (via duplicate join table entries)
    let sbom_id = /* create SBOM with duplicate advisory links */;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .unwrap();

    // Then each advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: serde_json::Value = resp.json().await.unwrap();
    // If same Critical advisory linked twice, critical should be 1, not 2
    assert_eq!(summary["critical"], 1);
    assert_eq!(summary["total"], 1);
}
```

## Conventions Applied

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization -- matches `tests/api/advisory.rs` and `tests/api/sbom.rs`
- **Response validation**: checks both status code and response body field values (not just length)
- **Error cases**: 404 test with `StatusCode::NOT_FOUND` matching sibling test pattern
- **Test naming**: `test_advisory_summary_<scenario>` following `test_<endpoint>_<scenario>` convention
- **Documentation**: every test function has a `///` doc comment explaining what it verifies
- **Given-When-Then**: section comments in test bodies for non-trivial tests (all four tests qualify)
- **Value-based assertions**: asserts on specific count values, not just that response is OK
- **Test organization**: all tests for this endpoint in one file, grouped by scenario

## Inspection Required

Before creating, would:
1. Read `tests/api/advisory.rs` and `tests/api/sbom.rs` to see exact test setup patterns (how client is created, how test DB is seeded, exact import paths)
2. Check `tests/Cargo.toml` for test dependencies
3. Verify whether the test file needs to be registered in a `mod.rs` or if Cargo discovers it automatically
4. Understand the test database fixture seeding pattern to write realistic setup code

## Sibling Parity

Compared with `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- Same test framework (`tokio::test`)
- Same assertion patterns
- Same HTTP client usage
- Same test naming convention
- Added doc comments (new standard per SKILL.md, applied even if siblings lack them)
