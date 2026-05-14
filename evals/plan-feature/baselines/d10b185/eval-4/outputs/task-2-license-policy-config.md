# Task 2 — Add license policy configuration file and loader

## Repository
trustify-backend

## Target Branch
main

## Description
Add a default license policy JSON configuration file and a loader function that reads and deserializes the policy at service initialization. The policy file defines which SPDX licenses are allowed or denied, and a default disposition for unlisted licenses. This enables organizations to customize their compliance rules.

## Files to Create
- `config/license-policy.json` — default license policy configuration with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and common copyleft licenses (GPL-2.0-only, GPL-3.0-only, AGPL-3.0-only) as denied, with a default of Deny
- `modules/fundamental/src/sbom/service/license_policy_loader.rs` — function to load and parse the policy JSON file, returning a `LicensePolicy` struct

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add module declaration for `license_policy_loader`

## Implementation Notes
- Follow the service module pattern from `modules/fundamental/src/sbom/service/mod.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for module organization.
- The loader function should accept a file path parameter (with a sensible default) so the policy file location is configurable.
- Use `serde_json::from_reader` for deserialization, returning `Result<LicensePolicy, AppError>` using the error type from `common/src/error.rs`.
- Wrap errors with `.context()` per the project's error handling convention (all handlers return `Result<T, AppError>` with `.context()` wrapping as noted in repo conventions).
- Per constraints doc section 5.3: implementation must follow the patterns referenced in these notes.
- Per constraints doc section 5.4: do not duplicate existing deserialization utilities — check `common/src/` for any existing config loading helpers before writing new ones.

## Reuse Candidates
- `common/src/error.rs::AppError` — the standard error type; use for all error returns from the loader
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service module pattern and error handling conventions

## Acceptance Criteria
- [ ] `config/license-policy.json` exists with a valid default policy covering common SPDX licenses
- [ ] Loader function reads and deserializes the JSON file into a `LicensePolicy` struct
- [ ] Loader returns a clear error message when the file is missing or malformed
- [ ] The policy file path is configurable (not hardcoded)
- [ ] Code compiles without errors (`cargo build`)

## Test Requirements
- [ ] Unit test: loading a valid policy JSON file returns correct `LicensePolicy` with expected allowed/denied lists
- [ ] Unit test: loading a malformed JSON file returns an appropriate error
- [ ] Unit test: loading a non-existent file returns an appropriate error

## Dependencies
- Depends on: Task 1 — Add license report and policy model structs
