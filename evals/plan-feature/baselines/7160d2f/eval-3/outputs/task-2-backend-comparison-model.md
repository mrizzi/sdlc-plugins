## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the response model types for the SBOM comparison endpoint. This defines the structured diff representation including added/removed packages, version changes, new/resolved vulnerabilities, and license changes. These types are consumed by the comparison service (Task 3) and endpoint (Task 4).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declaration for the new comparison model

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` structs with serde Serialize/Deserialize derives

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model struct derives `Serialize`, `Deserialize`, `Clone`, `Debug` and uses `serde` for field naming.

The `SbomComparison` struct should contain these fields:
- `added_packages: Vec<PackageDiff>` — packages in right SBOM not in left
- `removed_packages: Vec<PackageDiff>` — packages in left SBOM not in right
- `version_changes: Vec<VersionChange>` — packages present in both with different versions
- `new_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting right but not left
- `resolved_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting left but not right
- `license_changes: Vec<LicenseChange>` — packages whose license differs

Each `PackageDiff` should include: `name`, `version`, `license`, `advisory_count`.
Each `VersionChange` should include: `name`, `left_version`, `right_version`, `direction` (upgrade/downgrade).
Each `VulnerabilityDiff` should include: `advisory_id`, `severity`, `title`, `affected_package`.
Each `LicenseChange` should include: `name`, `left_license`, `right_license`.

Use `AppError` from `common/src/error.rs` for error handling in any conversion methods.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct demonstrating the project's model conventions (derives, field types, serde attributes)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — advisory model with severity field that the VulnerabilityDiff struct mirrors
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — package model with license field that the PackageDiff struct mirrors

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff category fields
- [ ] Supporting structs (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined with appropriate fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] Module is declared in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit tests for any conversion or helper methods on the comparison structs
- [ ] Verify serialization produces the expected JSON field names matching the API contract

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
