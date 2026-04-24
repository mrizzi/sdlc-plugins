# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation follows the existing advisory severity filter pattern and reuses the shared `apply_filter` query helper.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter to the package list endpoint handler.

**Changes**:

- **Add `license` field to the `Query` struct**: Following the pattern in `modules/fundamental/src/advisory/endpoints/list.rs` where the advisory list endpoint defines a `Query` struct with an optional `severity` field, add an `Option<String>` field named `license` to the package list endpoint's `Query` struct. This field will capture the raw query parameter value (e.g., `"MIT"` or `"MIT,Apache-2.0"`).

  ```rust
  #[derive(Debug, Deserialize)]
  pub struct Query {
      // ... existing pagination/sorting fields ...
      pub license: Option<String>,
  }
  ```

- **Pass the `license` filter to the service layer**: In the handler function, extract `query.license` and pass it to `PackageService::list()` as a new parameter. This mirrors how the advisory list handler passes `query.severity` to `AdvisoryService::list()`.

  ```rust
  pub async fn list(
      Query(query): Query<PackageQuery>,
      // ... other extractors ...
  ) -> Result<Json<PaginatedResults<PackageSummary>>, AppError> {
      let results = service
          .list(/* existing params */, query.license.as_deref())
          .await
          .context("Failed to list packages")?;
      Ok(Json(results))
  }
  ```

- **Add input validation**: Validate that if a `license` value is provided, each comma-separated segment is a non-empty string. Return `AppError` (400 Bad Request) for invalid values such as empty strings, trailing commas, or whitespace-only segments.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Add license filtering logic to the `PackageService::list` method.

**Changes**:

- **Add `license` parameter to the `list` method signature**: Add `license: Option<&str>` as a new parameter to the `PackageService::list()` method.

  ```rust
  pub async fn list(
      &self,
      // ... existing params (pagination, sorting, etc.) ...
      license: Option<&str>,
  ) -> Result<PaginatedResults<PackageSummary>, anyhow::Error> {
  ```

- **Apply the license filter using `apply_filter` from `common/src/db/query.rs`**: When `license` is `Some`, call `apply_filter` to parse the comma-separated value and generate a SQL `IN` clause. This is the same function used by the advisory severity filter -- it handles splitting on commas and building the parameterized query condition.

  ```rust
  use common::db::query::apply_filter;

  // Inside the list method, after building the base query:
  if let Some(license_value) = license {
      query = apply_filter(query, "package_license.license", license_value)?;
  }
  ```

- **Add JOIN to `package_license` table**: When the license filter is active, join through the `entity::package_license` entity to access the license column. Use a SeaORM `JoinType::InnerJoin` on `package_license::Relation::Package` so that only packages with matching licenses are returned. When no license filter is present, skip the join to avoid changing default behavior.

  ```rust
  use entity::package_license;

  if license.is_some() {
      query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
  }
  ```

- **Handle deduplication**: Since the join through `package_license` can produce duplicate package rows (a package may have multiple license entries), add `.distinct()` to the query when the license filter is active to ensure each package appears only once in the results.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the new license filter functionality.

**Changes**:

- **Create the test file** following the same structure as `tests/api/advisory.rs` and `tests/api/sbom.rs`. Use the existing test harness that spins up a PostgreSQL test database.

- **Test cases**:

  1. **`test_filter_single_license`**: Seed test packages with known licenses (e.g., MIT, Apache-2.0, GPL-3.0). Call `GET /api/v2/package?license=MIT`. Assert response status is 200, response body is `PaginatedResults<PackageSummary>`, and all returned packages have `license == "MIT"`.

  2. **`test_filter_multiple_licenses`**: Call `GET /api/v2/package?license=MIT,Apache-2.0`. Assert response status is 200 and returned packages have licenses matching either "MIT" or "Apache-2.0". Assert that GPL-3.0 packages are excluded.

  3. **`test_no_filter_returns_all`**: Call `GET /api/v2/package` (no license parameter). Assert response status is 200 and all seeded packages are returned, confirming no regression.

  4. **`test_invalid_license_returns_400`**: Call `GET /api/v2/package?license=` (empty value). Assert response status is 400 Bad Request. Also test `?license=,` and `?license=MIT,,Apache-2.0` for malformed values.

  5. **`test_nonexistent_license_returns_empty`**: Call `GET /api/v2/package?license=NONEXISTENT`. Assert response status is 200 with an empty results list (not a 404).

- **Register the test module**: Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test crate root if tests are organized differently).

### 4. `tests/api/mod.rs` (modify, if exists)

**Purpose**: Register the new test module.

**Changes**:
- Add `mod package_license_filter;` to include the new test file in the test suite.

## Implementation Order

1. **Service layer first** (`modules/fundamental/src/package/service/mod.rs`): Add the `license` parameter and filtering logic to `PackageService::list()`. This is the core change and can be unit-tested in isolation.

2. **Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`): Add the `license` field to the `Query` struct and wire it through to the service call. Add validation logic.

3. **Integration tests** (`tests/api/package_license_filter.rs`): Write and run the integration tests against all acceptance criteria.

4. **Verify no regression**: Run the full test suite (`cargo test`) to confirm existing package list behavior is unchanged when no license filter is provided.

## Verification Criteria

| Acceptance Criterion | Verification |
|---|---|
| `?license=MIT` returns only MIT packages | `test_filter_single_license` |
| `?license=MIT,Apache-2.0` returns matching packages | `test_filter_multiple_licenses` |
| No license param returns all packages | `test_no_filter_returns_all` |
| Response shape unchanged | All tests assert `PaginatedResults<PackageSummary>` deserialization |
| Invalid license returns 400 | `test_invalid_license_returns_400` |
