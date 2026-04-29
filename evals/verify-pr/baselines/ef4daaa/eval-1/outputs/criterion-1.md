# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR diff introduces the `license` query parameter to the `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs`:

```rust
pub license: Option<String>,
```

When the `license` parameter is present, the `validate_license_param` function parses the comma-separated string into individual identifiers. The `list_packages` handler then passes the parsed license filter to `PackageService::list()`.

In `modules/fundamental/src/package/service/mod.rs`, the `list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, it applies an `is_in` filter on `package_license::Column::License` with an `InnerJoin` to the `PackageLicense` relation. For a single value like `MIT`, the `is_in` clause contains only `["MIT"]`, which filters to only packages whose license matches MIT.

The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds three packages (two MIT, one Apache-2.0), queries with `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned
- All items have `license == "MIT"`

This test directly validates the criterion. The implementation correctly filters by a single license value.
