## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison logic in the SbomService. This service method takes two SBOM IDs, fetches their package lists and associated advisory/license data, and computes a structured diff identifying added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly from existing data without new database tables, per the non-functional requirements.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare` method to SbomService

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (fetch, list, ingest methods) — the new `compare` method should accept two SBOM UUIDs and a database connection reference.
- Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch package lists for each SBOM.
- Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisories linked to each SBOM.
- Use existing entity joins: `entity/src/sbom_package.rs` for SBOM-to-package mapping and `entity/src/sbom_advisory.rs` for SBOM-to-advisory mapping.
- Compute diffs in memory: build HashMaps keyed by package name for O(n) set difference operations.
- For version change direction detection, use semantic version comparison (upgrade vs downgrade).
- Return `Result<SbomComparisonResult, AppError>` following the error handling pattern with `.context()` wrapping from `common/src/error.rs`.
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each — use efficient set operations, avoid N+1 queries.
- Use `entity/src/package_license.rs` for license data to populate LicenseChange entries.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — extend this existing service with the new compare method
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — standard error type for the return value
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package data for both SBOMs
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisory data for vulnerability diff

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id, db)` method is implemented and returns `SbomComparisonResult`
- [ ] Added packages are correctly identified (in right but not in left)
- [ ] Removed packages are correctly identified (in left but not in right)
- [ ] Version changes detect upgrade vs downgrade direction
- [ ] New vulnerabilities are advisories affecting right SBOM but not left
- [ ] Resolved vulnerabilities are advisories affecting left SBOM but not right
- [ ] License changes are detected for packages present in both SBOMs with different licenses
- [ ] Returns appropriate error when either SBOM ID is not found

## Test Requirements
- [ ] Unit test: compare two SBOMs with known diff — verify all six diff categories are correct
- [ ] Unit test: compare identical SBOMs — verify all diff categories are empty
- [ ] Unit test: compare with non-existent SBOM ID — verify error is returned
- [ ] Unit test: verify version change direction detection (upgrade and downgrade cases)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model types

[sdlc-workflow] Description digest: sha256-md:8597c77eb99ff64f2a1806eb8e139e37d402868fb67f174477831aaa12806b90
