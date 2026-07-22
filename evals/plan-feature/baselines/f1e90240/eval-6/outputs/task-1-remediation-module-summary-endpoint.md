# Task 1: Create remediation module with model types, aggregation service, and summary endpoint

**Epic**: TC-9006: trustify-backend

## Repository

trustify-backend

## Target Branch

main

## Description

Create a new `remediation` domain module under `modules/fundamental/src/` following the existing module pattern (model/ + service/ + endpoints/). This module provides the aggregation service and the `GET /api/v2/remediation/summary` endpoint, which returns vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). Aggregations are computed from existing vulnerability and SBOM relationship data -- no new database tables are required.

## Acceptance Criteria

- [ ] New `remediation` module exists under `modules/fundamental/src/remediation/` with `model/`, `service/`, and `endpoints/` subdirectories
- [ ] `RemediationSummary` model struct defined with severity-by-status counts
- [ ] `RemediationService` implements aggregation queries over existing `advisory`, `sbom_advisory`, and related entity tables
- [ ] `GET /api/v2/remediation/summary` endpoint returns JSON with counts grouped by severity and status
- [ ] Endpoint is registered in `server/src/main.rs`
- [ ] All handlers return `Result<T, AppError>` with `.context()` wrapping
- [ ] Summary endpoint response time meets p95 < 500ms target for up to 10,000 vulnerabilities

## Files to Modify

- `server/src/main.rs` -- mount the new remediation module routes
- `modules/fundamental/Cargo.toml` -- add remediation module to the crate

## Files to Create

- `modules/fundamental/src/remediation/mod.rs` -- module root
- `modules/fundamental/src/remediation/model/mod.rs` -- model module root
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary struct
- `modules/fundamental/src/remediation/service/mod.rs` -- RemediationService with aggregation logic
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for /api/v2/remediation
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler

## API Changes

- **New endpoint**: `GET /api/v2/remediation/summary`
  - Response: JSON object with `counts` array, each entry containing `severity` (Critical/High/Medium/Low), `status` (Open/In Progress/Resolved), and `count` (integer)
  - No authentication changes required

## Implementation Notes

- Follow the module pattern established by `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`: each domain module has `model/`, `service/`, and `endpoints/` subdirectories
- Use `common/src/db/query.rs` for shared query builder helpers (filtering, pagination, sorting)
- All endpoint handlers must return `Result<T, AppError>` using `.context()` wrapping, matching the pattern in `common/src/error.rs`
- Register routes in `endpoints/mod.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`, then mount in `server/src/main.rs`
- Aggregate from existing SeaORM entities: `entity/src/advisory.rs`, `entity/src/sbom_advisory.rs` -- no new database tables or migrations
- Apply `tower-http` caching middleware to the summary endpoint route builder, following the caching convention used in existing endpoint modules

## Convention-Aware Enrichment

- **Module pattern**: Applies: task creates `modules/fundamental/src/remediation/` matching the convention's domain module structure scope.
- **Error handling**: Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's handler return type scope.
- **Endpoint registration**: Applies: task modifies `server/src/main.rs` matching the convention's route mounting scope.
- **Query helpers**: Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's shared query builder scope.
- **Caching**: Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's cache middleware scope.

## Test Requirements

- Unit test for `RemediationService` aggregation logic verifying correct grouping by severity and status
- Verify endpoint returns valid JSON with expected schema
