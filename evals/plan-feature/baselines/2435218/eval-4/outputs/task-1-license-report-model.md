# Task 1 — Add license compliance report response model

## Repository
trustify-backend

## Description
Define the response model structs for the license compliance report endpoint. The report groups packages by license type and includes a compliance flag per group based on a license policy. This task creates the data structures that the service and endpoint layers will use.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declaration for the new license report model

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseReportGroup` and `LicenseReport` structs

## Implementation Notes
- Follow the existing model pattern in the SBOM module. See `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for struct definition conventions (derive macros, serde attributes, field naming).
- The `LicenseReport` struct should contain a `groups` field of type `Vec<LicenseReportGroup>`.
- The `LicenseReportGroup` struct should contain:
  - `license: String` — the SPDX license identifier
  - `packages: Vec<PackageSummary>` — list of packages with this license (reuse the existing `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`)
  - `compliant: bool` — whether this license is compliant with the configured policy
- Derive `Serialize`, `Deserialize`, `Clone`, `Debug` to match existing model conventions.
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` already includes a `license` field — reuse it directly rather than creating a new package representation.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package model that includes the license field; use as the package type within each license group
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct definition conventions (derive macros, serde attributes)

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseReportGroup` structs are defined in `modules/fundamental/src/sbom/model/license_report.rs`
- [ ] Structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] `LicenseReportGroup` reuses `PackageSummary` for its package list
- [ ] Module is declared in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Verify that `LicenseReport` serializes to the expected JSON shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Verify that `LicenseReport` round-trips through serde (serialize then deserialize produces equivalent struct)

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
