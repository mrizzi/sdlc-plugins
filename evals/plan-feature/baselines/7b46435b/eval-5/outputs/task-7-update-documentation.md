## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the advisory_status lookup table to the advisory_status_enum column on the advisory table. The documentation should describe the new enum-based status model, the removal of the join, and the simplified query patterns. No external API documentation changes are needed since the response shape is unchanged.

Doc impact type: Updates to existing content. The Feature's Documentation Considerations indicate minor updates to internal architecture docs to reflect the schema change. Reference material: SeaORM enum mapping documentation.

## Acceptance Criteria
- [ ] Architecture documentation reflects the enum column instead of the lookup table
- [ ] No stale references to advisory_status table in documentation
- [ ] Schema descriptions show the direct status enum column on the advisory table

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented schema changes

## Dependencies
- Depends on: Task 2 — Database migration
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
- Depends on: Task 6 — Update integration tests
