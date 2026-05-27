## Criterion 1: Single License Filter

**Text:** `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict:** PASS

**Reasoning:**

The diff in `list.rs` adds a `license: Option<String>` field to `PackageListParams`. When present, `validate_license_param(license)` parses and validates the SPDX identifier via `Expression::parse(id)`. The validated identifiers are passed to `PackageService::list()`.

In `service/mod.rs`, the service applies the filter using `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` with an inner join to `PackageLicense`. This returns only packages whose license matches the specified identifier.

The test `test_list_packages_single_license_filter` seeds MIT and Apache-2.0 packages, filters by MIT, and asserts `body.items.len() == 2` with all items having `license == "MIT"`.
