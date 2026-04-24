# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Description
Define a `LicensePolicy` configuration model that represents the project's license compliance rules. The policy is loaded from a JSON configuration file at startup and specifies which licenses are allowed, denied, or flagged for review. This is the foundational data structure that the license report service (Task 2) will evaluate packages against.

## Files to Create
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct with `allowed_licenses`, `denied_licenses`, and `review_required_licenses` fields; includes deserialization from JSON and a `is_compliant(license: &str) -> bool` method
- `license-policy.json` — Default license policy configuration file at the repository root (or a `config/` directory) with a starter set of common compliant licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and a deny list

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `modules/fundamental/src/lib.rs` — Ensure the sbom model module is re-exported if needed

## Implementation Notes
- Follow the existing model pattern used by `SbomSummary` (`modules/fundamental/src/sbom/model/summary.rs`) and `SbomDetails` (`modules/fundamental/src/sbom/model/details.rs`) for struct definition style and derive macros
- Use `serde::Deserialize` for JSON config loading; the project already uses serde (SeaORM entities rely on it)
- The policy struct should implement `Default` so the service can fall back gracefully if no config file is provided
- The policy evaluation method should use case-insensitive SPDX license identifier matching
- Per constraints doc section 5.2: inspect existing model files before implementing to match patterns exactly
- Per constraints doc section 5.4: reuse existing error types from `common/src/error.rs` (`AppError`) for config loading failures

## Reuse Candidates
- `common/src/error.rs::AppError` — Use for error handling when the policy config file is missing or malformed
- `modules/fundamental/src/sbom/model/summary.rs` — Reference for struct definition patterns and derive macros

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `is_compliant()` correctly identifies allowed, denied, and review-required licenses
- [ ] A default policy is provided when no config file exists
- [ ] License matching is case-insensitive (e.g., "MIT" matches "mit")
- [ ] Default `license-policy.json` file contains reasonable starter values

## Test Requirements
- [ ] Unit test: deserialize a valid JSON policy string into `LicensePolicy`
- [ ] Unit test: `is_compliant` returns `true` for allowed licenses
- [ ] Unit test: `is_compliant` returns `false` for denied licenses
- [ ] Unit test: default policy is usable and non-empty
- [ ] Unit test: case-insensitive matching works correctly
