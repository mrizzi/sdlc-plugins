## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Create a new `remediation` domain module under `modules/fundamental/src/` following the established model/service/endpoints pattern. Implement the aggregation service that computes remediation status counts (Open/In Progress/Resolved) grouped by severity (Critical/High/Medium/Low) from existing vulnerability and SBOM relationship data. Add the `GET /api/v2/remediation/summary` endpoint that returns these aggregated counts.

The aggregation must compute from existing tables (entity/advisory.rs, entity/sbom_advisory.rs) without creating new database tables, per the non-functional requirement.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root
- `modules/fundamental/src/remediation/model/mod.rs` -- model module root
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary struct with severity-by-status breakdown
- `modules/fundamental/src/remediation/service/mod.rs` -- service module root
- `modules/fundamental/src/remediation/service/remediation.rs` -- RemediationService with aggregation queries
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- endpoint route registration for /api/v2/remediation
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` declaration
- `server/src/main.rs` -- mount remediation module routes

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns aggregated remediation counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)

## Implementation Notes
- Per CONVENTIONS.md $Module Pattern: follow the model/ + service/ + endpoints/ directory structure as used by the advisory and sbom modules. See `modules/fundamental/src/advisory/` for the established pattern.
  Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the convention's Rust module scope.
- Per CONVENTIONS.md $Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation. See `modules/fundamental/src/advisory/endpoints/list.rs` for an example.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's .rs endpoint scope.
- Per CONVENTIONS.md $Endpoint Registration: register routes in `endpoints/mod.rs` and mount in `server/main.rs`, following the pattern in `modules/fundamental/src/advisory/endpoints/mod.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's endpoint registration scope.
- The aggregation query must join existing entity tables (`advisory`, `sbom_advisory`) using SeaORM to compute counts without creating new database tables.
- Use `common/src/db/query.rs` for any filtering or pagination helpers.
- Performance target: p95 < 500ms for the summary endpoint.

## Reuse Candidates
- `common/src/db/query.rs` -- shared filtering, pagination, and sorting helpers to reuse for query construction
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper for list-style responses
- `common/src/error.rs::AppError` -- error type for consistent error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- reference implementation of service pattern with SeaORM queries
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- reference for endpoint route registration pattern

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with aggregated counts grouped by severity and status
- [ ] Response includes counts for all four severity levels (Critical, High, Medium, Low) and three statuses (Open, In Progress, Resolved)
- [ ] No new database tables or migrations are created
- [ ] Module follows the established model/service/endpoints directory structure
- [ ] Handler returns `Result<T, AppError>` with proper error context

## Test Requirements
- [ ] Verify the summary endpoint returns correct aggregation counts with known test data
- [ ] Verify the endpoint returns 200 with empty counts when no vulnerability data exists
- [ ] Verify the endpoint handles database errors gracefully with appropriate error responses

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
