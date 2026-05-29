# Task 2 — Add SBOM comparison diff model structs

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust structs for the SBOM comparison diff response. These model types represent the structured diff between two SBOMs, covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The models will be used by the comparison service (Task 3) and serialized as JSON by the comparison endpoint (Task 4).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — structs for the comparison response: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition style (derive macros, serde attributes, field naming).
- All structs must derive `Serialize`, `Deserialize`, `Clone`, `Debug` at minimum, matching sibling model structs.
- Use `snake_case` field names to match the expected JSON response shape from the Figma design context:
  - `SbomComparisonResult` fields: `added_packages: Vec<AddedPackage>`, `removed_packages: Vec<RemovedPackage>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<NewVulnerability>`, `resolved_vulnerabilities: Vec<ResolvedVulnerability>`, `license_changes: Vec<LicenseChange>`
  - `AddedPackage` / `RemovedPackage`: `name: String`, `version: String`, `license: String`, `advisory_count: u32`
  - `VersionChange`: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade")
  - `NewVulnerability`: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
  - `ResolvedVulnerability`: `advisory_id: String`, `severity: String`, `title: String`, `previously_affected_package: String`
  - `LicenseChange`: `name: String`, `left_license: String`, `right_license: String`

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — example of struct definition conventions with serde derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — example of a complex model struct in the same module
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes `severity` field pattern that maps to `NewVulnerability.severity`
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes `license` field pattern that maps to package license fields

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct exists with six `Vec` fields for each diff category
- [ ] All six sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) are defined with fields matching the API response shape
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] Module is properly re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify struct serialization produces the expected JSON field names (snake_case)
- [ ] Verify deserialization round-trip works for all structs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256:47ed1003e7b5d7523d2336170d40779ce8c792792eb6753ff5fa516da972da67
