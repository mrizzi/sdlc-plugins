# Task 6: Update advisory endpoints for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint handlers to work with the updated service layer that now returns status as an enum-derived string instead of a joined lookup value. While the API response shape remains unchanged (status is still a string field), the endpoint handlers may contain status-related query parameter parsing, filter construction, or response mapping logic that references the old `advisory_status` table or `status_id` column. These references must be updated to use the `AdvisoryStatusEnum` type for any status-based filtering or validation at the endpoint level.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to use `AdvisoryStatusEnum` for validation; remove any direct references to `advisory_status` entity
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update if it contains any status-related response mapping that references the old join
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- update route registration if any status-related middleware or extractors reference the old entity

## Implementation Notes
The list endpoint at `GET /api/v2/advisory` likely accepts a `status` query parameter for filtering. If this parameter is currently validated against the `advisory_status` table (e.g., checking if the value exists as a row), it should instead validate against `AdvisoryStatusEnum` variants using Rust's enum parsing.

The response serialization should remain unchanged -- `AdvisorySummary` already contains a status string field, and the model layer (updated in Task 4) handles the enum-to-string conversion.

Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter handling and error responses.

Per CONVENTIONS.md Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md Key Conventions: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for query parameter parsing and filter construction patterns
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper type used by list endpoints

## Acceptance Criteria
- [ ] Status filter query parameter validates against `AdvisoryStatusEnum` variants
- [ ] No references to `advisory_status` entity remain in endpoint handlers
- [ ] `GET /api/v2/advisory` returns advisory list with correct status strings
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with correct status string
- [ ] API response shape is unchanged -- status is still a string field
- [ ] List endpoint continues to return `PaginatedResults<AdvisorySummary>`

## Test Requirements
- [ ] `GET /api/v2/advisory?status=Fixed` returns only advisories with status "Fixed"
- [ ] `GET /api/v2/advisory?status=InvalidStatus` returns a 400 error
- [ ] `GET /api/v2/advisory/{id}` returns the correct status string
- [ ] `cargo build -p fundamental` compiles successfully

## Verification Commands
- `cargo build -p fundamental` -- module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service layer and models

## additional_fields
- **labels**: ai-generated-jira, workflow:feature-branch
- **priority**: High
- **fixVersions**: RHTPA 2.0.0
