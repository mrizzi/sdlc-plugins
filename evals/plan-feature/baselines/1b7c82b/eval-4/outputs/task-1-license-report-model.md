## Repository
trustify-backend

## Target Branch
main

## Description
Define the model structs for the license compliance report. This provides the data structures that the service layer will populate and the endpoint will serialize as JSON. The report groups packages by license type, each group indicating whether that license is compliant with the project's policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Model structs: `LicenseReport`, `LicenseGroup`, and `LicensePackageEntry`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/`. The sibling files `summary.rs` and `details.rs` demonstrate the conventions: derive `Serialize`, `Deserialize`, `Clone`, and `Debug` on all structs; use `serde` rename attributes for JSON field naming if needed.

Struct definitions:

- `LicensePackageEntry` — represents a single package within a license group. Fields: `name: String`, `version: String`, `purl: Option<String>` (package URL for precise identification).
- `LicenseGroup` — represents one license bucket. Fields: `license: String` (SPDX identifier), `packages: Vec<LicensePackageEntry>`, `compliant: bool` (whether this license passes the policy check).
- `LicenseReport` — top-level response. Fields: `sbom_id: String`, `groups: Vec<LicenseGroup>`, `generated_at: chrono::DateTime<chrono::Utc>` (timestamp of report generation), `policy_name: Option<String>` (name of the applied policy, if any).

Reference `modules/fundamental/src/package/model/summary.rs::PackageSummary` for the existing `license` field pattern on packages — the report model should use the same license identifier format.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field pattern; use the same SPDX identifier format in `LicenseGroup.license`
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — demonstrates the struct derivation and serialization pattern to follow

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `LicensePackageEntry` structs are defined in `modules/fundamental/src/sbom/model/license_report.rs`
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, and `Debug`
- [ ] The module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] The crate compiles without errors (`cargo check -p trustify-module-fundamental`)

## Test Requirements
- [ ] Verify the module compiles and structs can be instantiated in a unit test
- [ ] Verify `LicenseReport` serializes to the expected JSON structure: `{ "sbom_id": "...", "groups": [{ "license": "MIT", "packages": [...], "compliant": true }], "generated_at": "...", "policy_name": "..." }`

## Verification Commands
- `cargo check -p trustify-module-fundamental` — should compile without errors
