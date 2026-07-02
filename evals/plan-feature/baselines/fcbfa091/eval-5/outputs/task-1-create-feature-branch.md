# Task 1: Create feature branch TC-9005 from main

## Bookend Type
create-branch

## Repository
trustify-backend

## Target Branch
main

## Description
Create the feature branch `TC-9005` from `main` to isolate all changes for the advisory status table-to-enum migration. This feature requires coordinated schema migrations and tightly coupled code changes that must land atomically: the database migration, entity definitions, service layer, ingestion pipeline, and endpoints all reference either the old `advisory_status` lookup table or the new `status` enum column. Merging any subset independently would break advisory queries. A feature branch ensures all changes are developed and validated together before merging to `main`.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` is created from the latest `main`
- [ ] Branch is pushed to the remote repository
- [ ] Branch protection rules (if any) allow pushes to the feature branch

## Test Requirements
- [ ] Verify the branch exists on the remote with `git ls-remote --heads origin TC-9005`
- [ ] Verify the branch point matches the current `main` HEAD

## Dependencies
- None

## additional_fields
- **labels**: ai-generated-jira, workflow:feature-branch
- **priority**: High
- **fixVersions**: RHTPA 2.0.0
