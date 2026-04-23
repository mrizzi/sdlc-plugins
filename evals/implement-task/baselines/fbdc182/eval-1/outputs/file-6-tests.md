# File 6 — Create: `tests/api/advisory_summary.rs`

## Purpose

Integration tests for `GET /api/v2/sbom/{id}/advisory-summary`. Tests hit a real PostgreSQL test database following the pattern in sibling files `tests/api/advisory.rs` and `tests/api/sbom.rs`.

## Inspection Step

Before writing, read:
- `tests/api/advisory.rs` — confirm test setup helpers (fixture creation, app initialization), assertion patterns, and test naming
- `tests/api/sbom.rs` — confirm 404 pattern and how SBOM fixtures are created in tests
- `tests/Cargo.toml` — confirm available test dependencies (`tokio`, `reqwest` or `axum::test`, `uuid`, etc.)

Key patterns to extract from sibling test files:
- How the test app is initialized (likely a shared helper like `create_test_app()` or a fixture)
- How SBOMs and advisories are seeded into the test database
- How HTTP requests are made (likely `reqwest::Client` or `axum::test::TestClient`)
- How responses are deserialized
- Whether tests use `#[tokio::test]` or a custom test macro

## Full File Content

```rust
//! Integration tests for GET /api/v2/sbom/{id}/advisory-summary

use reqwest::StatusCode;  // or `axum_test::TestClient` — match sibling pattern

// Import test helpers from sibling tests (exact paths confirmed by reading siblings)
use crate::common::{create_test_app, seed_sbom, seed_advisory, seed_sbom_advisory_link};

// Import the response struct for deserialization
use fundamental::advisory::model::severity_summary::SeveritySummary;

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given a test app and an SBOM with advisories at known severity levels
    let app = create_test_app().await;
    let sbom_id = seed_sbom(&app).await;
    let adv_critical = seed_advisory(&app, "Critical").await;
    let adv_high = seed_advisory(&app, "High").await;
    let adv_medium_1 = seed_advisory(&app, "Medium").await;
    let adv_medium_2 = seed_advisory(&app, "Medium").await;
    seed_sbom_advisory_link(&app, sbom_id, adv_critical).await;
    seed_sbom_advisory_link(&app, sbom_id, adv_high).await;
    seed_sbom_advisory_link(&app, sbom_id, adv_medium_1).await;
    seed_sbom_advisory_link(&app, sbom_id, adv_medium_2).await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .expect("request failed");

    // Then the response is 200 with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await.expect("failed to deserialize body");
    assert_eq!(body.critical, 1, "expected 1 critical advisory");
    assert_eq!(body.high, 1, "expected 1 high advisory");
    assert_eq!(body.medium, 2, "expected 2 medium advisories");
    assert_eq!(body.low, 0, "expected 0 low advisories");
    assert_eq!(body.total, 4, "expected total of 4 advisories");
}

/// Verifies that requesting a summary for a non-existent SBOM returns HTTP 404.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a test app and a SBOM ID that does not exist in the database
    let app = create_test_app().await;
    let nonexistent_id = uuid::Uuid::new_v4(); // or appropriate ID type

    // When requesting the advisory summary for the non-existent SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{nonexistent_id}/advisory-summary"))
        .send()
        .await
        .expect("request failed");

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given a test app and an SBOM with no advisory links
    let app = create_test_app().await;
    let sbom_id = seed_sbom(&app).await;

    // When requesting the advisory summary for that SBOM
    let resp = app
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .expect("request failed");

    // Then the response is 200 with all counts at zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await.expect("failed to deserialize body");
    assert_eq!(body.critical, 0, "expected 0 critical advisories");
    assert_eq!(body.high, 0, "expected 0 high advisories");
    assert_eq!(body.medium, 0, "expected 0 medium advisories");
    assert_eq!(body.low, 0, "expected 0 low advisories");
    assert_eq!(body.total, 0, "expected total of 0 advisories");
}

/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM where the same advisory is linked twice (duplicate join entries)
    let app = create_test_app().await;
    let sbom_id = seed_sbom(&app).await;
    let adv_id = seed_advisory(&app, "High").await;
    seed_sbom_advisory_link(&app, sbom_id, adv_id).await;
    seed_sbom_advisory_link(&app, sbom_id, adv_id).await; // duplicate link

    // When requesting the advisory summary
    let resp = app
        .get(&format!("/api/v2/sbom/{sbom_id}/advisory-summary"))
        .send()
        .await
        .expect("request failed");

    // Then duplicates are deduplicated — count is 1, not 2
    assert_eq!(resp.status(), StatusCode::OK);
    let body: SeveritySummary = resp.json().await.expect("failed to deserialize body");
    assert_eq!(body.high, 1, "expected 1 unique high advisory after deduplication");
    assert_eq!(body.total, 1, "expected total of 1 unique advisory after deduplication");
}
```

## Notes on test helper functions

The exact names of `create_test_app`, `seed_sbom`, `seed_advisory`, and `seed_sbom_advisory_link` must be confirmed by reading `tests/api/advisory.rs` and `tests/api/sbom.rs`. These helpers likely already exist for advisory and SBOM fixture creation — reuse them rather than inventing new ones.

If `seed_advisory` does not accept a severity parameter, read how it creates advisories and either extend it or use an existing variant that sets severity.

## Registration requirement

After writing this file, the test module must be registered. Check `tests/Cargo.toml` or look for a `tests/api/mod.rs` that lists sub-modules. Add:

```rust
// In tests/api/mod.rs or tests/lib.rs:
pub mod advisory_summary;
```

This file (`tests/api/mod.rs`) may or may not be listed in the task's Files to Create — if it isn't, it is a small addition within scope since it is required for the test file to compile. Flag it to the user during the scope containment check in Step 9.

## Convention compliance

- File lives in `tests/api/` alongside `advisory.rs` and `sbom.rs`
- Test naming follows `test_<endpoint>_<scenario>` pattern
- `///` doc comment on every test function
- Given-When-Then section comments in all four tests (non-trivial setup)
- Assertions use `assert_eq!` with message strings for diagnostic clarity
- Value-based assertions used throughout — not just count checks
- 404 test included matching sibling convention
- No parameterized tests used — the four scenarios have distinct setup/teardown structures, so separate functions are preferred (matching project convention from sibling analysis)
