# Task 2 — Add SBOM comparison model and diff service

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model types for SBOM comparison results and implement the diff computation logic in SbomService. The comparison service computes a structured diff between two SBOMs by querying existing package, advisory, and license data — no new database tables are needed. The diff includes: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export new comparison model types
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to SbomService

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange structs

## API Changes
- None (this task adds the service layer; the endpoint is in Task 3)

## Implementation Notes
- Follow the existing model pattern: each domain entity has its own file under `model/` (see `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for the established pattern).
- The `compare` method on `SbomService` should accept two SBOM IDs, fetch their package lists via the existing `PackageService` (at `modules/fundamental/src/package/service/mod.rs`), and compute the diff in memory.
- For vulnerability diff: use `AdvisoryService` (at `modules/fundamental/src/advisory/service/advisory.rs`) to fetch advisories linked to each SBOM via the `sbom_advisory` join table (entity at `entity/src/sbom_advisory.rs`).
- For license diff: use the `package_license` entity (at `entity/src/package_license.rs`) to compare licenses per package between the two SBOMs.
- For version changes, include a `direction` field with values "upgrade" or "downgrade" determined by semver comparison of the left and right versions.
- All handler return types should use `Result<T, AppError>` with `.context()` wrapping per the project's error handling convention.
- Response time target: p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashMaps keyed by package name) for diffing rather than nested loops.
- Use `common/src/db/query.rs` for any query builder helpers needed.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list/ingest methods; extend with compare
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package lists for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories linked to SBOMs
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license diff
- `common/src/error.rs::AppError` — error type for Result returns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field, reuse for package data

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Each sub-struct contains the fields specified in the API response shape (see feature description)
- [ ] `SbomService::compare(left_id, right_id)` returns `Result<SbomComparisonResult, AppError>`
- [ ] Diff correctly identifies packages added in the right SBOM but absent in the left
- [ ] Diff correctly identifies packages removed from the left SBOM but absent in the right
- [ ] Diff correctly identifies version changes with upgrade/downgrade direction
- [ ] Diff correctly identifies new and resolved vulnerabilities by comparing advisory sets
- [ ] Diff correctly identifies license changes for packages present in both SBOMs

## Test Requirements
- [ ] Unit test: compare two SBOMs where the right has additional packages — verify `added_packages` is populated
- [ ] Unit test: compare two SBOMs where the right is missing packages from the left — verify `removed_packages` is populated
- [ ] Unit test: compare two SBOMs with version changes — verify `version_changes` includes correct direction
- [ ] Unit test: compare two SBOMs with different advisory sets — verify `new_vulnerabilities` and `resolved_vulnerabilities`
- [ ] Unit test: compare two SBOMs with license changes — verify `license_changes` is populated
- [ ] Unit test: compare identical SBOMs — verify all diff sections are empty

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256-md:358cc6823fe13d9866e662990ad3865e1a210461ad0d4702c91e7b40cacb07d4
