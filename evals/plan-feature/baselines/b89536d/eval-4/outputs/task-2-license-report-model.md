# Task 2 — Add license report response model

## Repository
trustify-backend

## Target Branch
main

## Description
Define the response model structs for the license compliance report. The report groups packages by license type and includes a compliance flag per group, enabling consumers to quickly identify which license categories contain policy violations.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport and LicenseReportGroup structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the model struct pattern from `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails).
- Use `serde::Serialize` for JSON response serialization.
- The response structure should match the feature requirement:
  ```
  LicenseReport {
      groups: Vec<LicenseReportGroup>
  }
  
  LicenseReportGroup {
      license: String,
      packages: Vec<PackageLicenseEntry>,
      compliant: bool,
  }
  
  PackageLicenseEntry {
      name: String,
      version: String,
      // Other relevant fields from PackageSummary
  }
  ```
- Reference `modules/fundamental/src/package/model/summary.rs` (PackageSummary) for the package fields to include — the `license` field on PackageSummary is the source of license information.
- Per docs/constraints.md §4.6: All file paths are real paths discovered during repository analysis.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the license field; reuse or reference its field structure for PackageLicenseEntry rather than duplicating field definitions.
- `common/src/model/paginated.rs::PaginatedResults` — Reference for response wrapper patterns, though the license report uses a grouping structure rather than pagination.

## Acceptance Criteria
- [ ] LicenseReport struct serializes to the expected JSON shape: `{ groups: [{ license, packages, compliant }] }`
- [ ] PackageLicenseEntry includes relevant package identification fields
- [ ] Module is properly exported via model/mod.rs

## Test Requirements
- [ ] Unit test: LicenseReport serializes to expected JSON structure
- [ ] Unit test: Empty groups list serializes correctly

## Dependencies
- None
