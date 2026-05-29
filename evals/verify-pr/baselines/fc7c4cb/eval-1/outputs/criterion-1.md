## Criterion 1

**Text**: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### What was checked

Examined the PR diff for the full request path: query parameter extraction, validation, service-layer filtering, and test coverage.

### Code evidence

1. **Parameter extraction** (`modules/fundamental/src/package/endpoints/list.rs`): The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will automatically deserialize from `?license=MIT`.

2. **Validation** (`modules/fundamental/src/package/endpoints/list.rs`): The `validate_license_param` function splits on comma, trims whitespace, and parses each identifier via `spdx::Expression::parse()`. For a single value like `MIT`, this produces `Ok(vec!["MIT".to_string()])`.

3. **Filtering** (`modules/fundamental/src/package/service/mod.rs`): When `license_filter` is `Some`, the service applies:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   This inner-joins to the `package_license` table and filters with `WHERE license IN ('MIT')`, ensuring only packages with MIT license are returned.

4. **Test coverage** (`tests/api/package.rs`): `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries `?license=MIT`, and asserts:
   - Status is 200 OK
   - Exactly 2 items returned (the two MIT-licensed packages)
   - All items have `license == "MIT"`

### Verdict: PASS

The endpoint correctly extracts the `license` query parameter, validates it as a valid SPDX identifier, filters at the database level using an `IN` clause on the `package_license` table, and a test confirms only MIT-licensed packages are returned.
