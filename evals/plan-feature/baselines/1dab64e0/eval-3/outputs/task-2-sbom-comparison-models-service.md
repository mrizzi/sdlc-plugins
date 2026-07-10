## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model structs and diff computation service for SBOM comparison. The comparison service takes two SBOM IDs, loads their package and advisory data using existing services, and computes a structured diff containing: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This is the core business logic that powers the comparison endpoint added in Task 3.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomCompareService` with a `compare(left_id, right_id)` method that computes the structured diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to export the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to export the new service module

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/` where each domain concept has separate `model/` and `service/` sub-modules.

The comparison result struct should derive `Serialize` and `Deserialize` for JSON serialization, following the pattern used by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`.

The diff service should:
1. Use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to fetch both SBOMs and their associated packages
2. Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to load package details including license information
3. Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to load advisories linked to each SBOM via the `sbom_advisory` join table
4. Compute the diff by comparing package sets (by name), version sets, advisory sets, and license values
5. Return `Result<SbomComparisonResult, AppError>` following the error handling pattern with `.context()` wrapping per `common/src/error.rs`

The `direction` field in `VersionChange` should be computed by comparing semver strings (upgrade vs downgrade).

Per CONVENTIONS.md: all service methods return `Result<T, AppError>` with `.context()` wrapping for error propagation.
Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` service file scope.

Per CONVENTIONS.md: follow the established module pattern of `model/ + service/ + endpoints/` for organizing domain code.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` and `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` module structure scope.

Non-functional: comparison must complete in p95 < 1s for SBOMs with up to 2000 packages each. Avoid N+1 queries — batch-load packages and advisories for both SBOMs in bulk queries.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service for fetching SBOM data; use its `fetch` method to load both SBOMs
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct serialization patterns and field naming conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field needed for vulnerability diff entries
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the license field needed for license change detection
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for loading packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for loading advisories per SBOM
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct contains all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Each diff category struct has the fields specified in the API response shape (see feature description)
- [ ] `SbomCompareService::compare()` correctly identifies added, removed, and version-changed packages
- [ ] Vulnerability diff correctly detects advisories unique to each SBOM
- [ ] License change detection identifies packages with different license values between SBOMs
- [ ] Version change direction (upgrade/downgrade) is computed correctly

## Test Requirements
- [ ] Unit test: comparing two identical SBOMs returns empty diff categories
- [ ] Unit test: comparing SBOMs with non-overlapping packages correctly categorizes all as added/removed
- [ ] Unit test: version change direction is correctly computed for upgrade and downgrade cases
- [ ] Unit test: advisory diff correctly classifies new vs resolved vulnerabilities

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
