## Repository
trustify-backend

## Description
Define the response model structs for the license compliance report and implement a license policy configuration loader. The report model will represent packages grouped by license type with a compliance flag per group. The policy configuration will be loaded from a JSON file that defines which licenses are allowed, denied, or flagged for review.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Response model structs: `LicenseReport`, `LicenseGroup` (containing license name, list of packages, and `compliant: bool` flag)
- `common/src/license_policy.rs` — License policy configuration struct and JSON loader; defines `LicensePolicy` with allowed/denied license lists and a `check(license: &str) -> bool` method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the policy module

## Implementation Notes
Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definitions with serde `Serialize`/`Deserialize` derives. The `LicenseReport` struct should contain a `groups: Vec<LicenseGroup>` field. Each `LicenseGroup` should have fields: `license: String`, `packages: Vec<PackageRef>` (a lightweight reference with package name and version), and `compliant: bool`. The `PackageRef` struct should be minimal to avoid duplicating the full `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`.

For the license policy, use `serde_json` to deserialize a config file. The policy struct should support an `allowed_licenses` list (if present, only these are compliant) and a `denied_licenses` list (these are always non-compliant). If both are specified, `denied_licenses` takes precedence. Reference `common/src/error.rs` for the `AppError` enum pattern when returning configuration load errors.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the `license` field on packages; reference this struct's license field type for consistency
- `common/src/error.rs::AppError` — Use for error handling in policy file loading

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs are defined with serde derives and compile successfully
- [ ] `LicensePolicy` struct can be deserialized from a JSON file with `allowed_licenses` and `denied_licenses` fields
- [ ] `LicensePolicy::check()` returns correct compliance status for allowed, denied, and unlisted licenses
- [ ] New modules are properly exported from their parent `mod.rs` files

## Test Requirements
- [ ] Unit test: `LicensePolicy` with only `allowed_licenses` correctly flags licenses not in the list
- [ ] Unit test: `LicensePolicy` with only `denied_licenses` correctly flags denied licenses as non-compliant
- [ ] Unit test: `LicensePolicy` with both lists, verifying `denied_licenses` takes precedence
- [ ] Unit test: `LicenseReport` serializes to expected JSON shape matching the API contract `{ groups: [{ license, packages, compliant }] }`

## Verification Commands
- `cargo build -p common` — Compiles without errors
- `cargo build -p trustify-module-fundamental` — Compiles without errors
- `cargo test -p common -- license_policy` — All policy unit tests pass
