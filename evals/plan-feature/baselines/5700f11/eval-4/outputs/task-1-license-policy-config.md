## Repository
trustify-backend

## Description
Add a license compliance policy configuration file and a Rust model to parse it. The policy defines which SPDX license identifiers are considered compliant (allowed), which are explicitly non-compliant (denied), and an optional review-required list. This policy is consumed by the license report service (Task 2) to flag packages with non-compliant or unreviewed licenses.

## Files to Create
- `license-policy.json` -- Default license compliance policy file at the project root, containing JSON with `allowed`, `denied`, and `review_required` arrays of SPDX license identifiers
- `modules/fundamental/src/sbom/model/license_policy.rs` -- Rust struct `LicensePolicy` with fields for allowed/denied/review_required license lists, plus a `load()` function that reads and deserializes the policy file, and an `evaluate(&self, license: &str) -> ComplianceStatus` method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_policy;` declaration

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct organization and derive macros (`Serialize`, `Deserialize`, `Clone`, `Debug`).
- The `LicensePolicy` struct should derive `serde::Deserialize` for JSON parsing.
- Define a `ComplianceStatus` enum with variants: `Compliant`, `NonCompliant`, `ReviewRequired`, `Unknown`.
- The `evaluate` method should check the license string against the denied list first (returns `NonCompliant`), then the allowed list (`Compliant`), then the review list (`ReviewRequired`), and default to `Unknown` for unrecognized licenses.
- Use `serde_json::from_reader` for file parsing with proper error handling via `AppError` from `common/src/error.rs`.
- The default `license-policy.json` should include common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and known copyleft licenses (GPL-2.0-only, GPL-3.0-only, AGPL-3.0-only) as denied, providing a sensible starting point.

## Reuse Candidates
- `common/src/error.rs::AppError` -- Use for error handling when the policy file cannot be read or parsed
- `modules/fundamental/src/sbom/model/summary.rs` -- Reference for struct derive patterns and module organization

## Acceptance Criteria
- [ ] `license-policy.json` exists at project root with valid JSON containing allowed, denied, and review_required arrays
- [ ] `LicensePolicy` struct correctly deserializes the policy file
- [ ] `evaluate()` correctly classifies licenses against all three lists
- [ ] Unknown licenses (not in any list) return `Unknown` status
- [ ] Policy file parse errors produce meaningful error messages via `AppError`

## Test Requirements
- [ ] Unit test: `evaluate` returns `Compliant` for a license in the allowed list
- [ ] Unit test: `evaluate` returns `NonCompliant` for a license in the denied list
- [ ] Unit test: `evaluate` returns `ReviewRequired` for a license in the review list
- [ ] Unit test: `evaluate` returns `Unknown` for an unrecognized license
- [ ] Unit test: deserialization fails gracefully with a clear error for malformed JSON
