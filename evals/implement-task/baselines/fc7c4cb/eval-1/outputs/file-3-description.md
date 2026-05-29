# File 3: tests/api/advisory_summary.rs (CREATE)

## Purpose

New integration test file for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all four test requirements from the task.

## Detailed Changes

Create a new test file with four test functions:

### Test 1: `test_advisory_summary_returns_correct_counts`

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    // (seed test DB with SBOM and linked advisories: 2 critical, 1 high, 3 medium, 0 low)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should contain correct counts per severity level
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: `test_advisory_summary_not_found`

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: `test_advisory_summary_empty_sbom`

```rust
/// Verifies that an SBOM with no linked advisories returns all-zero severity counts.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    // (seed test DB with SBOM but no advisory links)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", empty_sbom_id))
        .send()
        .await;

    // Then all severity counts should be zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: `test_advisory_summary_deduplicates`

```rust
/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links
    // (seed test DB with SBOM linked to the same advisory twice via sbom_advisory)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then duplicates should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // If the duplicate advisory is critical-severity, expect 1 not 2
    assert_eq!(summary.critical, 1);
    assert_eq!(summary.total, 1);
}
```

### Design Decisions

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` matching sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Response validation**: Asserts on specific field values (not just counts or lengths), ensuring test failures reveal what changed.
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern consistent with sibling tests.
- **Given-When-Then**: All tests use `// Given`, `// When`, `// Then` section comments since they have distinct setup, action, and assertion phases.
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies, per the skill's documentation requirement.
- **Test setup**: Each test sets up its own data in the test database, following the independence pattern in sibling test files.
- **Error cases**: Includes 404 test consistent with sibling test files.

### Convention Conformance

- Matches the test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- Uses `#[tokio::test]` for async test functions (Rust async test convention).
- Asserts on specific values, not just collection lengths.
