# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint to allow
filtering packages by their declared SPDX license identifier. Support both single-value
and comma-separated multi-value filtering.

## Repository

trustify-backend (Serena instance: `serena_backend`)

## Target Branch

main

## Branch

`TC-9203` (created from `main`)

---

## Step 4 — Understand the Code

### Files to inspect

1. **`modules/fundamental/src/package/endpoints/list.rs`** — current list endpoint handler;
   use `get_symbols_overview` via `mcp__serena_backend__get_symbols_overview` to see the
   existing Query struct and handler function signature.
2. **`modules/fundamental/src/package/service/mod.rs`** — current PackageService list method;
   inspect how it builds the database query and returns `PaginatedResults<PackageSummary>`.
3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (Reuse Candidate / sibling) —
   use `get_symbols_overview` to understand the severity filter pattern: the Query struct
   with an optional `severity` field, how it calls `apply_filter`, and how the filter
   is plumbed into the service layer.
4. **`common/src/db/query.rs`** (Reuse Candidate) — use `find_symbol` with `include_body=true`
   on `apply_filter` to read its full implementation: understand the signature, how it parses
   comma-separated values, and how it generates the SQL `IN` clause.
5. **`entity/src/package_license.rs`** (Reuse Candidate) — inspect the SeaORM entity to
   understand the join table schema (columns, relations, primary key) for the package-license
   mapping.
6. **`modules/fundamental/src/package/model/summary.rs`** — verify `PackageSummary` already
   includes a `license` field (as stated in repo-backend.md); confirm the response shape.
7. **`modules/fundamental/src/package/endpoints/mod.rs`** — check route registration to
   understand how the list handler is mounted.

### Sibling / convention analysis

- Compare `advisory/endpoints/list.rs` (severity filter) with `package/endpoints/list.rs`
  to confirm both follow the same Query struct + handler pattern.
- Compare `advisory/service/advisory.rs` with `package/service/mod.rs` to confirm the
  service-layer filter plumbing pattern.
- Review `tests/api/advisory.rs` for test conventions (assertion style, setup, naming).

### Documentation files

- `docs/api.md` — check if it documents the `GET /api/v2/package` endpoint; if so, update
  to mention the new `license` query parameter.
- `CONVENTIONS.md` — read for CI check commands and project-level conventions.

---

## Step 6 — Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Current state (expected):** Contains a `Query` struct (or similar) for query parameter
extraction and a handler function that calls `PackageService::list()`.

**Changes:**

1. **Add `license` field to the Query struct:**
   ```rust
   #[derive(Debug, Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, search) ...
       /// Optional SPDX license identifier filter. Supports comma-separated values
       /// for multi-license filtering (e.g., "MIT,Apache-2.0").
       pub license: Option<String>,
   }
   ```
   Follow the exact pattern used in the advisory list endpoint's Query struct for
   the `severity` field (Reuse Candidate: `advisory/endpoints/list.rs`).

2. **Pass the license filter to the service layer:**
   In the handler function, extract `query.license` and pass it to
   `PackageService::list()` as an additional parameter. Follow the same approach
   used in the advisory handler for passing the severity filter.

3. **Add input validation:**
   If `license` contains values, validate that each comma-separated token is
   non-empty. Return `400 Bad Request` via `AppError` for invalid values (empty
   strings after splitting). Follow the error handling convention:
   `Result<T, AppError>` with `.context()` wrapping.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Current state (expected):** Contains `PackageService` with a `list` method that
builds a SeaORM query, applies pagination/sorting, and returns
`PaginatedResults<PackageSummary>`.

**Changes:**

