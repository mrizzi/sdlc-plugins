# TC-9003-7: Merge feature branch

## Repository

trustify-backend

## Target Branch

main

## Bookend Type

merge-branch

## Description

Merge the `TC-9003` feature branch to `main` in both `trustify-backend` and `trustify-ui` repositories after all implementation tasks are complete and verified. This coordinated merge ensures the backend comparison endpoint and frontend comparison UI are delivered together.

## Dependencies

- TC-9003-2 (backend models and service)
- TC-9003-3 (backend endpoint and tests)
- TC-9003-4 (frontend API types and hook)
- TC-9003-5 (frontend comparison page)
- TC-9003-6 (frontend list page selection)

## Acceptance Criteria

- [ ] All intermediate task PRs have been merged to the `TC-9003` feature branch
- [ ] CI passes on the feature branch in both repositories
- [ ] Feature branch `TC-9003` is merged to `main` in `trustify-backend`
- [ ] Feature branch `TC-9003` is merged to `main` in `trustify-ui`
- [ ] `GET /api/v2/sbom/compare` endpoint is accessible on main
- [ ] `/sbom/compare` page is accessible on main

## Test Requirements

- [ ] All backend integration tests pass on main after merge
- [ ] All frontend unit and E2E tests pass on main after merge

[Description digest: sha256-md:a9d3e7b1c5f0a6d2e8b4f9c3a7e1d5b0f6c2a8e4d0b7f3c9a5e2d8b4f1c6a0e3]
