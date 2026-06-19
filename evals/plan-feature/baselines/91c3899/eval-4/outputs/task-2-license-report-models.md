## Repository
trustify-backend

## Target Branch
main

## Description
Add response model structs for the license compliance report endpoint. These models define the shape of the API response: a top-level report containing groups of packages organized by license type, each with a compliance flag.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- LicenseReport and LicenseGroup structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Define `LicenseReport` struct with a `groups: Vec<LicenseGroup>` field.
- Define `LicenseGroup` struct with fields: `license: String`, `packages: Vec<PackageRef>`, `compliant: bool`.
- Define `PackageRef` struct (or reuse existing package summary types) with fields sufficient to identify a package (name, version, purl).
- All structs must derive `Serialize` (for JSON response) and `Debug`.
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` -- see `summary.rs` for `SbomSummary` and `details.rs` for `SbomDetails` as reference for struct layout and derive macros.
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` already includes a `license` field -- reference this for the package-license data model.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- Reference for model struct patterns (derive macros, field types)
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- Existing package model with license field; consider reusing or referencing its type for package data in the report

## Acceptance Criteria
- [ ] `LicenseReport` struct serializes to the expected JSON shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Structs are accessible from the SBOM module's public API
- [ ] All structs derive `Serialize` and `Debug`

## Test Requirements
- [ ] Unit test: serialize a `LicenseReport` with multiple groups and verify JSON output structure
- [ ] Unit test: verify empty report serializes correctly

## Dependencies
- None
