## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Analysis

**What the criterion requires:**
The endpoint must accept a `license` query parameter and, when set to a single SPDX identifier like `MIT`, return only packages whose license matches that identifier.

**Evidence from the PR diff:**

1. **Query parameter parsing (`list.rs`):**
   The `PackageListParams` struct now includes a `pub license: Option<String>` field. Axum's `Query` extractor will automatically deserialize `?license=MIT` into this field. This is consistent with the existing `offset` and `limit` parameters.

2. **Validation (`list.rs`):**
   The `validate_license_param` function splits the license string by commas, trims whitespace, and validates each identifier against the `spdx::Expression::parse` function. For a single value like `MIT`, this produces `Ok(vec!["MIT".to_string()])`. The validated identifiers are passed to the service layer.

3. **Filtering (`service/mod.rs`):**
   The `PackageService::list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, it applies:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   The `is_in` filter with a single-element slice effectively becomes `WHERE package_license.license = 'MIT'`. The `InnerJoin` ensures only packages with matching license records are returned.

4. **Test coverage (`tests/api/package.rs`):**
   The `test_list_packages_single_license_filter` test seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, asserts `StatusCode::OK`, verifies that exactly 2 items are returned, and confirms all items have `license == "MIT"`. This directly validates the criterion.

**Conclusion:**
The code correctly adds the `license` query parameter, validates it, filters using a SQL `IN` clause with inner join to the license table, and the test confirms correct behavior for a single license filter. The criterion is satisfied.
