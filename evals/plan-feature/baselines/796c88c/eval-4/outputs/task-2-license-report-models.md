## Repository
trustify-backend

## Target Branch
main

## Description
Define the response models for the license compliance report endpoint. These models structure the API response that groups packages by license and includes compliance flags. The models follow the existing pattern established by `SbomSummary`, `SbomDetails`, and other response types in the `modules/fundamental/sbom/model/` directory.

## Files to Modify
- `modules/fundamental/sbom/model/mod.rs` -- Add `license_report` module declaration

## Files to Create
- `modules/fundamental/sbom/model/license_report.rs` -- Response model structs:
  - `LicenseReport` -- Top-level response containing a `Vec<LicenseGroup>`, total package count, and compliant/non-compliant/unknown counts
  - `LicenseGroup` -- Represents a single license grouping with fields: `license: String`, `packages: Vec<LicensePackageRef>`, `compliant: ComplianceStatus`, `package_count: usize`
  - `LicensePackageRef` -- Lightweight package reference with `id`, `name`, `version`, and `is_transitive: bool`

## API Changes
- None (models only; endpoint is in Task 4)

## Implementation Notes
- Follow the pattern in `modules/fundamental/sbom/model/summary.rs` and `details.rs` for struct layout and derive macros
- All response structs should derive `Serialize`, `Clone`, and `Debug` for JSON serialization and logging
- Use `utoipa::ToSchema` derive macro if the project uses OpenAPI generation (check existing models for this pattern)
- `ComplianceStatus` is defined in Task 1's license policy module; re-export or reference it from there
- The `LicenseReport` struct should include metadata: `sbom_id`, `generated_at: DateTime<Utc>`, and `policy_version: String`
- Keep the model flat and avoid deep nesting to support efficient JSON serialization

## Acceptance Criteria
- [ ] `LicenseReport` serializes to the expected JSON schema: `{ sbom_id, generated_at, policy_version, total_packages, compliant_count, non_compliant_count, unknown_count, groups: [...] }`
- [ ] `LicenseGroup` contains the license identifier, package list, compliance flag, and count
- [ ] `LicensePackageRef` includes package id, name, version, and transitive dependency flag
- [ ] All structs derive the necessary traits for JSON serialization

## Test Requirements
- [ ] Unit test: `LicenseReport` serializes to valid JSON with expected field names
- [ ] Unit test: `LicenseGroup` correctly represents a group of packages under one license
- [ ] Unit test: empty report (no packages) serializes without errors

## Dependencies
- Depends on: Task 1 -- Define license policy configuration model (for `ComplianceStatus` enum)
