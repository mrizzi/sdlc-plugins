## Repository
trustify-backend

## Description
Add a dedicated integration test file for the license compliance report endpoint. Tests run against a real PostgreSQL test database (following the project's existing test conventions) and cover the full request-response cycle, compliance flag correctness, transitive dependency inclusion, and the p95 < 500 ms performance requirement for SBOMs with up to 1000 packages.

## Files to Create
- `tests/api/license_report.rs` — integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — confirm no new dependency is needed; the test binary already pulls in the full server
- `tests/api/sbom.rs` — add a module declaration `mod license_report;` if the test directory uses a single binary entry point, or confirm the new file is picked up automatically

## Implementation Notes
Follow the patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
- Use `assert_eq!(resp.status(), StatusCode::OK)` for HTTP status assertions.
- Use the existing test helper to spin up an Axum test server backed by the PostgreSQL test database.
- Seed data by calling the ingest service (`modules/ingestor/src/service/mod.rs::IngestorService`) directly in the test setup, or by inserting rows via SeaORM into `sbom_package` and `package_license` entities.

Test cases to implement:

**Happy-path compliance report**
1. Ingest an SBOM with three packages: two under `"MIT"` (compliant), one under `"GPL-3.0"` (non-compliant per default policy).
2. `GET /api/v2/sbom/{id}/license-report` → `200 OK`.
3. Assert `groups` has two entries: `{ license: "MIT", compliant: true }` and `{ license: "GPL-3.0", compliant: false }`.
4. Assert the MIT group contains exactly two `PackageRef` entries.

**Transitive dependency inclusion**
1. Ingest an SBOM with a direct package `A` under `"Apache-2.0"` and a transitive dependency `B` under `"LGPL-2.1"`.
2. Assert that both `A` and `B` appear in the report (verify transitive walk).

**Package with no license**
1. Ingest an SBOM with one package that has no `package_license` row.
2. Assert the package appears under the `"NOASSERTION"` group with `compliant: false`.

**Not found**
1. `GET /api/v2/sbom/00000000-0000-0000-0000-000000000000/license-report` → `404 NOT_FOUND`.

**Performance gate**
1. Ingest a synthetic SBOM with 1000 packages spread across 10 license types.
2. Record wall-clock time for 20 requests and assert p95 < 500 ms.
3. Use `std::time::Instant` for timing; skip this test in CI with `#[ignore]` and a comment explaining it is a local performance benchmark.

## Reuse Candidates
- `tests/api/sbom.rs` — test server setup pattern, `assert_eq!(resp.status(), StatusCode::OK)` idiom
- `modules/ingestor/src/service/mod.rs::IngestorService` — use for seeding SBOM and package data in test setup
- `entity/src/package_license.rs` — SeaORM ActiveModel for direct row insertion in test fixtures

## Acceptance Criteria
- [ ] All four functional tests pass against the PostgreSQL test database
- [ ] The `"NOASSERTION"` sentinel case is covered
- [ ] The performance benchmark test exists (marked `#[ignore]`) and documents the 500 ms target in a comment
- [ ] `cargo test` (excluding ignored tests) passes with no failures

## Test Requirements
- [ ] Happy-path compliance report test as described above
- [ ] Transitive dependency inclusion test as described above
- [ ] No-license / NOASSERTION sentinel test
- [ ] 404 not-found test
- [ ] Performance benchmark test (ignored in CI)

## Dependencies
- Depends on: Task 4 — License report endpoint
