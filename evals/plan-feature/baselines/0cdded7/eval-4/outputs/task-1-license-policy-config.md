# Task 1 — Add license policy configuration model and loader

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are allowed, denied, or flagged for review. The policy is stored as a JSON configuration file in the repository. This task creates the data structures for deserializing the policy and a loader function that reads the configuration at startup or on-demand. This is a foundational piece that the license report service (Task 2) depends on to determine compliance status.

## Files to Create
- `common/src/license_policy/mod.rs` — License policy module with `LicensePolicy` struct and deserialization logic
- `common/src/license_policy/config.rs` — Policy loader that reads and validates the JSON configuration file
- `license-policy.json` — Default license policy configuration file at the repository root

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add `serde_json` dependency if not already present for config deserialization

## Implementation Notes
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` — SPDX identifiers that are always compliant
  - `denied_licenses: Vec<String>` — SPDX identifiers that are never compliant
  - `review_required_licenses: Vec<String>` — SPDX identifiers that require manual review
  - `default_policy: PolicyAction` — enum (`Allow`, `Deny`, `Review`) for licenses not explicitly listed
- Follow the existing pattern in `common/src/` for module organization — see `common/src/db/mod.rs` and `common/src/model/mod.rs` for established module structure
- Use `serde::Deserialize` for the policy struct, matching the deserialization patterns used in entity definitions (e.g., `entity/src/package.rs`)
- The JSON config file should use SPDX license identifiers (e.g., "MIT", "Apache-2.0", "GPL-3.0-only") for consistency with the SPDX standard
- Error handling: return `Result<LicensePolicy, AppError>` from the loader, using the `.context()` wrapping pattern established in `common/src/error.rs`

## Reuse Candidates
- `common/src/error.rs::AppError` — Use the existing error type for configuration loading errors
- `common/src/model/mod.rs` — Follow the existing model organization pattern

## Acceptance Criteria
- [ ] `LicensePolicy` struct deserializes from a JSON configuration file
- [ ] Loader function returns a validated policy or a descriptive error
- [ ] Default `license-policy.json` includes common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and common copyleft licenses (GPL-2.0-only, GPL-3.0-only, AGPL-3.0-only) as denied
- [ ] Unknown SPDX identifiers in the config do not cause a loading error (validated at report time instead)

## Test Requirements
- [ ] Unit test: deserialize a valid JSON policy file into `LicensePolicy`
- [ ] Unit test: deserialize a policy with `default_policy` set to each variant
- [ ] Unit test: loading a malformed JSON file returns an appropriate `AppError`
- [ ] Unit test: loading a non-existent file returns a descriptive error

## Dependencies
- None

[sdlc-workflow] Description digest: sha256:10dad1e7df4966c188628c4e78ece7874774f6515d050439ea0523a6f5ad35e4
