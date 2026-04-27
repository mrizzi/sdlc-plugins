# File 3: Create `tests/api/advisory_summary.rs`

## Action: CREATE

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the four test requirements specified in the task.

## Detailed Changes

### Imports

```rust
use axum::http::StatusCode;
use serde_json::Value;
// Additional imports for test setup, HTTP client, test database fixtures
// following the patterns in tests/api/advisory.rs and tests/api/sbom.rs
```

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that querying an SBOM with known linked advisories returns
/// the correct count for each severity level.
#[tokio::test]
async fn test_advisory_summary_returns_correct_severity_counts() {
    // Given an SBOM with linked advisories of known severities
    //   - 2 Critical, 1 High, 3 Medium, 0 Low
    // (set up via test database fixtures following sibling test patterns)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response contains correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 1);
    assert_eq!(body["medium"], 3);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM
/// returns HTTP 404 Not Found.
#[tokio::test]
async fn test_advisory_summary_not_found_for_missing_sbom() {
    // Given a non-existent SBOM ID
    let fake_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts set to zero.
#[tokio::test]
async fn test_advisory_summary_empty_sbom_returns_zeros() {
    // Given an SBOM with no linked advisories
    // (create an SBOM in the test DB without linking any advisories)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", empty_sbom_id))
        .send()
        .await;

    // Then all counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}
```

### Test 4: Duplicate advisory links are deduplicated in the count

```rust
/// Verifies that duplicate advisory-SBOM links are deduplicated, so each
/// advisory is counted only once in the severity summary.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisory_links() {
    // Given an SBOM where the same advisory is linked twice
    //   - 1 Critical advisory linked via two sbom_advisory rows

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_with_dupes_id))
        .send()
        .await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let body: Value = resp.json().await;
    assert_eq!(body["critical"], 1);
    assert_eq!(body["total"], 1);
}
```

## Conventions Applied

- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_returns_correct_severity_counts`)
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization and field-level assertions, matching sibling test files
- **Value-based assertions**: Asserts on specific field values (not just counts or lengths)
- **Error case coverage**: Includes 404 test matching the pattern in sibling test files
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies
- **Given-When-Then**: Section comments (`// Given`, `// When`, `// Then`) in each test body since all tests have distinct setup, action, and assertion phases
- **Async tests**: Uses `#[tokio::test]` for async test functions
- **Test database**: Uses real PostgreSQL test database, matching the project's integration test approach
