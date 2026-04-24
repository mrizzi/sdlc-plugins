# Task 1 — Add license policy configuration model and default policy file

## Repository
trustify-backend

## Description
Define the license policy data model that drives compliance evaluation. The policy specifies which licenses are allowed, denied, or flagged for review. It is loaded from a JSON configuration file at startup. This task also creates a default `license-policy.json` file with a starter set of common OSS license classifications (e.g., MIT and Apache-2.0 as allowed, GPL-3.0 as denied).

## Files to Create
- `common/src/model/license_policy.rs` — `LicensePolicy` struct with `allowed`, `denied`, and `review` license ID lists, plus `load_from_file()` deserialization method
- `license-policy.json` — Default policy configuration file at the repository root with starter license classifications

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add `serde_json` dependency if not already present (for JSON deserialization)

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` — see `paginated.rs` for the established struct + derive pattern
- Use `serde::Deserialize` for JSON loading, consistent with the rest of the codebase
- The `LicensePolicy` struct should contain:
  - `allowed: Vec<String>` — SPDX license identifiers that are compliant
  - `denied: Vec<String>` — SPDX license identifiers that are non-compliant
  - `review: Option<Vec<String>>` — licenses requiring manual review (optional field)
- Implement a `LicensePolicy::load(path: &Path) -> Result<Self, AppError>` method using `std::fs::read_to_string` + `serde_json::from_str`, wrapping errors with `.context()` per the error handling pattern in `common/src/error.rs`
- Implement `LicensePolicy::is_compliant(&self, license_id: &str) -> bool` — returns `true` if the license is in `allowed` or not in `denied`
- The default `license-policy.json` should use SPDX identifiers (e.g., `MIT`, `Apache-2.0`, `BSD-2-Clause`, `GPL-3.0-only`)

## Reuse Candidates
- `common/src/error.rs::AppError` — use for error handling with `.context()` wrapping
- `common/src/model/paginated.rs` — reference for struct definition patterns and derive macros

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a valid JSON config file
- [ ] `LicensePolicy::is_compliant()` correctly classifies allowed, denied, and unknown licenses
- [ ] A default `license-policy.json` file exists with reasonable starter classifications
- [ ] Invalid or missing config file produces a clear `AppError` with context

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON string into `LicensePolicy`
- [ ] Unit test: `is_compliant` returns `true` for allowed licenses
- [ ] Unit test: `is_compliant` returns `false` for denied licenses
- [ ] Unit test: `is_compliant` handles licenses not in either list (default behavior)
- [ ] Unit test: loading a nonexistent file returns an appropriate error

## Documentation Updates
- `README.md` — Add section documenting the license policy configuration file format and location
