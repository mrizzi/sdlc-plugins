## Repository
trustify-backend

## Target Branch
main

## Description
Add the model types and license policy configuration needed for the license compliance report feature. This task creates the data structures that represent the license report response (packages grouped by license type with compliance flags) and a policy configuration loader that reads a JSON policy file defining which licenses are compliant.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReportSummary and LicenseGroup structs with Serialize derives for JSON response
- `common/src/model/license_policy.rs` — LicensePolicy struct and policy loader that reads a JSON config file listing allowed/denied license identifiers

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` to re-export the new module
- `common/src/model/mod.rs` — add `pub mod license_policy;` to re-export the policy module

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW (models only; endpoint wired in Task 2): response shape `{ groups: [{ license: String, packages: [PackageSummary], compliant: bool }] }`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct layout and derive macros.
- The `LicenseReportSummary` struct should contain a `groups` field of type `Vec<LicenseGroup>`.
- The `LicenseGroup` struct should contain: `license: String`, `packages: Vec<PackageSummary>`, `compliant: bool`.
- Reuse the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` — do not create a duplicate package representation.
- The `LicensePolicy` struct should hold two sets of SPDX license identifiers: `allowed` (allowlist) and `denied` (denylist). A license is compliant if it appears in the allowed set, or if it does not appear in the denied set when no allowed set is defined.
- The policy loader should read from a configurable file path (defaulting to `license-policy.json` in the working directory). Use `serde_json::from_reader` for deserialization.
- Per CONVENTIONS.md Key Conventions (Module pattern): follow the `model/ + service/ + endpoints/` directory structure by placing model types under `model/`.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's module pattern scope.
- Per CONVENTIONS.md Key Conventions (Framework): use serde derives for Axum JSON serialization.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serialization patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing struct with license field; reuse directly in LicenseGroup instead of duplicating
- `common/src/model/paginated.rs::PaginatedResults` — reference for response wrapper pattern (though the report uses a different shape)

## Acceptance Criteria
- [ ] `LicenseReportSummary` and `LicenseGroup` structs are defined with correct field types and Serialize derives
- [ ] `LicensePolicy` struct can be deserialized from a JSON config file
- [ ] Policy loader handles missing config file gracefully (returns a default permissive policy)
- [ ] All new types are re-exported through their respective module `mod.rs` files
- [ ] No new database tables or entities are introduced

## Test Requirements
- [ ] Unit test: LicensePolicy deserialization from valid JSON produces correct allowed/denied sets
- [ ] Unit test: LicensePolicy deserialization from empty/missing file returns default permissive policy
- [ ] Unit test: LicenseGroup serialization produces expected JSON shape matching the API contract

## Dependencies
- None
