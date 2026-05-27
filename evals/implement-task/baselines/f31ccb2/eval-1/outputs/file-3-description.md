# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering all acceptance criteria and test requirements from TC-9201.

## Detailed Changes

Create a new test file following the patterns established in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

### Test Structure

The test file uses the project's integration test infrastructure, which runs against a real PostgreSQL database with test fixtures.

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    // Setup: create test SBOM and link advisories with known severities
    // - 2 Critical advisories
    // - 3 High advisories
    // - 1 Medium advisory
    // - 0 Low advisories
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    create_linked_advisories(&app, sbom_id, &[
        ("adv-1", "Critical"),
        ("adv-2", "Critical"),
        ("adv-3", "High"),
        ("adv-4", "High"),
        ("adv-5", "High"),
        ("adv-6", "Medium"),
    ]).await;

    // Act: call the endpoint
    let response = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    // Assert: verify status and counts
    assert_eq!(response.status(), 200);
    let body: serde_json::Value = response.json().await;
    assert_eq!(body["critical"], 2);
    assert_eq!(body["high"], 3);
    assert_eq!(body["medium"], 1);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 6);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    let app = setup_test_app().await;
    let fake_id = "non-existent-sbom-id";

    let response = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", fake_id))
        .await;

    assert_eq!(response.status(), 404);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    // No advisories linked to this SBOM

    let response = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(response.status(), 200);
    let body: serde_json::Value = response.json().await;
    assert_eq!(body["critical"], 0);
    assert_eq!(body["high"], 0);
    assert_eq!(body["medium"], 0);
    assert_eq!(body["low"], 0);
    assert_eq!(body["total"], 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    let app = setup_test_app().await;
    let sbom_id = create_test_sbom(&app).await;
    // Link the same advisory to the SBOM multiple times
    let advisory_id = create_test_advisory(&app, "Critical").await;
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await;
    link_advisory_to_sbom(&app, sbom_id, advisory_id).await; // duplicate link

    let response = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(response.status(), 200);
    let body: serde_json::Value = response.json().await;
    assert_eq!(body["critical"], 1); // deduplicated: only counted once
    assert_eq!(body["total"], 1);
}
```

### Helper Functions

The test file will use helper functions for test setup. These either reuse existing helpers from `tests/api/` or define new ones:

- `setup_test_app()` — initializes the Axum test server with a clean database (likely already exists in test infrastructure)
- `create_test_sbom()` — inserts a test SBOM record and returns its ID
- `create_test_advisory()` — inserts a test advisory with a given severity
- `create_linked_advisories()` — batch creates advisories and links them to an SBOM
- `link_advisory_to_sbom()` — creates an entry in the `sbom_advisory` join table

The exact helper implementations depend on the existing test infrastructure patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

### Module Registration

The test file also needs to be registered in `tests/api/` if there is a `mod.rs` or if Cargo auto-discovers test files. For Cargo integration tests, files in `tests/` are auto-discovered, but if `tests/api/` is a subdirectory module, a `mod advisory_summary;` line may need to be added to `tests/api/mod.rs` (if it exists). This should be confirmed by inspecting the test infrastructure.

## Conventions Applied

- Tests in `tests/api/` directory, matching existing test organization
- Uses real PostgreSQL database for integration testing
- Tests verify both HTTP status codes and JSON response body content
- Each test function is `#[tokio::test]` async
- Test names are descriptive and follow `test_` prefix convention
- Tests cover positive cases, error cases, edge cases, and data integrity (deduplication)
