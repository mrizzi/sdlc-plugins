# File 6: Create `tests/api/advisory_summary.rs`

## Purpose

Integration tests for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all 4 test requirements from the task description.

## Detailed Changes

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with known advisory links returns the correct severity
/// counts per level and the correct total.
#[tokio::test]
async fn test_get_advisory_summary_with_advisories() {
    // Given an SBOM with advisories at known severity levels:
    //   - 2 Critical, 1 High, 3 Medium, 0 Low
    // (Set up test SBOM, advisories, and sbom_advisory join records)

    // When requesting the advisory summary endpoint
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns HTTP 404, consistent with other SBOM-scoped endpoints.
#[tokio::test]
async fn test_get_advisory_summary_not_found() {
    // Given a non-existent SBOM ID
    let fake_id = "non-existent-sbom-id";

    // When requesting the advisory summary endpoint
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary with all
/// severity counts set to zero and total set to zero.
#[tokio::test]
async fn test_get_advisory_summary_empty() {
    // Given an SBOM with no advisory links
    // (Set up test SBOM with no sbom_advisory records)

    // When requesting the advisory summary endpoint
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be 200 OK with all zeros
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that when an SBOM has duplicate links to the same advisory (multiple
/// sbom_advisory records pointing to the same advisory ID), the advisory is
/// counted only once in the severity summary.
#[tokio::test]
async fn test_get_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate links to the same advisory:
    //   - Advisory A (Critical) linked twice via sbom_advisory
    //   - Advisory B (High) linked once
    // (Set up test SBOM, advisories, and duplicate sbom_advisory records)

    // When requesting the advisory summary endpoint
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should count each advisory only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);  // Advisory A counted once despite two links
    assert_eq!(summary.high, 1);      // Advisory B counted once
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2);     // Only 2 unique advisories
}
```

## Convention Compliance

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by `resp.json::<T>().await` for body deserialization -- matches sibling test files
- **Response validation**: Asserts on specific field values (not just lengths), verifying each severity level count individually
- **Error cases**: Includes 404 test using `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` -- matches sibling pattern
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_summary_not_found`)
- **Test setup**: Uses shared test database with fixture creation before assertions
- **Test organization**: Success case first, then 404, then edge cases
- **Doc comments**: Every test function has a `///` doc comment explaining what it verifies (per SKILL.md requirement)
- **Given-When-Then**: All tests include `// Given`, `// When`, `// Then` section comments (non-trivial tests with setup)
- **Parameterized tests**: NOT used -- sibling test files do not use `#[rstest]`, so individual test functions are used per convention conformance
- **Value-based assertions**: Asserts on specific count values per severity level rather than just checking total or length
