# Task 1 — Add license compliance policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license compliance policy model that defines which licenses are approved, restricted, or denied. The policy is loaded from a JSON configuration file at startup. This provides the foundation for evaluating license compliance in the report endpoint (Task 3).

## Files to Modify
- `common/src/lib.rs` — add `policy` module declaration
- `common/Cargo.toml` — add serde_json dependency if not already present

## Files to Create
- `common/src/policy/mod.rs` — LicensePolicy struct with fields: `approved: Vec<String>`, `restricted: Vec<String>`, `denied: Vec<String>`; includes `load_from_file` function and `is_compliant(license: &str) -> ComplianceStatus` method
- `common/src/policy/default_policy.json` — default license policy configuration file with common approved licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and denied licenses (GPL-3.0, AGPL-3.0)

## Implementation Notes
- Follow the established module pattern in `common/src/` — see `common/src/db/mod.rs` for the module structure convention.
- Use `serde::Deserialize` for the policy struct, consistent with the serialization patterns throughout the codebase.
- The `ComplianceStatus` enum should have variants: `Approved`, `Restricted`, `Denied`, `Unknown` (for licenses not in any list).
- Error handling: return `Result<LicensePolicy, AppError>` from `load_from_file`, using the existing `AppError` enum from `common/src/error.rs` with `.context()` wrapping per project convention.
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format, reference TC-9004 in the footer, and include `--trailer="Assisted-by: Claude Code"`.
- Per constraints doc section 5 (Code Change Rules): scope changes to the files listed above; inspect existing code before modifying.

## Reuse Candidates
- `common/src/error.rs::AppError` — use for error handling in policy loading, consistent with all other modules
- `common/src/model/mod.rs` — follow the model definition patterns used by existing domain models

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `is_compliant` correctly categorizes licenses as Approved, Restricted, Denied, or Unknown
- [ ] Default policy file exists with sensible defaults for common open-source licenses
- [ ] Policy loading errors produce clear error messages via `AppError`

## Test Requirements
- [ ] Unit test: `LicensePolicy::load_from_file` successfully loads the default policy
- [ ] Unit test: `is_compliant` returns `Approved` for MIT license
- [ ] Unit test: `is_compliant` returns `Denied` for GPL-3.0 license
- [ ] Unit test: `is_compliant` returns `Unknown` for an unlisted license
- [ ] Unit test: loading a malformed JSON file returns an appropriate error

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:330dcdc9f5679b98b50af65b24251e9b81d4144173b23774634b9a1bd28906f4
