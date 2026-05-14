## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Evidence

The PR implements single-license filtering through the following code path:

1. **Query parameter parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
   The `PackageListParams` struct adds a `pub license: Option<String>` field. When a request arrives with `?license=MIT`, this field is populated with `Some("MIT")`.

2. **Validation** (`list.rs` -- `validate_license_param`):
   The `validate_license_param` function splits the license string by comma, trims whitespace, and validates each identifier against the `spdx::Expression::parse` function. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.

3. **Filter application** (`modules/fundamental/src/package/service/mod.rs`):
   The `list` method receives `license_filter: Option<&[String]>`. When `Some`, it applies:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   This inner-joins the `package_license` table and filters using `IS IN ('MIT')`, which correctly returns only packages whose license matches `MIT`.

4. **Test coverage** (`tests/api/package.rs` -- `test_list_packages_single_license_filter`):
   The test seeds three packages (two MIT, one Apache-2.0), requests `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned
   - All items have `license == "MIT"`

### Conclusion

The endpoint handler parses the `license` query parameter, validates it as a valid SPDX identifier, passes it to the service layer which applies an `IS IN` filter via an inner join on the `package_license` table, and returns only matching packages. The integration test confirms the expected behavior. This criterion is satisfied.
