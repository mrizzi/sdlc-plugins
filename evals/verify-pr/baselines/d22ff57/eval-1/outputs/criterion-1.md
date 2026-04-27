## Criterion 1

**Text:** `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Evidence

1. **Query parameter parsing** (`modules/fundamental/src/package/endpoints/list.rs`): The `PackageListParams` struct now includes `pub license: Option<String>`, which allows Axum's `Query` extractor to bind the `?license=MIT` query parameter.

2. **Validation** (`list.rs`): The `validate_license_param` function splits the license string on commas and validates each identifier via `spdx::Expression::parse(id)`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.

3. **Filter application** (`modules/fundamental/src/package/service/mod.rs`): When `license_filter` is `Some`, the service applies:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   This inner-joins the `package_license` table and filters to rows where the license column matches the provided identifiers. For `["MIT"]`, only MIT-licensed packages are returned.

4. **Test coverage** (`tests/api/package.rs`): `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned (the two MIT packages)
   - All returned items have `license == "MIT"`

### Verdict: PASS
