# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant for the organization. The policy is stored as a JSON configuration file in the repository root and loaded at runtime. This provides the compliance evaluation foundation used by the license report service (Task 3) and endpoint (Task 4).

## Files to Create
- `common/src/model/license_policy.rs` — `LicensePolicy` struct with `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>`, and `default_policy: PolicyDefault` enum; includes `load_from_file()` constructor and `is_compliant(license: &str) -> bool` evaluation method
- `config/default-license-policy.json` — Default license policy configuration file with common open-source license classifications (MIT, Apache-2.0, BSD-2-Clause as allowed; GPL-3.0-only, AGPL-3.0-only as denied)

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add serde_json dependency if not already present

## Implementation Notes
- Follow the existing model pattern in `common/src/model/paginated.rs` for struct definition style — use `#[derive(Clone, Debug, Serialize, Deserialize)]` with serde derives.
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` — SPDX identifiers for licenses that are compliant
  - `denied_licenses: Vec<String>` — SPDX identifiers for licenses that are non-compliant
  - `default_policy: PolicyDefault` — enum with variants `Allow` and `Deny`, controlling how licenses not in either list are treated
- Implement `is_compliant(&self, license: &str) -> bool` that checks a license identifier against the policy: return `true` if in allowed list, `false` if in denied list, and defer to `default_policy` for unlisted licenses.
- Use `serde::Deserialize` for JSON deserialization, consistent with how other models in `common/` derive serde traits.
- Error handling: return `Result<LicensePolicy, AppError>` from `load_from_file`, using the existing `AppError` enum from `common/src/error.rs` with `.context()` wrapping per project convention.
- Per the NFR, the policy is a JSON config file in the repo — not a database table.

## Reuse Candidates
- `common/src/model/paginated.rs` — Demonstrates the struct + derive macro pattern used in the common crate
- `common/src/error.rs::AppError` — Standard error type for consistent error handling when policy loading fails

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `is_compliant()` correctly classifies allowed, denied, and unlisted licenses based on default policy
- [ ] A default license policy JSON file exists with reasonable defaults (e.g., MIT, Apache-2.0 as allowed; GPL-3.0-only as denied)
- [ ] Policy loading errors produce clear error messages via `AppError`

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON string into `LicensePolicy`
- [ ] Unit test: `is_compliant` returns true for allowed licenses
- [ ] Unit test: `is_compliant` returns false for denied licenses
- [ ] Unit test: `is_compliant` respects the `default_policy` for unlisted licenses (both Allow and Deny defaults)
- [ ] Unit test: handle malformed policy JSON gracefully (return error, not panic)

## Verification Commands
- `cargo test -p common` — all tests pass including new license policy tests

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:8699910d96b8585c40debcf4de66fc11e54d797b22c0feda575db6636e25c1bb