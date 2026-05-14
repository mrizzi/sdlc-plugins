## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model structs for the SBOM comparison diff result. These structs define the response shape for the comparison endpoint and represent the structured diff between two SBOMs: added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseDiff`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`.
- Define the following structs:
  - `SbomComparisonResult` with fields: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseDiff>`
  - `PackageDiff` with fields: `name: String`, `version: String`, `license: Option<String>`, `advisory_count: u32`
  - `VersionChange` with fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade")
  - `VulnerabilityDiff` with fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
  - `LicenseDiff` with fields: `name: String`, `left_license: String`, `right_license: String`
- Use `serde(rename_all = "snake_case")` on all structs to ensure JSON field names match the expected API response format from the Figma design context.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct derive macros and serialization patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for the severity field type and serialization
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference for the license field type

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, and `LicenseDiff` structs are defined with all fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] The comparison module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] The project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Unit test verifying `SbomComparisonResult` serializes to the expected JSON shape matching the API contract from the Figma design context
- [ ] Unit test verifying `VersionChange` direction field accepts "upgrade" and "downgrade" values

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
