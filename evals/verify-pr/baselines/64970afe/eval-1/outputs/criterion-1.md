## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

The `PackageListParams` struct now includes an optional `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When present, the `license` parameter is passed through `validate_license_param`, which splits on commas and validates each identifier as a valid SPDX expression using `spdx::Expression::parse`. For a single value like `MIT`, this produces a `Vec<String>` containing one element `["MIT"]`.

The validated identifiers are forwarded to `PackageService::list` as `license_filter: Option<&[String]>`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

The service applies the filter using SeaORM's `Condition::any()` with `is_in`:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This generates a SQL `WHERE package_license.license IN ('MIT')` clause with an `INNER JOIN` on the `package_license` table, ensuring only packages with a matching license are returned.

**Test coverage (`tests/api/package.rs`):**

`test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned
- All returned items have `license == "MIT"`

This directly verifies the criterion.
