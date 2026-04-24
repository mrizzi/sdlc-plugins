## Repository
trustify-backend

## Description
Define the Rust data types that represent the SBOM comparison response. These structs form the contract between the comparison service and the REST endpoint, and their serialized form becomes the API response consumed by the frontend. This task establishes the data model before any business logic or endpoint code is written.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- Structs for the comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `VulnerabilityDiff`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod comparison;` and re-export the new types

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` -- NEW: Returns `SbomComparison` (this task defines the response type only; the endpoint handler is Task 3)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`: derive `Serialize`, `Deserialize`, `Clone`, `Debug` on all structs, and use `utoipa::ToSchema` for OpenAPI generation.
- The `SbomComparison` struct must contain six `Vec` fields matching the API response shape specified in the feature requirements:
  - `added_packages: Vec<AddedPackage>` -- fields: `name`, `version`, `license`, `advisory_count`
  - `removed_packages: Vec<RemovedPackage>` -- fields: `name`, `version`, `license`, `advisory_count`
  - `version_changes: Vec<VersionChange>` -- fields: `name`, `left_version`, `right_version`, `direction` (enum: `Upgrade`, `Downgrade`)
  - `new_vulnerabilities: Vec<VulnerabilityDiff>` -- fields: `advisory_id`, `severity`, `title`, `affected_package`
  - `resolved_vulnerabilities: Vec<ResolvedVulnerability>` -- fields: `advisory_id`, `severity`, `title`, `previously_affected_package`
  - `license_changes: Vec<LicenseChange>` -- fields: `name`, `left_license`, `right_license`
- Use `String` for most fields. Use a `Direction` enum with `#[serde(rename_all = "lowercase")]` for the upgrade/downgrade indicator.
- Reuse the severity representation from `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary` has a `severity` field) -- use the same type or a compatible string representation.
- All field names must use `snake_case` to match the JSON contract in the Figma design context.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- Pattern reference for struct layout, derive macros, and serde configuration
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Severity field type reference
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- License field type reference

## Acceptance Criteria
- [ ] `SbomComparison` struct exists with all six diff category fields
- [ ] All child structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `VulnerabilityDiff`, `ResolvedVulnerability`, `LicenseChange`) are defined with correct fields
- [ ] `Direction` enum exists with `Upgrade` and `Downgrade` variants, serialized as lowercase
- [ ] All types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] All types derive `Serialize`, `Deserialize`, `Clone`, `Debug`, `ToSchema`
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Verify `SbomComparison` serializes to JSON matching the expected API response shape (unit test with `serde_json::to_value`)
- [ ] Verify `Direction::Upgrade` serializes as `"upgrade"` and `Direction::Downgrade` as `"downgrade"`

## Verification Commands
- `cargo check -p trustify-fundamental` -- should compile without errors
- `cargo test -p trustify-fundamental comparison` -- should pass serialization tests
