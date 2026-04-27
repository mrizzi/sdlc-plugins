# File 6 -- Create: `tests/api/advisory_summary.rs`

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests
cover the four scenarios required by the task's Test Requirements section.

## Pre-Implementation Inspection

Before creating, inspect sibling test files to match conventions:
- `tests/api/advisory.rs` -- primary sibling; examine test naming, assertion patterns,
  setup/teardown, and HTTP client usage.
- `tests/api/sbom.rs` -- cross-module sibling for additional patterns.
- `tests/api/search.rs` -- to confirm naming and organization conventions are consistent.

Also check `tests/Cargo.toml` to understand test dependencies and whether the new test
file needs to be registered (Rust integration tests in `tests/` are auto-discovered, but
a `mod.rs` or test harness might require explicit registration).

## Full File Content

```rust
//! Integration tests for the advisory severity summary endpoint.

use axum::http::StatusCode;
use serde_json::Value;

// Test setup utilities (exact import path to be confirmed from sibling test files)
use crate::common::setup_test_db;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    let db = setup_test_db().await;
    let sbom_id = create_test_sbom(&db).await;
    create_test_advisory(&db, sbom_id, "critical").await;
    create_test_advisory(&db, sbom_id, "critical").await;
    create_test_advisory(&db, sbom_id, "high").await;
    create_test_advisory(&db, sbom_id, "medium").await;
    create_test_advisory(&db, sbom_id, "low").await;
    create_test_advisory(&db, sbom_id, "low").await;
    create_test_advisory(&db, sbom_id, "low").await;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should contain correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 3);
    assert_eq!(body["total"], 7);
}

/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let db = setup_test_db().await;
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary for that ID
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    let db = setup_test_db().await;
    let sbom_id = create_test_sbom(&db).await;

    // When requesting the advisory summary for that SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then all severity counts should be zero
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
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM where the same advisory is linked multiple times
    let db = setup_test_db().await;
    let sbom_id = create_test_sbom(&db).await;
    let advisory_id = create_test_advisory(&db, sbom_id, "high").await;
    // Link the same advisory again (duplicate)
    link_advisory_to_sbom(&db, sbom_id, advisory_id).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the duplicate should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["high"], 1);
    assert_eq!(body["total"], 1);
}
```

## Design Decisions

- **Four test functions**: one per Test Requirement in the task description.
- **Individual test functions (not parameterized)**: sibling test files do not use `#[rstest]`
  or parameterized tests; each test is a standalone function.
- **`serde_json::Value` for body parsing**: allows flexible field-level assertions without
  needing to import the `SeveritySummary` struct into the test crate. If sibling tests
  import domain structs directly, adjust accordingly.
- **given-when-then comments**: non-trivial tests with distinct setup, action, and assertion
  phases include section comments.
- **Doc comments on every test**: each test has a `///` doc comment explaining what it verifies.

## Conventions Applied

- Test naming: `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_returns_correct_counts`).
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- Error case: includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- Value-based assertions: asserts on specific field values, not just collection lengths.
- Async test runtime: `#[tokio::test]` matching Axum's async runtime.
- Test setup: uses shared utilities (exact patterns to be confirmed from sibling files at implementation time).

## Notes

- The exact test helper functions (`setup_test_db`, `create_test_sbom`, `create_test_advisory`,
  `link_advisory_to_sbom`) will be confirmed by inspecting the sibling test files. If these
  helpers do not exist, they will be created following the patterns found in `tests/api/advisory.rs`
  and `tests/api/sbom.rs`.
- The HTTP client setup (`client`) will match the pattern used in sibling test files -- likely
  constructed from the test application instance.
- The new test file must be registered in `tests/Cargo.toml` if integration tests require
  explicit listing (to be confirmed by inspecting sibling test configuration).
