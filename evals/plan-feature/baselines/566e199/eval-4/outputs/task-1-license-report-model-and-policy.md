# Task 1 — Add license report response model and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model structs for the license compliance report and the license policy configuration type. The report groups packages by license and flags non-compliant licenses based on a configurable JSON policy file. This task creates the foundational types that the service and endpoint tasks will consume.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `license_report` module

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport`, `LicenseGroup`, and `PackageRef` structs with serde Serialize derives
- `common/src/model/license_policy.rs` — `LicensePolicy` struct with `allowed_licenses` and `denied_licenses` fields, serde Deserialize, and a method to evaluate compliance for a given license string
- `license-policy.json` — default license policy configuration file at the repository root with example allowed/denied license lists (e.g., MIT, Apache-2.0 allowed; GPL-3.0 denied)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`: define structs with `#[derive(Clone, Debug, Serialize)]` and expose them via `mod.rs` re-export.
- The `LicenseGroup` struct should contain: `license: String`, `packages: Vec<PackageRef>`, `compliant: bool`.
- The `LicenseReport` struct should contain: `groups: Vec<LicenseGroup>`.
- The `PackageRef` struct should contain at minimum: `name: String`, `version: String` — reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` for field naming conventions.
- The `LicensePolicy` struct in `common/src/model/license_policy.rs` should include a `check_compliance(&self, license: &str) -> bool` method. A license is compliant if it appears in `allowed_licenses` (when the list is non-empty) and does not appear in `denied_licenses`.
- Load the policy from a configurable file path (environment variable or default path). Follow the error handling pattern in `common/src/error.rs` using `AppError` and `.context()`.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field on packages; reference for field naming and type conventions
- `common/src/error.rs::AppError` — error type to use for policy file loading failures
- `common/src/model/paginated.rs::PaginatedResults` — example of a shared response model in the `common` crate; follow the same derive and module registration pattern

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageRef` structs exist and derive `Serialize`
- [ ] `LicensePolicy` struct exists with `allowed_licenses` and `denied_licenses` fields and a `check_compliance` method
- [ ] A default `license-policy.json` file exists at the repo root with example allowed/denied license entries
- [ ] All new types are re-exported from their parent modules
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Unit tests for `LicensePolicy::check_compliance` covering: license in allowed list returns true, license in denied list returns false, license in neither list with non-empty allowed list returns false, empty allowed list with no denied match returns true
- [ ] Unit test for `LicensePolicy` deserialization from JSON string

## Verification Commands
- `cargo check` — compiles without errors
- `cargo test --lib` — all unit tests pass
