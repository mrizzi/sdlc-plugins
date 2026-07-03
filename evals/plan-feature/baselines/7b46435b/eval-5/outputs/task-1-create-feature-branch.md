## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push feature branch TC-9005 from main. This feature branch will contain all changes for dropping the advisory_status lookup table and migrating to an advisory_status_enum column on the advisory table. A feature branch is required because the migration and code changes must land atomically — merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist.

## Acceptance Criteria
- [ ] Feature branch TC-9005 is created from the latest main
- [ ] Feature branch TC-9005 is pushed to the remote repository
- [ ] Branch name matches the feature issue ID exactly: TC-9005

## Test Requirements
- [ ] Verify the branch exists on the remote after pushing
- [ ] Verify the branch is based on the latest main commit

## Dependencies
None
