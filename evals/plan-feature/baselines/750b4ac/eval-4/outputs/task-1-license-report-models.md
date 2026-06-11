## Repository
trustify-backend

## Target Branch
main

## Description
Add model structs for the license compliance report feature. This includes the license policy configuration model (for loading and validating the configurable compliance policy), the license group model (for grouping packages by license type), and the license report response model (the top-level report structure returned by the endpoint). These models provide the data foundation for the license report service and endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport, LicenseGroup, and PackageLicenseEntry response structs
- `modules/fundamental/src/sbom/model/license_policy.rs` — LicensePolicy and PolicyRule structs for loading compliance policy from JSON config

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` and `pub mod license_policy;` declarations

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition, serialization derives, and module organization.
- The LicenseReport struct should contain a `groups` field of type `Vec<LicenseGroup>` where each group has: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`.
- The LicensePolicy struct should deserialize from a JSON configuration file and contain a list of allowed/denied license identifiers following the SPDX license list convention.
- Use `serde::Deserialize` and `serde::Serialize` derives consistent with existing model structs.
- The PackageLicenseEntry should reference the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` to reuse the package representation that already includes a `license` field.
- Per constraints (Section 5, Code Change Rules): follow the patterns referenced in Implementation Notes and reuse existing types rather than duplicating functionality.
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — example of a model struct with serde derives and field patterns to follow
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — example of a detailed response model struct
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package model with `license` field; reuse in PackageLicenseEntry rather than duplicating

## Acceptance Criteria
- [ ] LicenseReport, LicenseGroup, and PackageLicenseEntry structs are defined with appropriate serde derives
- [ ] LicensePolicy and PolicyRule structs are defined and can deserialize from JSON
- [ ] All new structs are publicly exported from the sbom model module
- [ ] The PackageLicenseEntry references or wraps the existing PackageSummary type

## Test Requirements
- [ ] Unit test: LicensePolicy deserializes correctly from a valid JSON policy string
- [ ] Unit test: LicensePolicy deserialization fails gracefully with invalid JSON input
- [ ] Unit test: LicenseReport serializes to the expected JSON structure with groups, packages, and compliance flags

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:94e7c44522ceb12736a50b755529239a0addf9ca6f385ef2809fc373482cdc2f
