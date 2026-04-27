## Repository
trustify-backend

## Description
Add Rust data model structs for the SBOM comparison result. This includes the top-level `SbomComparisonResult` and sub-structs for each diff category: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — `SbomComparisonResult` struct containing vectors of `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, and `LicenseChange` sub-structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` and re-export comparison types

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct layout, derive macros (`Serialize`, `Deserialize`, `Debug`, `Clone`), and module re-export convention.
- Response shape must match the Figma-specified API contract:
  - `added_packages: Vec<AddedPackage>` with fields `name`, `version`, `license`, `advisory_count`
  - `removed_packages: Vec<RemovedPackage>` with fields `name`, `version`, `license`, `advisory_count`
  - `version_changes: Vec<VersionChange>` with fields `name`, `left_version`, `right_version`, `direction`
  - `new_vulnerabilities: Vec<NewVulnerability>` with fields `advisory_id`, `severity`, `title`, `affected_package`
  - `resolved_vulnerabilities: Vec<ResolvedVulnerability>` with fields `advisory_id`, `severity`, `title`, `previously_affected_package`
  - `license_changes: Vec<LicenseChange>` with fields `name`, `left_license`, `right_license`
- Reference `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` for severity field representation.
- Reference `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` and `entity/src/package.rs` for package-related field types.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — struct layout and derive macro pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field representation
- `entity/src/package.rs` — package entity fields

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct exists with all six diff category vectors
- [ ] Each sub-struct has the correct fields matching the API contract
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `SbomComparisonResult` serializes to expected JSON shape
- [ ] Unit test: deserialization from valid JSON produces correct field values
