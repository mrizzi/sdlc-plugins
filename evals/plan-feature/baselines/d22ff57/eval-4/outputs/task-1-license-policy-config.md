# Task 1 — Add license policy configuration and report models

## Repository
trustify-backend

## Description
Add the license policy configuration model and the license report response models needed for the compliance report feature. The license policy is a JSON configuration file stored in the repository that defines which licenses are allowed, denied, or flagged for review. The report models define the API response shape: packages grouped by license type with compliance flags evaluated against the policy.

This task establishes the foundational data structures that the service layer (Task 2) and endpoint (Task 3) will build upon.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseGroup` and `LicenseReport` structs for the API response. `LicenseGroup` contains: `license: String`, `packages: Vec<PackageSummary>`, `compliant: bool`. `LicenseReport` contains: `groups: Vec<LicenseGroup>`.
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct and loader. Fields: `allowed: Vec<String>` (SPDX identifiers), `denied: Vec<String>`, `default_policy: PolicyAction` (enum: Allow, Deny, Review). Includes a `load_from_file(path: &Path) -> Result<LicensePolicy, AppError>` function.
- `license-policy.json` — Default license policy configuration file at the repository root. Contains a sensible default policy with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and known copyleft licenses (GPL-3.0, AGPL-3.0) as denied.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` and `pub mod license_policy;` declarations to expose the new modules.

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition style, derive macros, and serialization attributes.
- Reuse the `PackageSummary` struct from `modules/fundamental/src/sbom/model/../../../package/model/summary.rs` for the packages field in `LicenseGroup` — do not create a new package representation.
- Error handling: use `AppError` from `common/src/error.rs` with `.context()` wrapping, consistent with the existing codebase pattern.
- The `LicensePolicy` struct should implement `serde::Deserialize` for loading from JSON and `Clone` for sharing across requests.
- Per constraints doc section 5, code must not duplicate existing functionality. The `PackageSummary` struct already includes a `license` field — reuse it.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing struct that already contains a `license` field; reuse as the package representation in `LicenseGroup`.
- `common/src/error.rs::AppError` — shared error type for consistent error handling.

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file with allowed/denied license lists and a default policy action
- [ ] `LicenseReport` and `LicenseGroup` structs are defined with proper serialization derives for JSON API responses
- [ ] `license-policy.json` exists at the repo root with a sensible default configuration
- [ ] `LicensePolicy::load_from_file` returns an appropriate `AppError` when the file is missing or malformed
- [ ] All new modules are properly exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: deserialize a valid `LicensePolicy` JSON and verify all fields are populated correctly
- [ ] Unit test: deserialize a `LicensePolicy` with only `allowed` list (no `denied`) succeeds
- [ ] Unit test: `load_from_file` with a nonexistent path returns an error
- [ ] Unit test: `load_from_file` with malformed JSON returns an error
- [ ] Unit test: `LicenseReport` serializes to the expected JSON structure `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
