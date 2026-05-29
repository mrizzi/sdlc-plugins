## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison response model types that represent the structured diff between two SBOMs. These types define the response shape for the new comparison endpoint and include sub-structs for each diff category: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — comparison response model structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to expose the new module

## API Changes
- `GET /api/v2/sbom/compare` — NEW (model only): defines `SbomComparison` response struct with fields: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseChange>`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — derive `Serialize`, `Deserialize`, `Debug`, `Clone` on all structs, and use `utoipa::ToSchema` for OpenAPI generation.
- Define the following structs:
  - `SbomComparison` — top-level response containing vectors of each diff type
  - `PackageDiff` — fields: `name: String`, `version: String`, `license: String`, `advisory_count: u32`
  - `VersionChange` — fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade")
  - `VulnerabilityDiff` — fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
  - `LicenseChange` — fields: `name: String`, `left_license: String`, `right_license: String`
- The `VulnerabilityDiff` struct is used for both new and resolved vulnerabilities; the field name changes (`affected_package` vs `previously_affected_package`) are handled at serialization via `#[serde(rename)]` or at the service layer by populating the same struct.
- Reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` and `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for field naming conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow the same struct layout and derive macros
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference the severity field type and naming convention
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference the license field naming

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff category fields
- [ ] Each sub-struct (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) has the correct fields matching the API response shape
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and `ToSchema`
- [ ] The module is exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Verify that `SbomComparison` serializes to the expected JSON shape with `serde_json::to_value`
- [ ] Verify round-trip serialization/deserialization for each sub-struct

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256:7bf2f1c657bf08ba2739ba363a85416ad588b111893b9d4b54c6b8fb1667ac3d
