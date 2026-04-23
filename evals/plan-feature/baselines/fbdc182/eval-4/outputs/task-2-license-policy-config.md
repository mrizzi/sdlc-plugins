## Repository
trustify-backend

## Description
Add a JSON license policy configuration file to the repository and a loader module that reads and parses it at startup. The policy declares which SPDX license identifiers are considered compliant. The `LicenseReportService` (Task 1) uses the loaded policy to set the `compliant` flag on each `LicenseGroup` in the report.

## Files to Create
- `config/license-policy.json` — JSON policy file listing allowed SPDX license identifiers
- `common/src/license_policy.rs` — `LicensePolicy` struct and `LicensePolicy::load(path: &Path) -> Result<LicensePolicy, AppError>` loader function

## Files to Modify
- `common/src/lib.rs` — expose `pub mod license_policy`
- `server/src/main.rs` — load `LicensePolicy` at startup and pass it (or an `Arc<LicensePolicy>`) into the Axum application state

## Implementation Notes
Policy file shape (example):
```json
{
  "allowed_licenses": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"]
}
```

`LicensePolicy::load` should use `std::fs::read_to_string` and `serde_json::from_str`. Return `AppError` on missing file or parse failure, consistent with the pattern in `common/src/error.rs`.

In `server/src/main.rs`, load the policy from a path provided via an environment variable (e.g., `LICENSE_POLICY_PATH`, defaulting to `config/license-policy.json`). Wrap it in `Arc<LicensePolicy>` and inject it into the Axum `State` extractor so it is available to route handlers without cloning the full struct on every request.

The `LicenseReportService::get_license_groups` (Task 1) should accept `&LicensePolicy` as a parameter and set `compliant: true` on groups whose license is in `allowed_licenses`, and `compliant: false` otherwise.

## Reuse Candidates
- `common/src/error.rs::AppError` — wrap `serde_json` and `std::io` errors with `.context()`
- `server/src/main.rs` — examine existing `State` injection patterns for db connection pool; follow the same approach for `Arc<LicensePolicy>`

## Acceptance Criteria
- [ ] `config/license-policy.json` exists in the repository with at least five default allowed licenses
- [ ] `LicensePolicy::load` parses the JSON correctly and returns an error on malformed input
- [ ] The loaded policy is available to route handlers via Axum `State`
- [ ] A missing policy file at startup causes the server to exit with a descriptive error message
- [ ] `cargo build` succeeds with no new warnings

## Test Requirements
- [ ] Unit test: `LicensePolicy::load` with a valid JSON string returns the expected `allowed_licenses` list
- [ ] Unit test: `LicensePolicy::load` with invalid JSON returns an `AppError`
- [ ] Unit test: a license in `allowed_licenses` is marked `compliant: true`; a license not in the list is marked `compliant: false`
