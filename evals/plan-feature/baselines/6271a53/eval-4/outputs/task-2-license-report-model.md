# Task 2 — Add license report model structs

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model structs for the license compliance report. These structs define the shape of the API response: packages grouped by license type, with compliance flags per group based on the license policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport and LicenseGroup structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` (see `summary.rs` and `details.rs` for struct conventions)
- Define the following structs with `serde::Serialize`:
  - `LicenseReport` — top-level response containing `groups: Vec<LicenseGroup>`
  - `LicenseGroup` — represents one license type containing:
    - `license: String` — the SPDX license identifier
    - `packages: Vec<PackageLicenseEntry>` — list of packages with this license
    - `compliant: bool` — whether this license is compliant per the policy
  - `PackageLicenseEntry` — individual package info containing:
    - `package_name: String`
    - `version: String`
    - `transitive: bool` — whether this is a transitive dependency
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a license field — reference this for the package-license data shape
- Per constraints (docs/constraints.md) section 4.7: implementation notes must reference existing patterns, not abstract guidance

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs` — SbomSummary struct demonstrates the serde derive pattern and field naming conventions
- `modules/fundamental/src/sbom/model/details.rs` — SbomDetails struct shows how to compose nested response types
- `modules/fundamental/src/package/model/summary.rs` — PackageSummary struct contains the license field that this model will reference

## Acceptance Criteria
- [ ] LicenseReport struct serializes to the expected JSON shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] LicenseGroup correctly represents a license type with its associated packages and compliance status
- [ ] PackageLicenseEntry includes package name, version, and transitive dependency flag

## Test Requirements
- [ ] Unit test: serialize a LicenseReport with multiple groups to JSON and verify the output shape matches the API contract
- [ ] Unit test: verify empty groups produce valid JSON

## Dependencies
None
