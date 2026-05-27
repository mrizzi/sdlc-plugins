# Task 2 — Add SBOM comparison response model

**Summary:** Add SBOM comparison response model structs

**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the data model structs for the SBOM comparison response. This includes the top-level `SbomComparisonResult` struct and its sub-structs for each diff category: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. These structs will be used by the comparison service logic and serialized as the API response.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — comparison result structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize`, `Deserialize`, `Clone`, `Debug` and uses serde rename attributes where needed.
- The `SbomComparisonResult` struct must include these fields matching the API contract from the feature requirements:
  - `added_packages: Vec<AddedPackage>` — fields: name, version, license, advisory_count
  - `removed_packages: Vec<RemovedPackage>` — fields: name, version, license, advisory_count
  - `version_changes: Vec<VersionChange>` — fields: name, left_version, right_version, direction (upgrade/downgrade)
  - `new_vulnerabilities: Vec<NewVulnerability>` — fields: advisory_id, severity, title, affected_package
  - `resolved_vulnerabilities: Vec<ResolvedVulnerability>` — fields: advisory_id, severity, title, previously_affected_package
  - `license_changes: Vec<LicenseChange>` — fields: name, left_license, right_license
- Use `String` for text fields and consider using an enum for the `direction` field (Upgrade/Downgrade) and for the `severity` field if an existing severity enum is available.
- Per the feature's non-functional requirements: no new database tables — these are pure response structs, not SeaORM entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct derivation patterns and serde attributes
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — reference for struct organization
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains severity field pattern to reuse
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains license field pattern to reuse

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category vectors
- [ ] All sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) are defined with correct fields
- [ ] All structs derive Serialize and Deserialize for JSON serialization
- [ ] Module is exported via `model/mod.rs`

## Test Requirements
- [ ] Verify that SbomComparisonResult can be serialized to JSON matching the expected API response shape from the feature spec
- [ ] Verify deserialization round-trip for all struct types

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
