## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model types for SBOM comparison results and the service layer that computes the structured diff between two SBOMs. The comparison service queries existing package, advisory, and license data for both SBOMs using SeaORM joins against the sbom_package, sbom_advisory, and package_license tables, then computes the diff in-memory. No new database tables are needed — the diff is computed on-the-fly from existing entity data.

The response shape must match the API contract specified in the feature requirements:
```json
{
  "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
  "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
  "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
  "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
  "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
  "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
}
```

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `modules/fundamental/src/sbom/service/compare.rs` — Comparison service with diff logic: load packages and advisories for both SBOMs, compute set differences, classify version changes as upgrade/downgrade

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` and re-export comparison types
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` and re-export comparison service
- `modules/fundamental/src/sbom/mod.rs` — Ensure model and service submodules are properly exported

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/`: the `model/` directory contains data structs (see `model/summary.rs` for SbomSummary, `model/details.rs` for SbomDetails) and the `service/` directory contains business logic (see `service/sbom.rs` for SbomService).
  Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module scope.
- All comparison structs should derive `Serialize` for JSON serialization, following the pattern in `modules/fundamental/src/sbom/model/summary.rs`.
- The comparison service should accept two SBOM IDs and use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to fetch SBOM data.
- Query package data via the `sbom_package` join table entity (`entity/src/sbom_package.rs`) and package entity (`entity/src/package.rs`). Use `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` which includes the `license` field.
- Query advisory data via the `sbom_advisory` join table entity (`entity/src/sbom_advisory.rs`). Use `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` which includes the `severity` field.
- License change detection should use the `package_license` entity (`entity/src/package_license.rs`).
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` using `.context()` wrapping from `common/src/error.rs`.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust file scope.
- Version change direction (upgrade/downgrade) should be determined by semantic version comparison of left vs right package versions.
- Target p95 < 1s for SBOMs with up to 2000 packages each per NFR — use efficient set operations (HashMaps keyed by package name) rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM details; reuse for loading both left and right SBOM data
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing struct with name, version, and license fields; basis for package comparison
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing struct with advisory_id, severity, and title fields; basis for vulnerability comparison
- `common/src/error.rs::AppError` — existing error type; use for all service error returns
- `entity/src/sbom_package.rs` — SBOM-Package join table entity; use for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity; use for license change detection

## Acceptance Criteria
- [ ] SbomComparisonResult struct contains all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Each sub-struct has fields matching the API contract (e.g., AddedPackage has name, version, license, advisory_count)
- [ ] Comparison service correctly identifies packages present only in the right SBOM as added
- [ ] Comparison service correctly identifies packages present only in the left SBOM as removed
- [ ] Comparison service detects version changes and classifies direction as upgrade or downgrade
- [ ] Comparison service detects new vulnerabilities (advisories in right but not left SBOM)
- [ ] Comparison service detects resolved vulnerabilities (advisories in left but not right SBOM)
- [ ] Comparison service detects license changes for packages present in both SBOMs
- [ ] All service methods return Result<T, AppError>

## Test Requirements
- [ ] Unit test: comparing two identical SBOMs returns empty diff (all categories have zero items)
- [ ] Unit test: comparing SBOMs with different packages returns correct added/removed lists
- [ ] Unit test: comparing SBOMs with same package at different versions returns correct version_changes with direction
- [ ] Unit test: comparing SBOMs with different advisory associations returns correct new/resolved vulnerabilities
- [ ] Unit test: comparing SBOMs where a package changed license returns correct license_changes

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- comparison` — all comparison-related tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
