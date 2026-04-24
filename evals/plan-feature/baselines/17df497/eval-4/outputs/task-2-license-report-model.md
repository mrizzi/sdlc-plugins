# Task 2 — Add license report response model

## Repository
trustify-backend

## Description
Define the response types for the license compliance report endpoint. The report groups all packages in an SBOM by their license identifier, includes the list of packages under each license, and flags whether each group is compliant with the configured license policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReportGroup` and `LicenseReport` structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` — see `summary.rs` and `details.rs` for the established struct conventions (derive macros, serde attributes)
- Define the following structs:
  - `LicenseReportGroup`:
    - `license: String` — SPDX license identifier
    - `packages: Vec<PackageRef>` — list of packages with this license
    - `compliant: bool` — whether this license is compliant with the policy
  - `PackageRef`:
    - `name: String` — package name
    - `version: String` — package version
    - `transitive: bool` — whether this is a transitive dependency
  - `LicenseReport`:
    - `sbom_id: String` — the SBOM identifier
    - `groups: Vec<LicenseReportGroup>` — license groups
    - `compliant: bool` — overall compliance (true only if all groups are compliant)
- All structs should derive `Serialize`, `Debug`, `Clone` for API response serialization
- The response shape matches the feature requirement: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct definition patterns, serde derives, and serialization conventions
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — reference for complex response type structure
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference for the `license` field representation

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseReportGroup` structs serialize to the expected JSON shape
- [ ] `LicenseReport.compliant` is `true` only when all groups have `compliant: true`
- [ ] Structs follow the same derive and attribute patterns as existing model types

## Test Requirements
- [ ] Unit test: serialize a `LicenseReport` to JSON and verify the output shape matches the spec
- [ ] Unit test: `LicenseReport` with all compliant groups has `compliant: true`
- [ ] Unit test: `LicenseReport` with any non-compliant group has `compliant: false`

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and default policy file
