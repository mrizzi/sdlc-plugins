## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model and loader that reads a JSON config file defining allowed and denied license types. This provides the configurable compliance policy that the license report endpoint will use to flag non-compliant packages. The policy file uses SPDX license identifiers and supports both an allowlist and a denylist approach.

## Files to Create
- `common/src/license_policy.rs` — License policy struct and JSON deserialization logic, including policy loading from a configurable file path
- `license-policy.json` — Default license policy configuration file at the repository root with example allowed/denied licenses

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add `serde_json` dependency if not already present for JSON config parsing

## Implementation Notes
- Follow the existing module pattern in `common/src/` where shared utilities are defined (see `common/src/db/mod.rs` and `common/src/error.rs` for examples of shared modules).
- The policy struct should use `serde::Deserialize` for JSON parsing, consistent with how SeaORM entities use serde throughout the project.
- Define a `LicensePolicy` struct with fields: `allowed_licenses: Option<Vec<String>>`, `denied_licenses: Option<Vec<String>>`, and a method `is_compliant(license: &str) -> bool` that checks a given SPDX license identifier against the policy rules.
- When both allowed and denied lists are present, denied takes precedence (a license on both lists is non-compliant).
- The policy loader should accept a file path and return `Result<LicensePolicy, AppError>`, following the error handling pattern in `common/src/error.rs` where all errors use the `AppError` enum with `.context()` wrapping.
- Per CONVENTIONS.md §Error Handling: all public functions return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `common/src/lib.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — Error enum used throughout the project; reuse for policy loading errors instead of creating a new error type

## Acceptance Criteria
- [ ] A `LicensePolicy` struct exists that can be deserialized from a JSON configuration file
- [ ] The policy supports both allowed and denied license lists using SPDX identifiers
- [ ] A `is_compliant(license: &str) -> bool` method correctly evaluates licenses against the policy
- [ ] When both allowed and denied lists are present, denied takes precedence
- [ ] A default `license-policy.json` file exists at the repository root with example configuration
- [ ] Policy loading errors are wrapped in `AppError` with descriptive context

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON with both allowed and denied lists
- [ ] Unit test: `is_compliant` returns true for an allowed license not on the denied list
- [ ] Unit test: `is_compliant` returns false for a denied license
- [ ] Unit test: `is_compliant` returns false for a license on both allowed and denied lists (denied takes precedence)
- [ ] Unit test: `is_compliant` returns true for any license when no policy restrictions are configured (empty/null lists)
- [ ] Unit test: policy loading returns an error with context for an invalid JSON file

## Verification Commands
- `cargo test --package common` — all unit tests pass
- `cargo build --package common` — compiles without errors
