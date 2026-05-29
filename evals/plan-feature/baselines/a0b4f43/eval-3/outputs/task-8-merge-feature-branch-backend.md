## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main` in the trustify-backend repository. The PR description should summarize all backend changes made for the SBOM comparison feature: the comparison diff model structs, the comparison service logic, the GET /api/v2/sbom/compare endpoint, and the associated integration tests.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review in the trustify-backend repository
- [ ] The PR description summarizes all backend changes for the SBOM comparison feature

## Test Requirements
- [ ] Verify all intermediate backend task PRs (Tasks 3 and 4) have been merged into the TC-9003 feature branch before creating the merge PR

## Dependencies
- Depends on: Task 3 — Add SBOM comparison model and service (trustify-backend)
- Depends on: Task 4 — Add SBOM comparison endpoint and integration tests (trustify-backend)