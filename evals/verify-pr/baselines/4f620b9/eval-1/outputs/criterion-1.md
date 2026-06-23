# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through two complementary code changes:

### Endpoint Layer (`modules/fundamental/src/package/endpoints/list.rs`)

1. **Parameter parsing**: The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will automatically populate from the `?license=MIT` query parameter.

2. **Validation**: The `validate_license_param` function splits the license string by comma, trims whitespace, and validates each identifier against the SPDX expression parser (`spdx::Expression::parse`). For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.

3. **Handler wiring**: The `list_packages` handler maps the optional license parameter through `validate_license_param` and passes the result to `PackageService::list` as `license_filter`.

### Service Layer (`modules/fundamental/src/package/service/mod.rs`)

4. **Query filtering**: When `license_filter` is `Some`, the service applies:
   - A `Condition::any()` filter with `package_license::Column::License.is_in(licenses)` -- for a single license `["MIT"]`, this produces a `WHERE license IN ('MIT')` clause
   - An `InnerJoin` to the `PackageLicense` relation, ensuring only packages with a matching license row are returned

5. **Pagination preservation**: The filter is applied before `count()` and the paginated query, so `total` reflects the filtered count and `items` contains only filtered results.

### Test Coverage

The test `test_list_packages_single_license_filter` directly validates this criterion:
- Seeds 3 packages (2 MIT, 1 Apache-2.0)
- Queries `?license=MIT`
- Asserts status 200, exactly 2 results, and all results have `license == "MIT"`

## Evidence

- `PackageListParams.license: Option<String>` field added
- `validate_license_param("MIT")` returns `Ok(vec!["MIT".to_string()])`
- `Condition::any().add(package_license::Column::License.is_in(["MIT"]))` filters to MIT-only packages
- `InnerJoin` on `PackageLicense` ensures only packages with license records are included
- Test asserts `body.items.len() == 2` and `body.items.iter().all(|p| p.license == "MIT")`
