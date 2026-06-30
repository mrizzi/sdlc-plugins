# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the GET /api/v2/sbom/{id}/advisory-summary endpoint, covering all four test requirements from the task description.

## Detailed Changes

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    let app = test_app().await;

    // Setup: ingest an SBOM and link advisories with known severities
    // (2 Critical, 1 High, 1 Medium, 0 Low)
    let sbom_id = setup_sbom_with_advisories(&app).await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 2);
    assert_eq!(body.high, 1);
    assert_eq!(body.medium, 1);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 4);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
#[tokio::test]
async fn test_severity_summary_not_found() {
    let app = test_app().await;

    let resp = app
        .get("/api/v2/sbom/nonexistent-id/advisory-summary")
        .await;

    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let app = test_app().await;

    // Setup: ingest an SBOM with no linked advisories
    let sbom_id = setup_empty_sbom(&app).await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummary = resp.json().await;
    assert_eq!(body.critical, 0);
    assert_eq!(body.high, 0);
    assert_eq!(body.medium, 0);
    assert_eq!(body.low, 0);
    assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    let app = test_app().await;

    // Setup: ingest an SBOM and link the same advisory twice
    let sbom_id = setup_sbom_with_duplicate_advisory(&app).await;

    let resp = app
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .await;

    assert_eq!(resp.status(), StatusCode::OK);

    let body: SeveritySummary = resp.json().await;
    // Despite the advisory being linked twice, it should only count once
    assert_eq!(body.total, 1);
}
```

### Design decisions

- **Follows sibling test pattern**: Tests use the same `test_app()` setup, `app.get()` request pattern, `assert_eq!(resp.status(), ...)` status checks, and `.json().await` body deserialization seen in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- **Real PostgreSQL**: Tests run against a real test database, consistent with the project convention (no mocks).
- **Helper functions**: Setup helpers (`setup_sbom_with_advisories`, `setup_empty_sbom`, `setup_sbom_with_duplicate_advisory`) encapsulate test data creation, keeping test functions focused on assertions.
- **Covers all acceptance criteria**: The four tests map directly to the four test requirements in the task description.
