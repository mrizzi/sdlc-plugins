## Repository
trustify-backend

## Description
Define the data model structs for the SBOM comparison response. These structs represent the structured diff between two SBOMs, covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. This model forms the API contract that the frontend will consume.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison response: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize, Deserialize, Debug, Clone` and uses `utoipa::ToSchema` for OpenAPI generation.
- The `SbomComparison` struct should have six fields matching the API contract: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseChange>`.
- `PackageDiff` fields: `name: String`, `version: String`, `license: String`, `advisory_count: u32`.
- `VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade").
- `VulnerabilityDiff` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`.
- `LicenseChange` fields: `name: String`, `left_license: String`, `right_license: String`.
- Reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` for the `license` field pattern and `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for the `severity` field pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — pattern for struct derivation and serde attributes
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field representation

## Acceptance Criteria
- [ ] `SbomComparison` struct exists with all six diff category fields
- [ ] All sub-structs (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined with correct fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and `ToSchema`
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles with `cargo check -p trustify-module-fundamental`

## Test Requirements
- [ ] Unit test that `SbomComparison` can be serialized to JSON matching the expected API response shape
- [ ] Unit test that `SbomComparison` can be deserialized from a JSON string with all six sections populated
- [ ] Unit test that an empty comparison (all empty vectors) serializes correctly

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental comparison` — model tests pass

## Dependencies
- None
