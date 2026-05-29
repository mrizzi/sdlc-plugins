# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

### What was checked

This criterion requires that the endpoint accepts a `license` query parameter and, when set to a single SPDX identifier like `MIT`, returns only packages matching that license.

### Evidence from the diff

**1. Query parameter parsing (`list.rs`):**
The `PackageListParams` struct now includes `pub license: Option<String>`, which means Axum's `Query` extractor will parse `?license=MIT` from the URL and populate this field.

**2. Validation (`list.rs`):**
The `validate_license_param` function splits the license string by comma, trims whitespace, and validates each identifier using `spdx::Expression::parse()`. For a single value like `MIT`, this produces a `Vec<String>` containing one element `["MIT"]`.

**3. Filtering (`service/mod.rs`):**
The `list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, it adds a `Condition::any()` filter using `package_license::Column::License.is_in(licenses.iter().cloned())` and joins `package::Relation::PackageLicense`. This produces a SQL WHERE clause that filters packages to only those whose license column matches one of the provided values. For a single `MIT` value, this effectively becomes `WHERE license IN ('MIT')`.

**4. Test coverage (`tests/api/package.rs`):**
The test `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), requests `?license=MIT`, and asserts:
- Response status is 200 OK
- Result contains exactly 2 items
- All items have `license == "MIT"`

This test directly validates the criterion behavior.

### Conclusion

The implementation correctly adds the `license` query parameter, validates it as a valid SPDX identifier, and filters the database query to return only matching packages. The test confirms the expected behavior with concrete assertions on both count and license values.
