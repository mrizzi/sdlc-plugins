## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The documentation impact is classified as "Updates to existing content" -- no new documentation pages are needed, and no external API documentation changes are required.

Changes to document:
- The `advisory_status` lookup table has been removed from the database schema
- The `advisory` table now uses a `status` column of type `advisory_status_enum` instead of a `status_id` foreign key
- Advisory queries no longer join the `advisory_status` table, improving query performance
- The advisory ingestion pipeline writes enum values directly to the `status` column
- The SeaORM entity model uses `AdvisoryStatusEnum` with `DeriveActiveEnum` for database mapping

Reference: Feature TC-9005 -- Drop status table and migrate to enum column
Reference material: SeaORM enum mapping documentation

## Acceptance Criteria
- [ ] Architecture documentation accurately reflects the new schema (enum column replaces lookup table)
- [ ] Documentation covers the rationale for the migration (performance improvement, reduced schema complexity)
- [ ] No references to the removed `advisory_status` table remain in documentation
- [ ] Documentation is consistent with the implemented behavior

## Test Requirements
- [ ] Verify documentation accurately describes the new `advisory_status_enum` type and its values
- [ ] Verify no stale references to the `advisory_status` table or `status_id` FK exist in documentation
- [ ] Verify documentation is consistent with the implemented schema and code changes

## Dependencies
- Depends on: Task 4 -- Update advisory service and endpoints to use enum status column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum status directly
- Depends on: Task 6 -- Update integration tests for advisory status enum
