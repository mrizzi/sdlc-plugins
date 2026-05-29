# Task 2 — Add SBOM comparison diff model structs

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the data model structs for the SBOM comparison diff result. These structs represent the response shape of the comparison endpoint and are used by both the service layer and the endpoint handler. The diff is computed on-the-fly from existing package and advisory data — no new database tables are required.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison result: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`.
- The `SbomComparisonResult` struct fields must match the API response shape defined in the feature requirements:
  - `added_packages: Vec<AddedPackage>` — fields: `name`, `version`, `license`, `advisory_count`
  - `removed_packages: Vec<RemovedPackage>` — fields: `name`, `version`, `license`, `advisory_count`
  - `version_changes: Vec<VersionChange>` — fields: `name`, `left_version`, `right_version`, `direction` (upgrade/downgrade)
  - `new_vulnerabilities: Vec<NewVulnerability>` — fields: `advisory_id`, `severity`, `title`, `affected_package`
  - `resolved_vulnerabilities: Vec<ResolvedVulnerability>` — fields: `advisory_id`, `severity`, `title`, `previously_affected_package`
  - `license_changes: Vec<LicenseChange>` — fields: `name`, `left_license`, `right_license`
- The `direction` field in `VersionChange` should be a string enum (`"upgrade"` or `"downgrade"`).
- The `severity` field in vulnerability structs should match the severity field type used in `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`).

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct pattern to follow for derive macros and field conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field type to reuse for vulnerability severity representation
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the license field type to reference for package license representation

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] All sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) are defined with correct fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] The comparison module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Verify that all comparison model structs can be serialized to JSON and deserialized back (round-trip test)
- [ ] Verify that the JSON output field names match the expected API response shape (snake_case)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
