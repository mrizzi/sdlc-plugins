## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model structs for the license compliance report feature. This includes the response types for the license report endpoint: `LicenseGroup` (representing a group of packages sharing a license, with a compliance flag) and `LicenseReport` (the top-level report containing a list of license groups). Also add a `LicensePolicy` struct for loading and evaluating the configurable license policy from a JSON file.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declarations for the new license report model files

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseGroup` and `LicenseReport` structs with serde Serialize/Deserialize derives
- `modules/fundamental/src/sbom/model/license_policy.rs` — define `LicensePolicy` struct that loads allowed/denied license lists from a JSON config file

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — these use struct definitions with serde derives and are re-exported from the module's `mod.rs`.
- The `LicenseReport` struct should contain a `groups` field of type `Vec<LicenseGroup>`.
- Each `LicenseGroup` should contain: `license: String`, `packages: Vec<PackageSummary>`, `compliant: bool`.
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which already includes a `license` field — reuse this type rather than creating a new package representation.
- The `LicensePolicy` struct should support loading from a JSON config file with fields for `allowed_licenses: Vec<String>` and `denied_licenses: Vec<String>`.
- Per CONVENTIONS.md: follow the existing module pattern for model definitions. All new structs should use `#[derive(Clone, Debug, Serialize, Deserialize)]`.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust model file scope.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package summary struct that includes the `license` field; reuse for packages within license groups
- `common/src/model/paginated.rs::PaginatedResults` — existing response wrapper pattern to follow for consistent API responses
- `common/src/error.rs::AppError` — existing error handling enum for policy loading errors

## Acceptance Criteria
- [ ] `LicenseGroup` struct defined with `license`, `packages`, and `compliant` fields
- [ ] `LicenseReport` struct defined with `groups` field containing `Vec<LicenseGroup>`
- [ ] `LicensePolicy` struct defined with `allowed_licenses` and `denied_licenses` fields
- [ ] `LicensePolicy` includes a method to evaluate whether a given license string is compliant
- [ ] All structs derive `Serialize` and `Deserialize`
- [ ] New model files are properly declared in `mod.rs`

## Test Requirements
- [ ] Unit test for `LicensePolicy` compliance evaluation — allowed license returns compliant
- [ ] Unit test for `LicensePolicy` compliance evaluation — denied license returns non-compliant
- [ ] Unit test for `LicensePolicy` with empty policy (no restrictions) — all licenses compliant
- [ ] Unit test for `LicenseReport` serialization to JSON matches expected format

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- license` — all license-related unit tests pass

## Dependencies
- None
