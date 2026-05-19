## Repository
trustify-backend

## Target Branch
main

## Description
Add a configurable license policy mechanism that defines which licenses are compliant and which are not. The policy is stored as a JSON configuration file in the repository and loaded at runtime. This allows organizations to customize their compliance rules without code changes.

## Files to Create
- `config/license-policy.json` — Default license policy file with allow/deny lists and a policy name
- `modules/fundamental/src/sbom/service/license_policy.rs` — Policy loading and evaluation logic: `LicensePolicy` struct and `is_compliant(license: &str) -> bool` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_policy;` declaration

## Implementation Notes
The policy file should follow a simple schema:

```json
{
  "name": "default",
  "mode": "deny-list",
  "denied_licenses": ["GPL-3.0-only", "AGPL-3.0-only", "SSPL-1.0"],
  "allowed_licenses": []
}
```

Two modes should be supported:
- `deny-list` (default): all licenses are compliant unless explicitly listed in `denied_licenses`
- `allow-list`: only licenses explicitly listed in `allowed_licenses` are compliant

The `LicensePolicy` struct should:
1. Implement `Default` to provide a sensible deny-list policy
2. Have a `from_file(path: &Path) -> Result<Self, AppError>` constructor that loads and parses the JSON file
3. Have an `is_compliant(license: &str) -> bool` method for the service layer to call per license group

Use `common/src/error.rs::AppError` for error handling. Follow the error wrapping pattern with `.context()` used throughout the codebase.

The policy file path should be configurable (environment variable or server config), with a fallback to `config/license-policy.json` relative to the working directory.

## Reuse Candidates
- `common/src/error.rs::AppError` — standard error type; use for policy file loading errors
- `modules/fundamental/src/sbom/service/sbom.rs` — demonstrates service-layer patterns including error handling with `.context()`

## Acceptance Criteria
- [ ] `config/license-policy.json` exists with a default deny-list policy covering common copyleft licenses
- [ ] `LicensePolicy` struct loads from a JSON file and evaluates license compliance
- [ ] Both `deny-list` and `allow-list` modes are supported
- [ ] `LicensePolicy::default()` returns a sensible default policy
- [ ] License matching is case-insensitive to handle SPDX identifier variations
- [ ] The module is exported from `modules/fundamental/src/sbom/service/mod.rs`
- [ ] The crate compiles without errors

## Test Requirements
- [ ] Unit test: `LicensePolicy` in deny-list mode correctly flags denied licenses as non-compliant
- [ ] Unit test: `LicensePolicy` in allow-list mode correctly flags unlisted licenses as non-compliant
- [ ] Unit test: license matching is case-insensitive (e.g., "MIT" and "mit" both match)
- [ ] Unit test: `LicensePolicy::default()` returns a valid policy
- [ ] Unit test: `from_file` returns an appropriate error for a missing or malformed file

## Verification Commands
- `cargo check -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental license_policy` — policy unit tests should pass
