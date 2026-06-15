## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model structs for the license compliance report. The report groups packages by license and includes a compliance flag per group based on the license policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Define the following structs:
  - `LicenseReport` — Top-level response containing `sbom_id: String`, `groups: Vec<LicenseGroup>`, `summary: ReportSummary`
  - `LicenseGroup` — Represents one license grouping: `license: String`, `packages: Vec<PackageRef>`, `compliant: bool`, `disposition: String` (approved/denied/review)
  - `PackageRef` — Minimal package reference: `id: String`, `name: String`, `version: String`, `is_transitive: bool`
  - `ReportSummary` — Aggregate stats: `total_packages: u32`, `total_licenses: u32`, `compliant_count: u32`, `non_compliant_count: u32`, `review_count: u32`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` and re-export the key types

## Implementation Notes
- All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug` consistent with existing model structs like `SbomSummary` and `SbomDetails` in the same directory
- Use `utoipa::ToSchema` derive macro if the project uses it for OpenAPI spec generation (check existing model files for the pattern)
- The response shape matches the requirement: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }` with the addition of a summary for convenience

Per CONVENTIONS.md: Follow the existing module pattern where each domain module has `model/ + service/ + endpoints/` structure. Applies: task creates a new model file under `modules/fundamental/src/sbom/model/`.

## Acceptance Criteria
- `LicenseReport`, `LicenseGroup`, `PackageRef`, and `ReportSummary` structs compile and serialize to the expected JSON shape
- JSON output matches the documented response format from the feature requirements
- Structs are publicly exported from the sbom model module

## Test Requirements
- Unit tests in `modules/fundamental/src/sbom/model/license_report.rs` (inline `#[cfg(test)]` module)
- Test serialization of a `LicenseReport` with multiple groups to verify JSON shape
- Test that an empty report (no packages) serializes correctly

## Dependencies
- Depends on: None (can be developed in parallel with Task 1)

[sdlc-workflow] Description digest: sha256-md:f9b83816f3c997aebb603a8353e0acf50f864b74d8c81a4550b9560cde515a2b
