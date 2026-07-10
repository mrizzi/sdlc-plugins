## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model types for the license compliance report endpoint. This introduces
`LicenseGroup` and `LicenseReport` structs that represent the grouped license data returned
by `GET /api/v2/sbom/{id}/license-report`. The `LicenseGroup` struct captures a single
license type with its associated packages and a compliance flag. The `LicenseReport` struct
wraps a collection of `LicenseGroup` entries for a given SBOM.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseGroup` and `LicenseReport` response structs with serde Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` and re-export the new types

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: response shape `{ groups: [{ license: String, packages: [PackageSummary], compliant: bool }] }` (model types only; endpoint wiring in Task 3)

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and
`modules/fundamental/src/sbom/model/details.rs` for struct definition conventions (derive
macros, field visibility, documentation comments).

The `LicenseGroup` struct should contain:
- `license: String` — the SPDX license identifier
- `packages: Vec<PackageSummary>` — packages using this license (reuse the existing `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`)
- `compliant: bool` — whether this license is compliant with the configured policy

The `LicenseReport` struct should contain:
- `groups: Vec<LicenseGroup>` — license groups for the SBOM

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` directory structure for the SBOM module.
Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's module directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the struct definition pattern (derives, field types) used for SBOM response models
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — demonstrates the detailed response model pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — the existing package summary struct that includes the `license` field; reuse directly in `LicenseGroup.packages`

## Acceptance Criteria
- [ ] `LicenseGroup` struct is defined with `license`, `packages`, and `compliant` fields
- [ ] `LicenseReport` struct is defined with a `groups` field containing `Vec<LicenseGroup>`
- [ ] Both structs derive `Serialize` and `Deserialize`
- [ ] New module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Unit test verifying `LicenseReport` serializes to the expected JSON shape `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Unit test verifying `LicenseReport` deserializes from a valid JSON string
- [ ] Unit test verifying an empty `groups` array serializes correctly

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
