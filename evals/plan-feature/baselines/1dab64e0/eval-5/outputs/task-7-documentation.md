## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation should describe the new schema structure, the rationale for the migration (eliminating unnecessary join overhead, simplifying queries), and the fact that no external API changes were made. The doc impact type is "Updates to existing content" as identified in the Feature's Documentation Considerations section. Reference Feature TC-9005 for full context.

No external API documentation changes are needed since the response shape remains identical.

## Acceptance Criteria
- [ ] Internal architecture documentation accurately reflects the new `advisory.status` enum column schema
- [ ] Documentation explains the rationale for removing the `advisory_status` lookup table
- [ ] Documentation notes that no external API changes occurred (response shape unchanged)
- [ ] Documentation references the `advisory_status_enum` PostgreSQL type and its values (`New`, `Analyzing`, `Fixed`, `Rejected`)

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented schema changes
- [ ] Documentation correctly lists all four enum values
- [ ] No references to the removed `advisory_status` lookup table remain in architecture documentation

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum status writes
- Depends on: Task 6 — Update advisory integration tests for status enum
