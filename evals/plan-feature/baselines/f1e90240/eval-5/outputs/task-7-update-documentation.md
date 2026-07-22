# Task 7 -- Update internal architecture documentation

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update internal architecture documentation to reflect the schema change from the `advisory_status` lookup table to the `advisory_status_enum` PostgreSQL enum column on the `advisory` table. Document that advisory status is now stored as an enum column directly on the advisory table and the `advisory_status` lookup table has been removed. No external API documentation changes are needed since the response shape is unchanged.

## Acceptance Criteria
- [ ] Internal architecture documentation reflects the new advisory status enum column
- [ ] Documentation no longer references the `advisory_status` lookup table as a current schema element
- [ ] SeaORM enum mapping approach is documented

## Test Requirements
- [ ] Verify documentation accurately describes the current schema

## Dependencies
- Depends on: Task 2 -- Create migration: add advisory_status_enum type, backfill status column, drop lookup table
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use enum status column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 -- Update advisory integration tests for enum status
