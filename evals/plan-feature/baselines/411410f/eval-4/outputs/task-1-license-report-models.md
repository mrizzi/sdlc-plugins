# Task 1: Define license report data models

## Repository
trustify-backend

## Target Branch
main

## Description
Define the data models for the license compliance report response. These structs represent the structured output of the license report endpoint: a top-level report containing groups of packages organized by license type, each with a compliance status flag.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Data model structs for the license compliance report response

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition conventions (derive macros, serde attributes).
- Define the following structs:
  - `LicenseReport` — top-level response containing a `Vec<LicenseGroup>` and summary metadata (total packages, total violations)
  - `LicenseGroup` — represents one license type group with fields: `license: String`, `packages: Vec<LicensePackageRef>`, `compliant: bool`
  - `LicensePackageRef` — minimal package reference with fields: `name: String`, `version: String`, `purl: Option<String>`
- All structs should derive `Clone, Debug, Serialize, Deserialize` and use `#[serde(rename_all = "camelCase")]` to match the existing API JSON conventions.
- The `compliant` field on `LicenseGroup` indicates whether the license is allowed by the configured policy.

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `LicensePackageRef` structs are defined in `modules/fundamental/src/sbom/model/license_report.rs`
- [ ] All structs derive Serialize and Deserialize for JSON serialization
- [ ] Module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying `LicenseReport` serializes to the expected JSON structure: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }], "totalPackages": N, "totalViolations": N }`
- [ ] Unit test verifying deserialization round-trip for `LicenseReport`
