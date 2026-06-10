# File 6: tests/api/advisory_summary.rs

**Action**: CREATE

**Purpose**: Integration tests for the new GET /api/v2/sbom/{id}/advisory-summary endpoint, covering all four test requirements specified in the task.

## Detailed Changes

Create a new test file with the following structure:

```rust
//! Integration tests for the advisory severity summary endpoint.
//!
//! Tests the GET /api/v2/sbom/{id}/advisory-summary endpoint which returns
//! aggregated severity counts for advisories linked to an SBOM.

use reqwest::StatusCode;
// Additional imports would be confirmed from sibling test files
// (tests/api/advisory.rs, tests/api/sbom.rs)

/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (setup: create test SBOM, create advisories with specific severities,
    //  link them via sbom_advisory join table)
    let sbom = create_test_sbom().await;
    let _adv_critical = create_test_advisory(&sbom, "Critical").await;
    let _adv_high_1 = create_test_advisory(&sbom, "High").await;
    let _adv_high_2 = create_test_advisory(&sbom, "High").await;
    let _adv_medium = create_test_advisory(&sbom, "Medium").await;

    // When requesting the advisory summary for the SBOM
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .send()
        .await
        .unwrap();

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the severity counts match the expected values
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 1);
    assert_eq!(summary.high, 2);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 4);
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = "non-existent-sbom-id";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .send()
        .await
        .unwrap();

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let sbom = create_test_sbom().await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .send()
        .await
        .unwrap();

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And all severity counts are zero
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM where the same advisory is linked multiple times
    let sbom = create_test_sbom().await;
    let advisory = create_test_advisory(&sbom, "High").await;
    // Link the same advisory again (duplicate link in sbom_advisory)
    link_advisory_to_sbom(&advisory, &sbom).await;

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .send()
        .await
        .unwrap();

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the advisory is counted only once
    let summary: SeveritySummary = resp.json().await.unwrap();
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 1);
}
```

## Conventions Followed

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization -- matching sibling tests in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Response validation**: asserts on specific field values (not just counts/lengths) -- per SKILL.md Step 7 guidance on value-based assertions.
- **Error cases**: includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` -- matching sibling test convention.
- **Test naming**: `test_advisory_summary_<scenario>` pattern -- following `test_<endpoint>_<scenario>` convention from siblings.
- **Test organization**: one file for the new endpoint, in `tests/api/` directory.
- **Documentation**: every test function has a `///` doc comment explaining what it verifies -- per SKILL.md Step 7 requirement for AI-generated tests.
- **Given-When-Then**: all tests include `// Given`, `// When`, `// Then` section comments -- per SKILL.md Step 7 requirement for non-trivial tests.
- **Parameterized tests**: not used, since sibling tests do not use `#[rstest]` -- following existing project convention.
- **Test database**: integration tests hit a real PostgreSQL test database -- matching the project convention.

## Notes

- The exact test setup helpers (e.g., `create_test_sbom()`, `create_test_advisory()`, `link_advisory_to_sbom()`) would be confirmed by inspecting sibling test files to see what test utilities already exist. Would reuse existing test helpers rather than creating new ones where possible.
- The HTTP client setup and base URL configuration would follow the pattern in sibling tests.
- The `tests/Cargo.toml` may need updating to include the new test file as a test target, depending on how the test harness is configured. Would check this during implementation.
