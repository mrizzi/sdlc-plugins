# File 6: tests/api/advisory_summary.rs

**Action**: Create (new file)
**Purpose**: Integration tests for the advisory severity summary endpoint

## Pre-Implementation Inspection

Before creating, would use Serena to inspect sibling test files:
- `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` -- understand test structure, assertion patterns, setup helpers
- `mcp__serena_backend__find_symbol` on test functions in `tests/api/advisory.rs` with `include_body=true` -- read full test implementations
- `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` -- cross-domain test comparison
- `mcp__serena_backend__search_for_pattern` for `StatusCode::NOT_FOUND` in tests/api/ -- understand 404 test pattern
- `mcp__serena_backend__search_for_pattern` for `assert_eq!` in tests/api/ -- understand assertion style
- Check for `#[rstest]` or `#[case]` usage in siblings to determine if parameterized tests are used

## File Contents

```rust
//! Integration tests for the advisory severity summary endpoint.

use axum::http::StatusCode;
// ... additional imports matching sibling test files

/// Verifies that a valid SBOM with known advisories returns the correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (create test SBOM, link advisories with Critical=2, High=3, Medium=1, Low=0)
    let sbom = create_test_sbom().await;
    let _adv1 = create_test_advisory("critical").await;
    let _adv2 = create_test_advisory("critical").await;
    let _adv3 = create_test_advisory("high").await;
    let _adv4 = create_test_advisory("high").await;
    let _adv5 = create_test_advisory("high").await;
    let _adv6 = create_test_advisory("medium").await;
    // Link advisories to SBOM via sbom_advisory join table

    // When requesting the severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .await;

    // Then the response should contain correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 3);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that requesting a severity summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    // Given a non-existent SBOM ID
    let non_existent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", non_existent_id))
        .await;

    // Then the response should be 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all severity counts as zero.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let sbom = create_test_sbom().await;

    // When requesting the severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .await;

    // Then all counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links to the same SBOM are deduplicated in the severity count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with the same advisory linked multiple times
    let sbom = create_test_sbom().await;
    let adv = create_test_advisory("high").await;
    // Link the same advisory to the SBOM twice (duplicate join entries)
    link_advisory_to_sbom(&adv, &sbom).await;
    link_advisory_to_sbom(&adv, &sbom).await;

    // When requesting the severity summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom.id))
        .await;

    // Then the advisory should only be counted once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1);  // Not 2 -- deduplicated
    assert_eq!(summary.total, 1);
}
```

## Test Requirements Coverage

| Test Requirement | Test Function | Status |
|---|---|---|
| Valid SBOM with known advisories returns correct severity counts | `test_severity_summary_with_known_advisories` | Covered |
| Non-existent SBOM ID returns 404 | `test_severity_summary_sbom_not_found` | Covered |
| SBOM with no advisories returns all zeros | `test_severity_summary_no_advisories` | Covered |
| Duplicate advisory links are deduplicated in the count | `test_severity_summary_deduplicates_advisories` | Covered |

## Key Patterns Followed

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- **Value-based assertions**: Asserts on specific field values (e.g., `summary.critical == 2`), not just collection lengths, per skill requirements.
- **Error case**: Includes 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling patterns.
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_severity_summary_sbom_not_found`).
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies.
- **Given-When-Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- **Test isolation**: Each test creates its own data and does not depend on other tests.
- **Real database**: Tests hit a real PostgreSQL test database per project convention (not mocked).
- **Parameterized tests**: Would follow sibling pattern -- if siblings do not use `#[rstest]`, individual test functions are used instead (as shown above).

## Test Module Registration

The new test file `tests/api/advisory_summary.rs` may need to be registered in `tests/Cargo.toml` or a test module declaration file, depending on the project's test organization. Would verify this by inspecting how `tests/api/sbom.rs` and `tests/api/advisory.rs` are registered.