1. **Add `license` parameter to the `list` method signature:**
   ```rust
   pub async fn list(
       &self,
       // ... existing params ...
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Apply the license filter using `apply_filter` from `common/src/db/query.rs`:**
   Reuse the `apply_filter` function (Reuse Candidate) to handle comma-separated
   parsing and SQL `IN` clause generation. This is the same utility the advisory
   service uses for severity filtering.

3. **Add a JOIN to `package_license` entity:**
   When the `license` filter is present, join through the `package_license` table
   (Reuse Candidate: `entity/src/package_license.rs`) to filter packages by their
   associated license SPDX identifier. Use SeaORM's relation-based join API
   rather than raw SQL:
   ```rust
   if let Some(ref license) = license {
       // Join package_license table
       query = query.join(
           JoinType::InnerJoin,
           entity::package_license::Relation::Package.def().rev(),
       );
       // Apply filter using shared helper
       query = apply_filter(query, &license, entity::package_license::Column::License);
   }
   ```
   The exact column name for the SPDX identifier will be confirmed by inspecting
   `entity/src/package_license.rs` during Step 4.

4. **Ensure no duplicate results:**
   When joining through `package_license` with multi-value filtering, a package
   matching multiple licenses could appear multiple times. Apply `.distinct()` to
   the query when the license filter is active, following the pattern used in
   sibling service methods.

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create integration tests following the conventions found in `tests/api/advisory.rs`
and other sibling test files.

```rust
/// Integration tests for the package license filter on GET /api/v2/package.

/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_filter_single_license() {
    // Given a database seeded with packages having MIT and Apache-2.0 licenses
    // ... setup: seed test packages with different licenses ...

    // When requesting packages filtered by MIT
    let resp = client.get("/api/v2/package?license=MIT").send().await;

    // Then only MIT-licensed packages are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert!(body.items.iter().all(|p| p.license == "MIT"));
    // Assert on specific expected package names/identifiers, not just count
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[tokio::test]
async fn test_list_packages_filter_multiple_licenses() {
    // Given a database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses

    // When requesting packages filtered by MIT and Apache-2.0
    let resp = client.get("/api/v2/package?license=MIT,Apache-2.0").send().await;

    // Then packages with either MIT or Apache-2.0 are returned, but not GPL-3.0
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert!(body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0"));
    // Assert on specific expected items
}

/// Verifies that omitting the license parameter returns all packages (no regression).
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given a database seeded with packages having various licenses

    // When requesting packages without a license filter
    let resp = client.get("/api/v2/package").send().await;

    // Then all packages are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    // Assert total count matches expected seed data count
    // Assert specific known packages are present
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_returns_400() {
    // When requesting packages with an invalid (empty) license value
    let resp = client.get("/api/v2/package?license=").send().await;

    // Then a 400 Bad Request is returned
    assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
}
```

All tests follow the sibling conventions:
- `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Body deserialization into `PaginatedResults<PackageSummary>`
- Value-based assertions on item fields (not just length checks)
- `test_<endpoint>_<scenario>` naming convention
- Doc comment on every test function
- Given/When/Then section comments for non-trivial tests

### Additional integration points

- **`tests/Cargo.toml`**: Add `mod package_license_filter;` to the test module
  declarations (or ensure the new test file is picked up by the test harness).
- **`docs/api.md`** (if it documents the package endpoint): Add the `license` query
  parameter to the endpoint documentation.

---

## Step 8 — Acceptance Criteria Verification

| Criterion | Verification |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | `test_list_packages_filter_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns either | `test_list_packages_filter_multiple_licenses` |
| No license param returns all packages | `test_list_packages_no_license_filter` |
| Response shape unchanged | All tests deserialize into `PaginatedResults<PackageSummary>` |
| Invalid license returns 400 | `test_list_packages_invalid_license_returns_400` |

## Step 9 — Self-Verification Checklist

- Scope containment: only `list.rs`, `service/mod.rs`, and the new test file are touched.
- No sensitive patterns in diff.
- Data-flow trace: request param -> endpoint extraction -> service filter -> DB query with JOIN -> filtered response. Complete path.
- Duplication check: no new utility functions created; all filtering logic delegates to existing `apply_filter`.
- Contract & sibling parity: follows the same patterns as advisory severity filter.
- Documentation currency: update `docs/api.md` if it documents the package endpoint.

## Step 10 — Commit

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package supporting
single and comma-separated SPDX identifier filtering. Reuses the existing
apply_filter helper and package_license entity join table.

Implements TC-9203
```
