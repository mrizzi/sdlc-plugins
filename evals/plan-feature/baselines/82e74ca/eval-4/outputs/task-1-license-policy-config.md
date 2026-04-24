# Task 1 — Add license policy configuration

## Repository
trustify-backend

## Description
Add a configurable license policy that defines which licenses are compliant and which are non-compliant. The policy is stored as a JSON configuration file in the repository and loaded at startup. This policy is used by the license report endpoint (Task 3) to flag packages with non-compliant licenses.

## Files to Create
- `config/license-policy.json` — JSON file defining license compliance rules (allowed licenses, denied licenses, and unknown-license handling policy)

## Files to Modify
- `common/src/lib.rs` — add a `policy` module or re-export for license policy types
- `common/src/model/mod.rs` — add license policy model structs

## Implementation Notes
- Define a `LicensePolicy` struct with fields: `allowed: Vec<String>` (SPDX identifiers that are compliant), `denied: Vec<String>` (SPDX identifiers that are non-compliant), and `default_policy: PolicyDefault` enum (`Allow` or `Deny`) for licenses not explicitly listed.
- The JSON config file should use SPDX license identifiers (e.g., "MIT", "Apache-2.0", "GPL-3.0-only").
- Follow the existing model pattern in `common/src/model/` — see `common/src/model/paginated.rs` for struct conventions (derive `Serialize`, `Deserialize`, `Clone`, `Debug`).
- Load the policy file path from an environment variable or default to `config/license-policy.json`. Use `serde_json::from_reader` for deserialization.
- The policy struct should be registered in the application state (Axum `Extension` or `State`) so it can be injected into service handlers.
- Per constraints doc section 5: implementation must follow existing patterns found in the code.

## Reuse Candidates
- `common/src/model/paginated.rs` — demonstrates the existing model struct pattern with derives and serialization
- `server/src/main.rs` — shows how application state and extensions are registered during Axum server setup

## Acceptance Criteria
- [ ] A `config/license-policy.json` file exists with a default policy listing common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and common copyleft licenses (GPL-2.0-only, GPL-3.0-only, AGPL-3.0-only) as denied
- [ ] A `LicensePolicy` struct is defined with `Serialize` and `Deserialize` derives
- [ ] The policy file is loaded and made available in the Axum application state
- [ ] Invalid or missing policy files produce a clear error at startup

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON into the `LicensePolicy` struct
- [ ] Unit test: verify that missing policy file returns an appropriate error
- [ ] Unit test: verify policy lookup returns correct compliance status for allowed, denied, and unlisted licenses

## Dependencies
None
