## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main` in the trustify-ui repository. The PR description should summarize all frontend changes made for the SBOM comparison feature: TypeScript API types, React Query hook, the comparison page with PatternFly diff sections, route registration, SBOM list selection integration, and test coverage.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review in the trustify-ui repository
- [ ] The PR description summarizes all frontend changes for the SBOM comparison feature

## Test Requirements
- [ ] Verify all intermediate frontend task PRs (Tasks 5, 6, and 7) have been merged into the TC-9003 feature branch before creating the merge PR

## Dependencies
- Depends on: Task 5 — Add API types, client function, and React Query hook for SBOM comparison (trustify-ui)
- Depends on: Task 6 — Create SBOM comparison page with diff sections and routing (trustify-ui)
- Depends on: Task 7 — Add tests for SBOM comparison feature (trustify-ui)