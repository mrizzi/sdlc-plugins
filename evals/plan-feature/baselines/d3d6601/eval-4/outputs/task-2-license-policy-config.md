## Repository
trustify-backend

## Target Branch
main

## Description
Add a configurable license policy mechanism that defines which licenses are compliant and which are not. The policy is stored as a JSON configuration file in the repository and loaded at service startup. This policy is used by the license report service to flag non-compliant license groups.

## Files to Create
- `modules/fundamental/src/sbom/service/license_policy.rs` — license policy loading, parsing, and evaluation logic
- `config/license-policy.json` — default license policy configuration file listing allowed and denied license identifiers

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add module declaration for `license_policy`

## Implementation Notes
- The license policy JSON file should follow a simple structure: `{ "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", ...], "denied": ["GPL-3.0-only", "AGPL-3.0-only", ...], "default": "deny" }`. The `default` field determines the behavior for licenses not in either list.
- Implement a `LicensePolicy` struct that loads from the JSON file and exposes an `is_compliant(license: &str) -> bool` method.
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` — services are structs with methods that take `&self` and return `Result<T, AppError>`.
- Use `common/src/error.rs::AppError` for error handling with `.context()` wrapping for all fallible operations.
- The policy file path should be configurable (e.g., via environment variable or server configuration), with a sensible default pointing to the bundled `config/license-policy.json`.
- Reference the SPDX license identifier format for license string matching — use case-insensitive comparison to handle variations.

## Reuse Candidates
- `common/src/error.rs::AppError` — established error type used across all service modules
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service struct pattern, dependency injection, and error handling conventions

## Acceptance Criteria
- [ ] `LicensePolicy` struct can load from a JSON configuration file
- [ ] `is_compliant()` method correctly evaluates licenses against the allowed/denied lists
- [ ] Default policy file `config/license-policy.json` exists with a reasonable set of common open-source licenses
- [ ] Handles unknown licenses according to the `default` field policy
- [ ] Error handling follows the `AppError` pattern with `.context()` wrapping

## Test Requirements
- [ ] Unit test verifying allowed licenses return `compliant: true`
- [ ] Unit test verifying denied licenses return `compliant: false`
- [ ] Unit test verifying the `default` field behavior for unknown licenses
- [ ] Unit test verifying graceful error handling when policy file is missing or malformed

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental -- license_policy` — unit tests pass

## Documentation Updates
- `README.md` — add section documenting the license policy configuration file format and how to customize it

## Dependencies
- None

[sdlc-workflow] Description digest: sha256:2cbbe74d948c99739b248cff32d1caac6418fb08c73e8a04e27cbbaa549ebcab
