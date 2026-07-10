## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration module that loads a JSON policy file defining which
licenses are compliant and which are not. The policy file lists denied licenses (or
alternatively, a list of allowed licenses). This configuration drives the compliance
flags in the license report. The policy is stored as a JSON config file in the repository
and loaded at service initialization.

## Files to Create
- `common/src/model/license_policy.rs` — define `LicensePolicy` struct and loader function that reads and parses the JSON policy file
- `license-policy.json` — default license policy configuration file at the repository root (example with common permissive/copyleft classifications)

## Files to Modify
- `common/src/model/mod.rs` — add `pub mod license_policy;` and re-export the new types
- `common/Cargo.toml` — add `serde_json` dependency if not already present

## Implementation Notes
The `LicensePolicy` struct should support a configurable deny-list model:
- `denied_licenses: Vec<String>` — SPDX identifiers of licenses that are non-compliant
- A method `is_compliant(&self, license: &str) -> bool` that returns `false` if the license
  appears in the denied list

Follow the existing model pattern in `common/src/model/paginated.rs` for struct definition
conventions in the common crate.

The default `license-policy.json` should include a reasonable set of commonly denied
copyleft licenses (e.g., `GPL-3.0-only`, `AGPL-3.0-only`) while allowing permissive
licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause).

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` from the policy loader
with `.context()` wrapping for file I/O errors.
Applies: task creates `common/src/model/license_policy.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — demonstrates the struct definition and derive pattern used in the common crate
- `common/src/error.rs::AppError` — the error type to use for policy loading failures; reuse the existing error variants for I/O and parsing errors

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with a `denied_licenses` field
- [ ] `is_compliant()` method correctly identifies denied vs. allowed licenses
- [ ] Policy loader reads and parses a JSON file into `LicensePolicy`
- [ ] Policy loader returns `AppError` on file-not-found or parse errors
- [ ] Default `license-policy.json` exists at the repository root with a reasonable initial policy
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Unit test verifying `is_compliant()` returns `true` for a license not in the denied list
- [ ] Unit test verifying `is_compliant()` returns `false` for a denied license
- [ ] Unit test verifying policy loader parses a valid JSON policy file
- [ ] Unit test verifying policy loader returns an error for malformed JSON
- [ ] Unit test verifying case-sensitive license matching (SPDX identifiers are case-sensitive)

## Verification Commands
- `cargo check -p trustify-common` — compiles without errors
- `cargo test -p trustify-common -- license_policy` — all policy tests pass
