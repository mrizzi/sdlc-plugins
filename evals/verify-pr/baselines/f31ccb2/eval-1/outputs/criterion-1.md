## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Reasoning

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `PackageListParams` struct now includes `pub license: Option<String>`, so Axum will deserialize the `?license=MIT` query parameter into this field.
- When `params.license` is `Some("MIT")`, the handler calls `validate_license_param("MIT")` which splits on comma (yielding `["MIT"]`), then validates each identifier via `spdx::Expression::parse("MIT")`. "MIT" is a valid SPDX identifier, so validation passes and returns `Ok(vec!["MIT".to_string()])`.
- The validated list is passed to `PackageService::list()` as `Some(&["MIT"])`.

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- When `license_filter` is `Some(["MIT"])`, the service builds a `Condition::any()` with `package_license::Column::License.is_in(["MIT"])` and adds an `InnerJoin` on `package::Relation::PackageLicense`.
- This effectively filters the query to only return packages that have a row in the `package_license` table with `license = 'MIT'`.
- The total count and item retrieval both operate on this filtered query, ensuring only MIT-licensed packages appear in the response.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), requests `?license=MIT`, and asserts:
  - Response status is 200 OK
  - Exactly 2 items returned
  - All items have `license == "MIT"`

The implementation correctly filters by a single license value and the test validates the behavior end-to-end.
