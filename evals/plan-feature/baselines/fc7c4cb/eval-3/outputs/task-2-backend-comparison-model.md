## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the model types for the SBOM comparison diff result. These types represent the structured output of comparing two SBOMs: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The models will be consumed by the comparison service and serialized as the API response.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`.
- The `SbomComparisonResult` struct should contain six fields: `added_packages: Vec<AddedPackage>`, `removed_packages: Vec<RemovedPackage>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<NewVulnerability>`, `resolved_vulnerabilities: Vec<ResolvedVulnerability>`, `license_changes: Vec<LicenseChange>`.
- `AddedPackage` and `RemovedPackage` fields: `name: String`, `version: String`, `license: String`, `advisory_count: u32`.
- `VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade").
- `NewVulnerability` and `ResolvedVulnerability` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String` (for new) / `previously_affected_package: String` (for resolved).
- `LicenseChange` fields: `name: String`, `left_license: String`, `right_license: String`.
- Reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` for field naming conventions (uses `license` field).
- Reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` for severity field patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the standard struct derivation pattern and serialization approach used across model types
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains `license` field pattern to reuse for package-related comparison structs
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains `severity` field pattern to reuse for vulnerability comparison structs

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] All sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) are defined with correct fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] The comparison module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit tests verifying that `SbomComparisonResult` can be serialized to JSON and deserialized back, producing the expected JSON structure matching the API response shape from the feature specification
- [ ] Unit test verifying that an empty comparison result (all empty vectors) serializes correctly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256:15f385a2f4aa536a06d21b363451a11db296c20fce4bdd1b8eb61ac10d313366
