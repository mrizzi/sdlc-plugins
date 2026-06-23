# Task 2 — Add license compliance report response model

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model structs for the license compliance report. The report groups packages by license type and flags each group as compliant or non-compliant based on the license policy. These structs define the response shape for the `GET /api/v2/sbom/{id}/license-report` endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReportResponse`, `LicenseGroup`, and `PackageLicenseInfo` structs with serde Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module and re-export types

## Implementation Notes
- Follow the model struct pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — use `#[derive(Clone, Debug, Serialize, Deserialize)]` with serde.
- The response structure must match the feature specification:
  ```
  LicenseReportResponse {
    groups: Vec<LicenseGroup>
  }

  LicenseGroup {
    license: String,                     // SPDX license identifier
    packages: Vec<PackageLicenseInfo>,   // packages with this license
    compliant: bool                      // whether this license is compliant per policy
  }

  PackageLicenseInfo {
    name: String,        // package name
    version: String,     // package version
    transitive: bool     // whether this is a transitive dependency
  }
  ```
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a `license` field — reference this for the license data shape coming from the database.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Struct pattern for serde derives and field naming conventions
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Struct pattern for nested response types
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — `PackageSummary` with the `license` field that maps to package license data from the database

## Acceptance Criteria
- [ ] `LicenseReportResponse` struct exists with a `groups` field of type `Vec<LicenseGroup>`
- [ ] `LicenseGroup` struct includes `license`, `packages`, and `compliant` fields
- [ ] `PackageLicenseInfo` struct includes `name`, `version`, and `transitive` fields
- [ ] All structs derive `Serialize` for JSON API responses

## Test Requirements
- [ ] Unit test: serialize `LicenseReportResponse` to JSON and verify the output matches the expected shape `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Unit test: deserialize a JSON string into `LicenseReportResponse` and verify all fields are populated correctly

## Dependencies
- Depends on: Task 1 — Add license policy configuration model (uses `LicensePolicy` for compliance evaluation context)

[sdlc-workflow] Description digest: sha256-md:d1798094d932ab91e2e9611e06d4c69d47529a8b355b40d4f91cb55d89f641f0