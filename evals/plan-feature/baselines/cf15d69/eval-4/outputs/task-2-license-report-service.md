## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates package license data from existing database entities, walks transitive dependencies, groups packages by license, and evaluates compliance against the configured license policy. This is the core business logic for the license compliance report feature.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to re-export the new service module

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a `generate_report(sbom_id, db, policy)` method that queries package-license data and builds the compliance report

## Implementation Notes
- The service queries existing entities: `entity/src/sbom_package.rs` (SBOM-Package join), `entity/src/package.rs` (Package), and `entity/src/package_license.rs` (Package-License mapping). No new tables or migrations are needed.
- Walk transitive dependencies: use `sbom_package` to find all packages linked to the given SBOM ID, including indirect/transitive relationships if the join table supports depth or parent references. If the current schema only stores direct links, document this limitation and aggregate all linked packages.
- Group packages by their license identifier from `package_license`. Each group becomes a `LicenseGroup` with the license string, list of `PackageRef` entries, and a `compliant` flag evaluated against `LicensePolicyConfig`.
- Load the `LicensePolicyConfig` from `license-policy.json` at service initialization or accept it as a parameter. Prefer passing it as a parameter for testability.
- Per Key Conventions (Error handling): All fallible operations must return `Result<T, AppError>` with `.context()` wrapping, following the pattern in `common/src/error.rs`. Applies: task creates a new service in `modules/fundamental/src/sbom/service/` matching the convention's error handling scope.
- Per Key Conventions (Query helpers): Use shared filtering and query builder helpers from `common/src/db/query.rs` for database queries where applicable. Applies: task creates database queries in a service file matching the convention's query helpers scope.
- Per Key Conventions (Module pattern): Follow the `model/ + service/ + endpoints/` module structure established by existing modules like `advisory/` and `package/`. Applies: task adds a service file within the existing `sbom/service/` directory matching the convention's module pattern scope.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with joins rather than N+1 queries. Consider collecting all package IDs first, then batch-querying their licenses.

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` accepts an SBOM ID and returns a `Result<LicenseReport, AppError>`
- [ ] All packages linked to the SBOM (including transitive dependencies) are included in the report
- [ ] Packages are grouped by license identifier
- [ ] Each group's `compliant` flag is correctly evaluated against the license policy
- [ ] Packages with no license data are placed in an "Unknown" group and flagged as non-compliant
- [ ] The service uses efficient batch queries (no N+1 query patterns)

## Test Requirements
- [ ] Unit test: given a mock set of packages with known licenses and a policy, verify the report groups and compliance flags are correct
- [ ] Unit test: verify that packages with no license are grouped under "Unknown" and marked non-compliant
- [ ] Unit test: verify that an SBOM with no packages returns an empty report (no error)
- [ ] Unit test: verify that denied licenses are flagged non-compliant even when not in the allowed list

[sdlc-workflow] Description digest: sha256-md:725a9aee0052eed418e996ce7c148d9bc4dcb7e0b79a89454a104ece35143ef6
