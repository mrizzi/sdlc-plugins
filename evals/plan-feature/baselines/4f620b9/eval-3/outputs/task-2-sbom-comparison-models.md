## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the Rust model types for the SBOM comparison diff result. These types represent the structured output of comparing two SBOMs: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The models are consumed by the comparison service (Task 3) and serialized by the comparison endpoint (Task 4).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Diff result structs: SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — derive `Serialize`, `Deserialize`, `Clone`, `Debug` on all structs.
- `SbomComparisonResult` should contain fields: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseChange>`.
- `PackageDiff` fields: `name: String`, `version: String`, `license: String`, `advisory_count: i64`.
- `VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade").
- `VulnerabilityDiff` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`.
- `LicenseChange` fields: `name: String`, `left_license: String`, `right_license: String`.
- Reuse the serialization conventions from `PackageSummary` in `modules/fundamental/src/sbom/../package/model/summary.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follows the same derive pattern and serialization conventions to use as a template
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes severity field pattern to reuse for VulnerabilityDiff
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field pattern to reuse for PackageDiff

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] All sub-structs (`PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined with correct fields
- [ ] All types derive `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit tests verify that `SbomComparisonResult` serializes to the expected JSON shape matching the API contract
- [ ] Unit tests verify deserialization round-trip for each sub-struct

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256-md:02a27baa6f031615ad1d40f2332c537e0ef078fbd836427c52633a28d3ab4bf2
