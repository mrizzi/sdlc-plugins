## Repository
trustify-backend

## Target Branch
main

## Description
Define the license compliance report response model types and license policy configuration for the new license report feature (TC-9004). This task creates the foundational data structures that the service and endpoint layers will use: the `LicenseGroup` struct (representing packages grouped under a single license with a compliance flag) and the `LicenseReport` struct (the top-level report containing all groups). It also introduces a `LicensePolicy` configuration structure that loads a JSON policy file specifying which licenses are approved, restricted, or denied, enabling configurable compliance checking.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport and LicenseGroup response structs with serde Serialize/Deserialize derives
- `common/src/model/license_policy.rs` — LicensePolicy struct for loading and querying the JSON license policy configuration

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` to export the new model module
- `common/src/model/mod.rs` — add `pub mod license_policy;` to export the policy module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct layout, derive macros, and field naming conventions.
- The `LicenseGroup` struct should contain: `license: String` (SPDX identifier), `packages: Vec<PackageRef>` (list of packages with this license), `compliant: bool` (compliance status per policy).
- The `LicenseReport` struct should contain: `groups: Vec<LicenseGroup>` (all license groups for the SBOM).
- The `LicensePolicy` struct should support loading from a JSON file with categories for approved, restricted, and denied licenses. Use `serde_json` for deserialization.
- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ directory structure for the sbom module.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for any fallible operations in the policy loading logic.
  Applies: task creates `common/src/model/license_policy.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `entity/src/package_license.rs::PackageLicense` — existing SeaORM entity for the package-license mapping; use its field names and types as the basis for the PackageRef sub-struct in LicenseGroup
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes the `license` field; reference its structure for consistent license field naming
- `common/src/error.rs::AppError` — reuse the existing error type for policy loading failures

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs are defined with serde derives and exported from the sbom model module
- [ ] `LicensePolicy` struct can deserialize a JSON policy file specifying approved, restricted, and denied licenses
- [ ] `LicensePolicy` provides a method to check whether a given license identifier is compliant
- [ ] All new types are exported through their respective module `mod.rs` files

## Test Requirements
- [ ] Unit test that `LicensePolicy` correctly deserializes a sample JSON policy file
- [ ] Unit test that `LicensePolicy::is_compliant()` returns true for approved licenses and false for denied licenses
- [ ] Unit test that `LicenseReport` serializes to the expected JSON shape (`{ groups: [{ license, packages, compliant }] }`)

## Dependencies
- None (this is the foundational task)
