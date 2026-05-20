# Task 2 — Add SBOM comparison diff model structs

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust structs that represent the structured diff result returned by the SBOM comparison endpoint. These models capture the six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Response body uses `SbomComparisonResult` (this task defines the types; the endpoint is wired in Task 4)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — derive `Serialize`, `Deserialize`, `Debug`, `Clone` on all structs
- Use `utoipa::ToSchema` derive for OpenAPI schema generation, consistent with existing model structs
- The `SbomComparisonResult` struct must match the response shape specified in the feature requirements:
  ```
  {
    "added_packages": [{ "name", "version", "license", "advisory_count" }],
    "removed_packages": [{ "name", "version", "license", "advisory_count" }],
    "version_changes": [{ "name", "left_version", "right_version", "direction" }],
    "new_vulnerabilities": [{ "advisory_id", "severity", "title", "affected_package" }],
    "resolved_vulnerabilities": [{ "advisory_id", "severity", "title", "previously_affected_package" }],
    "license_changes": [{ "name", "left_license", "right_license" }]
  }
  ```
- The `direction` field in `VersionChange` should be an enum with variants `Upgrade` and `Downgrade`, serialized as lowercase strings
- The `severity` field in `VulnerabilityDiff` should reuse the severity type from `modules/fundamental/src/advisory/model/summary.rs` (check `AdvisorySummary` for the existing severity field type)

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow its derive macros and serialization patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reuse or reference the severity type for vulnerability diff entries
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference for package-related field naming (name, version, license)

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct defined with all six diff category fields
- [ ] `PackageDiff` struct defined with name, version, license, advisory_count fields
- [ ] `VersionChange` struct defined with name, left_version, right_version, direction fields
- [ ] `VulnerabilityDiff` struct defined with advisory_id, severity, title, affected_package/previously_affected_package fields
- [ ] `LicenseChange` struct defined with name, left_license, right_license fields
- [ ] All structs derive Serialize, Deserialize, Debug, Clone, and ToSchema
- [ ] Module is re-exported from `sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit tests for serialization: verify `SbomComparisonResult` serializes to the expected JSON shape
- [ ] Unit test for `VersionChange` direction enum serialization (upgrade/downgrade as lowercase strings)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
