## Repository
trustify-backend

## Description
Define the Rust data structures for the SBOM comparison response. These model types represent each category of diff (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes) and a top-level `SbomComparison` struct that aggregates them. These models are consumed by the comparison service and serialized as the API response.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — Comparison response model structs: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod compare;` and re-export comparison types

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` — NEW: Response body uses the `SbomComparison` struct defined in this task

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Clone, Debug, Serialize, Deserialize, ToSchema` (for utoipa OpenAPI generation).
- The `SbomComparison` struct should contain six `Vec` fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`.
- `PackageDiff` should include fields: `name: String`, `version: String`, `license: String`, `advisory_count: u32`. Reuse field naming conventions from `PackageSummary` in `modules/fundamental/src/sbom/../package/model/summary.rs`.
- `VersionChange` should include: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: `"upgrade"` or `"downgrade"`).
- `VulnerabilityDiff` should include: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`. Severity values should match those used in `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs`.
- `LicenseChange` should include: `name: String`, `left_license: String`, `right_license: String`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — pattern reference for struct definition with serde and utoipa derives
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field conventions
- `modules/fundamental/src/sbom/../package/model/summary.rs::PackageSummary` — package field naming (name, version, license)

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff category fields
- [ ] All sub-structs (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined with correct fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`, `ToSchema`
- [ ] Types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without warnings

## Test Requirements
- [ ] `cargo check` passes for the `fundamental` module
- [ ] Structs can be serialized to JSON matching the expected API response shape from the Figma design spec

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
