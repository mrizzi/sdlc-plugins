## Repository
trustify-backend

## Target Branch
main

## Description
Add model structs for the license compliance report feature. This includes a `LicenseGroup` struct that represents a group of packages sharing the same license type with a compliance flag, and a `LicenseReport` struct that aggregates all license groups for an SBOM. These models will be used by the service layer and serialized as the API response for the license report endpoint.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declarations for the new license report model

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseGroup` and `LicenseReport` structs with serde serialization

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model file defines a struct with `#[derive(Serialize, Deserialize, Debug, Clone)]` and implements any necessary `From` conversions.
- The `LicenseGroup` struct should contain: `license: String` (the SPDX license identifier), `packages: Vec<PackageSummary>` (list of packages with this license), and `compliant: bool` (whether this license is compliant with the project policy).
- The `LicenseReport` struct should contain: `groups: Vec<LicenseGroup>` representing all license groups for the SBOM.
- Reuse the `PackageSummary` struct from `modules/fundamental/src/sbom/../package/model/summary.rs` to represent packages within each group — do not duplicate package representation.
- The `package_license.rs` entity in `entity/src/package_license.rs` maps packages to licenses — the model structs should align with the data this entity provides.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the established model struct pattern with serde derives and field conventions
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — shows the detail-level model pattern with nested struct references
- `entity/src/package_license.rs` — existing package-license mapping entity that provides the underlying data relationship

## Acceptance Criteria
- [ ] `LicenseGroup` struct is defined with `license`, `packages`, and `compliant` fields
- [ ] `LicenseReport` struct is defined with a `groups` field containing a `Vec<LicenseGroup>`
- [ ] Both structs derive `Serialize`, `Deserialize`, `Debug`, and `Clone`
- [ ] Module is properly declared in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying `LicenseReport` serializes to the expected JSON structure: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Unit test verifying deserialization round-trip for `LicenseReport`

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental -- license_report` — unit tests pass

## Dependencies
- None

[sdlc-workflow] Description digest: sha256:83a0cb5db972a89a19971a1c599fdb60e242c8601d8ae0f10542c9d89f3c608e
