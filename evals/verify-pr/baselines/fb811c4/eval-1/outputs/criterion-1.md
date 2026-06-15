# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

The `license` query parameter is added to `PackageListParams` as `pub license: Option<String>`. When present, `validate_license_param` parses the parameter value by splitting on commas and validating each identifier as a valid SPDX expression via `Expression::parse(id)`. The validated identifiers are passed to `PackageService::list` as `license_filter: Option<&[String]>`.

In the service layer, when a license filter is provided, the query builder applies:
```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
```

This produces an SQL query with `WHERE license IN ('MIT')` and an `INNER JOIN` to the `package_license` table, ensuring only packages with the specified license are returned.

## Evidence

- `list.rs`: `PackageListParams` gains `pub license: Option<String>` field
- `list.rs`: `validate_license_param` splits on comma, validates each as SPDX expression
- `service/mod.rs`: Applies `Condition::any().add(package_license::Column::License.is_in(...))` filter
- `tests/api/package.rs`: `test_list_packages_single_license_filter` seeds MIT and Apache-2.0 packages, filters by MIT, asserts `body.items.len() == 2` and `body.items.iter().all(|p| p.license == "MIT")`
