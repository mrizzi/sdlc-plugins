# File 6: tests/api/advisory_summary.rs (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests verify correct severity counts, 404 for non-existent SBOMs, zero counts for empty SBOMs, and deduplication of advisory links.

## Pre-change Inspection

Before creating, inspect sibling test files to understand patterns:
```
mcp__serena_backend__get_symbols_overview("tests/api/advisory.rs")
mcp__serena_backend__get_symbols_overview("tests/api/sbom.rs")
```

Read specific test functions to understand:
- How the test database is set up
- How HTTP requests are made to the test server
- How responses are asserted on
- How test fixtures (SBOMs, advisories) are created

Also check `tests/Cargo.toml` for test dependencies and module registration.

## File Contents

```rust
//! Integration tests for the advisory severity summary endpoint.

use reqwest::StatusCode;

// Additional imports would match sibling test files -- test harness, fixtures, etc.

/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels:
    //   - 2 Critical advisories
    //   - 3 High advisories
    //   - 1 Medium advisory
    //   - 0 Low advisories
    // (Create test SBOM and link advisories using service methods or direct DB seeding)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request should succeed");

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And the response body contains correct severity counts
    let summary: SeveritySummary = resp.json().await.expect("valid JSON response");
    assert_eq!(summary.critical, 2, "expected 2 critical advisories");
    assert_eq!(summary.high, 3, "expected 3 high advisories");
    assert_eq!(summary.medium, 1, "expected 1 medium advisory");
    assert_eq!(summary.low, 0, "expected 0 low advisories");
    assert_eq!(summary.total, 6, "expected 6 total advisories");
}

/// Verifies that requesting a summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await
        .expect("request should succeed");

    // Then the response status is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty_sbom() {
    // Given an SBOM with no linked advisories
    // (Create test SBOM without linking any advisories)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", empty_sbom_id))
        .send()
        .await
        .expect("request should succeed");

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And all severity counts are zero
    let summary: SeveritySummary = resp.json().await.expect("valid JSON response");
    assert_eq!(summary.critical, 0, "expected 0 critical advisories");
    assert_eq!(summary.high, 0, "expected 0 high advisories");
    assert_eq!(summary.medium, 0, "expected 0 medium advisories");
    assert_eq!(summary.low, 0, "expected 0 low advisories");
    assert_eq!(summary.total, 0, "expected 0 total advisories");
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicated() {
    // Given an SBOM with the same advisory linked multiple times
    //   - Advisory A (Critical) linked 3 times via different sbom_advisory rows
    //   - Advisory B (High) linked 2 times
    // (Create test SBOM and insert duplicate sbom_advisory rows)

    // When requesting the advisory summary
    let resp = client
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await
        .expect("request should succeed");

    // Then the response status is 200 OK
    assert_eq!(resp.status(), StatusCode::OK);

    // And each advisory is counted only once despite duplicate links
    let summary: SeveritySummary = resp.json().await.expect("valid JSON response");
    assert_eq!(summary.critical, 1, "Advisory A counted once despite 3 links");
    assert_eq!(summary.high, 1, "Advisory B counted once despite 2 links");
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 2, "only 2 unique advisories");
}
```

## Design Decisions

1. **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization, matching sibling test files in `tests/api/`.

2. **Value-based assertions**: Asserts on specific count values rather than just checking structure. Each assertion includes a descriptive message explaining what is expected, per SKILL.md requirement for value-based assertions over length-only checks.

3. **Error case coverage**: Includes a 404 test for non-existent SBOM, matching the sibling test pattern where all endpoint test suites include a not-found test.

4. **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_valid_sbom`), consistent with sibling tests.

5. **Doc comments**: Every test function has a `///` doc comment explaining what it verifies, per SKILL.md mandate. This applies even if sibling tests do not have doc comments.

6. **Given-When-Then**: Non-trivial tests include `// Given`, `// When`, `// Then` section comments for structure, per SKILL.md requirement.

7. **Deduplication test**: Tests that duplicate `sbom_advisory` rows for the same advisory are properly deduplicated, directly covering acceptance criterion #3.

## Notes

- The exact test setup code (creating test SBOMs, advisories, linking them) depends on the project's test infrastructure. Would inspect sibling tests to understand fixture creation patterns.
- If the project uses a test database setup/teardown pattern (e.g., per-test transaction rollback), the same pattern would be applied here.
- May need to add a `mod advisory_summary;` declaration in the test crate root or `tests/Cargo.toml` depending on how the test suite discovers test modules.
- If siblings use `#[rstest]` for parameterized tests, would evaluate whether the empty/valid/dedup scenarios share enough structure to parameterize. Given that each test has distinct setup (different fixture configurations), individual test functions are more appropriate per the Meszaros heuristic.
