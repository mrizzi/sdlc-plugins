# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

**What was checked:**
This criterion requires that when the `license` query parameter is set to a single SPDX identifier (e.g., `MIT`), the endpoint filters the results to return only packages matching that license.

**Evidence from the diff:**

1. **Parameter parsing (list.rs):** The `PackageListParams` struct now includes `pub license: Option<String>`, which captures the `license` query parameter from the request URL.

2. **Validation (list.rs):** The `validate_license_param` function parses comma-separated license identifiers. For a single value like `MIT`, it produces a `Vec<String>` containing `["MIT"]`. Each identifier is validated against the SPDX expression parser (`Expression::parse(id)`), ensuring only valid SPDX identifiers are accepted.

3. **Filter application (service/mod.rs):** The `list` method now accepts `license_filter: Option<&[String]>`. When provided, it applies a SeaORM filter:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   This joins the `package_license` table and filters by the `License` column matching the provided identifiers. For a single value `["MIT"]`, `is_in` effectively becomes an equality check.

4. **Test coverage (tests/api/package.rs):** The test `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), requests `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items are returned
   - All returned items have `license == "MIT"`

**Conclusion:** The implementation correctly parses the single license parameter, validates it, applies the database filter via an inner join on `package_license`, and the integration test verifies the expected behavior. This criterion is satisfied.
