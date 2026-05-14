# Task 1: Define SBOM comparison response model

## Repository
trustify-backend

## Target Branch
main

## Description
Define the Rust data structures for the SBOM comparison response. These structs represent the structured diff between two SBOMs and are serialized as JSON by the comparison endpoint. This task establishes the response contract that the frontend will consume.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — Comparison response structs: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod compare;` declaration and re-export the comparison types

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` — derive `Serialize`, `Deserialize`, `Clone`, `Debug` on all structs.
- The `SbomComparison` struct should contain six fields matching the API contract:
  - `added_packages: Vec<PackageDiff>` — packages in right SBOM but not left
  - `removed_packages: Vec<PackageDiff>` — packages in left SBOM but not right
  - `version_changes: Vec<VersionChange>` — packages in both with different versions
  - `new_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting right but not left
  - `resolved_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting left but not right
  - `license_changes: Vec<LicenseChange>` — packages whose license differs
- `PackageDiff` fields: `name: String`, `version: String`, `license: Option<String>`, `advisory_count: u32`
- `VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: VersionDirection` (enum: `Upgrade`, `Downgrade`, `Unknown`)
- `VulnerabilityDiff` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
- `LicenseChange` fields: `name: String`, `left_license: String`, `right_license: String`
- Use `serde(rename_all = "snake_case")` on enums for JSON serialization consistency.
- Reference the `PackageSummary` struct in `modules/fundamental/src/sbom/../package/model/summary.rs` and `AdvisorySummary` in `modules/fundamental/src/sbom/../advisory/model/summary.rs` for field naming conventions (e.g., `license`, `severity`).

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff category fields
- [ ] All supporting structs (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined
- [ ] `VersionDirection` enum is defined with `Upgrade`, `Downgrade`, `Unknown` variants
- [ ] All types derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] Types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Add a unit test in `compare.rs` verifying that `SbomComparison` serializes to the expected JSON structure (matching the contract in the feature spec)
- [ ] Add a test verifying `VersionDirection` serializes as snake_case strings (`"upgrade"`, `"downgrade"`, `"unknown"`)

## Dependencies
- None — this is the first task
