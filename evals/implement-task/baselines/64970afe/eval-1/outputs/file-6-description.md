# File 6: `tests/api/advisory_summary.rs` (CREATE)

## Pre-creation inspection

Before creating this file, inspect sibling test files to match conventions:
- Read or `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs` to see test function signatures, assertion patterns, test setup/teardown, naming conventions, and how test fixtures are created.
- Read or `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs` to see SBOM-related test patterns, particularly how SBOM IDs are obtained for test requests.
- Check `tests/Cargo.toml` to understand test dependencies (HTTP client, assertion crates, test database setup).

Also check if `tests/api/mod.rs` exists and whether new test modules need to be registered there.

## Test cases

The Test Requirements specify 4 test cases. Each test function will have a `///` doc comment and given-when-then section comments.

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with known linked advisories returns the correct
/// severity counts, with each severity level accurately represented.
#[tokio::test]
async fn test_advisory_summary_valid_sbom_with_advisories() {
    // Given an SBOM with known advisories at various severity levels
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_test_advisory(&app, sbom_id, "Critical").await;
    create_test_advisory(&app, sbom_id, "Critical").await;
    create_test_advisory(&app, sbom_id, "High").await;
    create_test_advisory(&app, sbom_id, "Medium").await;
    create_test_advisory(&app, sbom_id, "Low").await;
    create_test_advisory(&app, sbom_id, "Low").await;
    create_test_advisory(&app, sbom_id, "Low").await;

    // When requesting the advisory severity summary
    let resp = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the response should be 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 1);
    assert_eq!(summary.low, 3);
    assert_eq!(summary.total, 7);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting the advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response, consistent with existing SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID
    let app = setup_test_app().await;
    let nonexistent_id = "00000000-0000-0000-0000-000000000000";

    // When requesting the advisory severity summary
    let resp = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", nonexistent_id))
        .send()
        .await;

    // Then the response should be 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a severity summary
/// where all severity counts and the total are zero.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;

    // When requesting the advisory severity summary
    let resp = app
        .client()
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
/// Verifies that when the same advisory is linked to an SBOM multiple times
/// (via duplicate entries in the sbom_advisory join table), the severity summary
/// counts each advisory only once by deduplicating on advisory ID.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with a single advisory linked multiple times
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    let advisory_id = create_test_advisory(&app, sbom_id, "High").await;
    // Link the same advisory again (duplicate join table entry)
    link_advisory_to_sbom(&app, advisory_id, sbom_id).await;
    link_advisory_to_sbom(&app, advisory_id, sbom_id).await;

    // When requesting the advisory severity summary
    let resp = app
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    // Then the advisory should be counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.high, 1);
    assert_eq!(summary.total, 1);
    // Other severity levels should be zero
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
}
```

## Module registration

If `tests/api/mod.rs` exists and uses explicit module declarations, add:
```rust
mod advisory_summary;
```

If tests are auto-discovered (no `mod.rs`), no registration is needed.

## Conventions followed

- **Assertion style**: Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by `resp.json::<T>().await` body deserialization -- matches `tests/api/advisory.rs` and `tests/api/sbom.rs` patterns.
- **Response validation**: Asserts on specific field values (e.g., `summary.critical == 2`), not just counts -- follows "prefer value-based assertions over length-only checks" guidance.
- **Error cases**: Includes a 404 test case matching the pattern in sibling test files.
- **Test naming**: Follows `test_<endpoint>_<scenario>` pattern (e.g., `test_advisory_summary_nonexistent_sbom`).
- **Test setup**: Uses the project's test fixture infrastructure (`setup_test_app`, `create_test_sbom`, etc.) -- exact function names to be confirmed from sibling inspection.
- **Given-When-Then**: All tests include `// Given`, `// When`, `// Then` section comments as required by SKILL.md.
- **Documentation**: Every test function has a `///` doc comment explaining what it verifies, as required by SKILL.md (overrides sibling convention if siblings lack doc comments).
- **Parameterized tests**: Not used -- sibling tests use individual test functions, and we follow that existing convention.
- **No trivial tests**: All tests have distinct setup, action, and assertion phases, so given-when-then comments are appropriate for all.
