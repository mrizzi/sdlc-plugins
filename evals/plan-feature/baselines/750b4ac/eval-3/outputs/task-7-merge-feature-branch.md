# Task 7 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the new SBOM comparison backend endpoint (`GET /api/v2/sbom/compare`), the comparison diff service, the frontend comparison page with selectors and collapsible diff sections, the API types/hooks, and the SbomListPage compare action.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2 through 6

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All backend integration tests pass on the feature branch
- [ ] All frontend unit and E2E tests pass on the feature branch

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests
- Depends on: Task 4 — Add comparison API types, client function, and React Query hook
- Depends on: Task 5 — Add SbomComparePage with diff sections
- Depends on: Task 6 — Add comparison route and SbomListPage compare action

[sdlc-workflow] Description digest: sha256-md:835dd1b7b59b6b2e9b8f62223ee816c66d6c69fbd9de5b148f57580527c20749
