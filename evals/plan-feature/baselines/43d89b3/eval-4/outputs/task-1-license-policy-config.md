## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are allowed, denied, or flagged for review. The policy is loaded from a JSON configuration file in the repository. This provides the compliance evaluation foundation that the license report endpoint (Task 2) will use to determine whether each package's license is compliant.

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy struct and deserialization logic for the JSON policy config
- `license-policy.json` — Default license policy configuration file at the repository root

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add serde_json dependency if not already present

## Implementation Notes
Follow the existing model pattern in `common/src/model/`. The `paginated.rs` file in the same directory demonstrates the struct + serde derive pattern used in this codebase.

The LicensePolicy struct should include:
- `allowed_licenses: Vec<String>` — SPDX identifiers of explicitly allowed licenses (e.g., "MIT", "Apache-2.0")
- `denied_licenses: Vec<String>` — SPDX identifiers of explicitly denied licenses (e.g., "GPL-3.0-only")
- `default_policy: PolicyDefault` — enum indicating whether unlisted licenses are allowed or denied (values: `Allow`, `Deny`)

The JSON config file should be loadable from a configurable path (environment variable or config setting), with a sensible default location.

Per CONVENTIONS.md §Key Conventions: use `Result<T, AppError>` with `.context()` wrapping for all error handling in policy loading.
Applies: task modifies `common/src/model/license_policy.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — Use the existing AppError enum for policy loading errors (file not found, parse error)
- `common/src/model/paginated.rs` — Reference for struct definition patterns with serde derives

## Acceptance Criteria
- [ ] LicensePolicy struct deserializes from a JSON file with allowed_licenses, denied_licenses, and default_policy fields
- [ ] Invalid or missing policy files produce clear AppError variants with context messages
- [ ] A default license-policy.json file exists with a reasonable starter policy
- [ ] The policy model is exposed via `common::model::license_policy`

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON string into LicensePolicy
- [ ] Unit test: deserialize a policy with empty allowed/denied lists
- [ ] Unit test: error case — malformed JSON returns an appropriate error
- [ ] Unit test: verify default_policy enum values (Allow, Deny) deserialize correctly
