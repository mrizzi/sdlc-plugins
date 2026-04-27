## Repository
trustify-backend

## Description
Define the data model structs for the license compliance report response and add license policy configuration support. The report model represents packages grouped by license type with compliance flags. The policy configuration is a JSON file that declares which licenses are allowed, denied, or flagged for review, enabling organizations to customize compliance rules.

## Files to Modify
- `common/src/model/mod.rs` — re-export the new license report model types

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseReport`, `LicenseGroup`, and `LicensePolicy` structs with serde Serialize/Deserialize
- `modules/fundamental/src/sbom/model/license_policy.rs` — define `LicensePolicyConfig` struct for reading JSON policy files, with a loader function

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model struct derives `Serialize, Deserialize, Debug, Clone` and lives in its own file under the module's `model/` directory.
- The `LicenseReport` struct should contain a `groups` field of type `Vec<LicenseGroup>`.
- The `LicenseGroup` struct should contain: `license: String`, `packages: Vec<PackageSummary>`, `compliant: bool`.
- Reference `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` which already includes a `license` field — reuse this type for the package entries within each group.
- The `LicensePolicyConfig` struct should support: `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>`, and `review_required_licenses: Vec<String>`.
- The policy loader should accept a file path and return `Result<LicensePolicyConfig, AppError>` following the error handling pattern in `common/src/error.rs` using `.context()` wrapping.
- Register the new model files in `modules/fundamental/src/sbom/model/mod.rs`.
- Per docs/constraints.md 4.6: all file paths are based on real paths discovered from the repository structure.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already contains a `license` field; reuse as the package representation within each license group instead of defining a new package struct
- `common/src/error.rs::AppError` — existing error enum with `IntoResponse` implementation; use for policy file loading errors
- `common/src/model/paginated.rs::PaginatedResults` — reference for how shared model types are structured and exported in this codebase

## Acceptance Criteria
- [ ] `LicenseReport` struct is defined with a `groups: Vec<LicenseGroup>` field
- [ ] `LicenseGroup` struct is defined with `license`, `packages`, and `compliant` fields
- [ ] `LicensePolicyConfig` struct is defined with `allowed_licenses`, `denied_licenses`, and `review_required_licenses` fields
- [ ] Policy loader function reads a JSON file and returns `Result<LicensePolicyConfig, AppError>`
- [ ] All new types derive `Serialize, Deserialize, Debug, Clone`
- [ ] New model files are registered in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Unit test: `LicensePolicyConfig` deserializes correctly from a valid JSON string
- [ ] Unit test: `LicensePolicyConfig` returns an appropriate error for malformed JSON
- [ ] Unit test: `LicenseReport` serializes to the expected JSON shape `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Verification Commands
- `cargo check -p fundamental` — expected: compiles without errors
- `cargo test -p fundamental -- license` — expected: all license-related unit tests pass
