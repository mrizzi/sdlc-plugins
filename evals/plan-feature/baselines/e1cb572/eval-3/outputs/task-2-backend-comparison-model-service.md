# Task 2: Implement SBOM comparison model and service layer

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the data model and service layer for SBOM comparison. The comparison service takes two SBOM IDs, fetches their packages and advisories, and computes a structured diff containing: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. No new database tables are needed — the diff is computed on-the-fly from existing entity relationships.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — `SbomComparison` response struct and its sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`)
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomComparisonService` with a `compare(left_id, right_id)` method that computes the diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod compare;` re-export
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod compare;` re-export

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/`: each domain concept has a `model/` struct and a `service/` implementation.
- The `SbomComparison` struct should derive `Serialize` and implement `IntoResponse` following the pattern in `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`).
- The comparison service should:
  1. Use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to validate both SBOM IDs exist (return `AppError::NotFound` if either is missing).
  2. Query `entity/src/sbom_package.rs` join table to get package lists for each SBOM.
  3. Diff packages by name to compute added, removed, and version-changed sets.
  4. Query `entity/src/sbom_advisory.rs` join table to get advisories for each SBOM.
  5. Diff advisories to compute new and resolved vulnerability sets.
  6. Compare `PackageSummary.license` field from `modules/fundamental/src/package/model/summary.rs` to detect license changes.
- All errors should use `Result<T, AppError>` with `.context()` wrapping, consistent with `common/src/error.rs`.
- The response JSON shape must match the contract defined in the feature description:
  ```json
  {
    "added_packages": [...],
    "removed_packages": [...],
    "version_changes": [...],
    "new_vulnerabilities": [...],
    "resolved_vulnerabilities": [...],
    "license_changes": [...]
  }
  ```

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — fetch and validate SBOM existence by ID
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package lists for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — query advisories linked to SBOM packages
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — package struct with `license` field for license change detection
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — advisory struct with `severity` field for vulnerability diff
- `common/src/error.rs::AppError` — error handling for invalid or missing SBOM IDs

## Acceptance Criteria
- [ ] `SbomComparison` struct serializes to the expected JSON shape with all six diff categories
- [ ] Comparison correctly identifies added packages (in right but not left)
- [ ] Comparison correctly identifies removed packages (in left but not right)
- [ ] Comparison correctly identifies version changes for packages present in both SBOMs
- [ ] Comparison correctly identifies new vulnerabilities (advisories in right but not left)
- [ ] Comparison correctly identifies resolved vulnerabilities (advisories in left but not right)
- [ ] Comparison correctly identifies license changes for packages present in both SBOMs
- [ ] Returns appropriate error when either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with known package differences produces correct added/removed/changed counts
- [ ] Unit test: comparison of identical SBOMs returns empty diff arrays
- [ ] Unit test: invalid SBOM ID returns appropriate error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

`[sdlc-workflow] Description digest: sha256-md:b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4`
