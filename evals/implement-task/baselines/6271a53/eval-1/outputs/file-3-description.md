# File 3: `tests/api/advisory_summary.rs` (CREATE)

## Purpose

Integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the four required test scenarios.

## Conventions Applied

- Follows the test pattern from sibling files `tests/api/advisory.rs` and `tests/api/sbom.rs`
- Uses `#[tokio::test]` async test functions
- Uses the test harness for real PostgreSQL database setup
- Makes HTTP requests to the test server and asserts on status codes and JSON bodies
- Test function names are descriptive snake_case

## Detailed Content

```rust
use serde_json::json;
use trustify_test::TestContext;

/// Test that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_with_advisories() {
    let ctx = TestContext::setup().await;

    // Set up test data: create an SBOM and link advisories with known severities
    let sbom_id = ctx.create_sbom("test-sbom-1").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-0001", "Critical").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-0002", "Critical").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-0003", "High").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-0004", "Medium").await;
    ctx.create_advisory_for_sbom(sbom_id, "CVE-2024-0005", "Low").await;

    let response = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    assert_eq!(response.status(), 200);

    let body: serde_json::Value = response.json().await;
    assert_eq!(body, json!({
        "critical": 2,
        "high": 1,
        "medium": 1,
        "low": 1,
        "total": 5
    }));
}

/// Test that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_sbom_not_found() {
    let ctx = TestContext::setup().await;

    let response = ctx
        .client()
        .get("/api/v2/sbom/00000000-0000-0000-0000-000000000000/advisory-summary")
        .send()
        .await;

    assert_eq!(response.status(), 404);
}

/// Test that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_no_advisories() {
    let ctx = TestContext::setup().await;

    let sbom_id = ctx.create_sbom("test-sbom-empty").await;

    let response = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    assert_eq!(response.status(), 200);

    let body: serde_json::Value = response.json().await;
    assert_eq!(body, json!({
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "total": 0
    }));
}

/// Test that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    let ctx = TestContext::setup().await;

    let sbom_id = ctx.create_sbom("test-sbom-dedup").await;

    // Link the same advisory twice to the SBOM
    let advisory_id = ctx.create_advisory("CVE-2024-1000", "High").await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;
    ctx.link_advisory_to_sbom(advisory_id, sbom_id).await;

    let response = ctx
        .client()
        .get(&format!("/api/v2/sbom/{}/advisory-summary", sbom_id))
        .send()
        .await;

    assert_eq!(response.status(), 200);

    let body: serde_json::Value = response.json().await;
    // Should count as 1, not 2
    assert_eq!(body, json!({
        "critical": 0,
        "high": 1,
        "medium": 0,
        "low": 0,
        "total": 1
    }));
}
```

## Design Decisions

1. **Test data setup**: Uses helper methods (e.g., `ctx.create_sbom`, `ctx.create_advisory_for_sbom`) that follow the patterns established in existing test files. The exact helper method names would be adjusted to match actual test utilities during implementation.

2. **Non-existent SBOM uses a zeroed UUID**: This is a common pattern in integration tests to test 404 behavior with an ID that is syntactically valid but does not correspond to any existing record.

3. **Deduplication test**: Creates a single advisory and links it to the SBOM twice via the join table, then asserts that the count reflects 1 unique advisory, not 2 rows.

4. **Full JSON body assertions**: Rather than checking individual fields, the tests assert on the entire JSON body to ensure no unexpected fields are present and all expected fields have correct values.

## Test Registration

The test file also needs to be registered in `tests/Cargo.toml` (or equivalent test harness configuration) as a test binary or included via the test module structure. This would follow the pattern of how `tests/api/advisory.rs` and `tests/api/sbom.rs` are registered.
