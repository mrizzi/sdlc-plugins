## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the response model for the SBOM comparison endpoint. This model represents the structured diff result containing six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The model follows the existing module pattern used by `SbomSummary` and `SbomDetails`.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — register the new comparison model module

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — `SbomComparisonResult` struct and its sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` JSON response with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition, derive macros, and serialization attributes.
- Each sub-struct must derive `Serialize`, `Deserialize`, `Debug`, `Clone` at minimum.
- The `AddedPackage` and `RemovedPackage` sub-structs should include: `name: String`, `version: String`, `license: String`, `advisory_count: i64`.
- The `VersionChange` sub-struct should include: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade").
- The `NewVulnerability` and `ResolvedVulnerability` sub-structs should include advisory ID, severity, title, and affected/previously affected package name.
- The `LicenseChange` sub-struct should include: `name: String`, `left_license: String`, `right_license: String`.
- The `direction` field for version changes should be computed by comparing semver-parsed versions when possible, falling back to string comparison.
- Reuse field naming conventions from `PackageSummary` (which includes `license` field) and `AdvisorySummary` (which includes `severity` field).

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serialization patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — provides `license` field naming convention and type
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — provides `severity` field naming convention and type

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] All sub-structs are defined with the correct fields per the API response shape
- [ ] Structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Module is registered in `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Verify the structs compile and can be serialized to JSON matching the expected response shape
- [ ] Verify deserialization round-trip for each sub-struct

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
