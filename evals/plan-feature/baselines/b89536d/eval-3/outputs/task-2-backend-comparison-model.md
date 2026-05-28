# Task 2 — Add SBOM comparison diff model types

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust structs that represent the structured diff response for the SBOM comparison endpoint. These model types are consumed by the comparison service (Task 3) and serialized by the comparison endpoint (Task 4). The response shape must match the contract expected by the frontend.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison module

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparison` struct containing `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes` (this task defines the types; the endpoint is wired in Task 4)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize`, `Deserialize`, `Debug`, `Clone` and uses `serde` for JSON field naming.
- The `SbomComparison` struct fields must use snake_case names to match the expected JSON response shape:
  ```
  added_packages: Vec<AddedPackage>
  removed_packages: Vec<RemovedPackage>
  version_changes: Vec<VersionChange>
  new_vulnerabilities: Vec<NewVulnerability>
  resolved_vulnerabilities: Vec<ResolvedVulnerability>
  license_changes: Vec<LicenseChange>
  ```
- `AddedPackage` and `RemovedPackage` fields: `name: String`, `version: String`, `license: String`, `advisory_count: u32`
- `VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade")
- `NewVulnerability` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
- `ResolvedVulnerability` fields: `advisory_id: String`, `severity: String`, `title: String`, `previously_affected_package: String`
- `LicenseChange` fields: `name: String`, `left_license: String`, `right_license: String`
- Reference `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` for the `license` field pattern.
- Reference `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for the `severity` field pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct demonstrating the serde derive pattern and field conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing advisory model with severity field that the comparison vulnerability types should mirror
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package model with license field to reuse as reference

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff category fields
- [ ] All sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) are defined with correct fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Add unit tests in `modules/fundamental/src/sbom/model/comparison.rs` verifying serialization of `SbomComparison` to JSON matches the expected response shape
- [ ] Verify round-trip serde (serialize then deserialize) produces equal structs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
