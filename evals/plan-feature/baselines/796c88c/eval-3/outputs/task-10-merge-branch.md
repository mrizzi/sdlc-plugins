## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the `TC-9003` feature branch into `main` in both `trustify-backend` and `trustify-ui` repositories. This finalizes the SBOM comparison view feature after all backend and frontend tasks have been completed and verified. The backend branch should be merged first to ensure the API endpoint is available before the frontend is deployed.

## Files to Modify
- None (merge operation only)

## Implementation Notes
1. Merge `TC-9003` into `main` in `trustify-backend` first (via pull request).
2. After backend merge is confirmed and deployed/available, merge `TC-9003` into `main` in `trustify-ui` (via pull request).
3. Delete the `TC-9003` branch in both repositories after successful merge.

Merge order matters: the frontend depends on the backend endpoint being available. If using CI/CD, ensure the backend deployment completes before merging the frontend PR.

Both PRs should reference TC-9003 in their descriptions for traceability.

## Acceptance Criteria
- [ ] `TC-9003` branch is merged into `main` in `trustify-backend`
- [ ] `TC-9003` branch is merged into `main` in `trustify-ui`
- [ ] Backend merge completes before frontend merge
- [ ] Feature branches are deleted after merge
- [ ] CI passes on both `main` branches after merge
- [ ] SBOM comparison endpoint is accessible in production
- [ ] SBOM comparison page is accessible in production

## Dependencies
- Depends on: Task 5 — Backend integration tests
- Depends on: Task 9 — Frontend MSW mocks and tests
