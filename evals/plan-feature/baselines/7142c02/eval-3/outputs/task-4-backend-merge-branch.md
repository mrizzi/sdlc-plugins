## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the TC-9003 feature branch back into main in the trustify-backend repository. This collects all backend SBOM comparison work (model types, service logic, and REST endpoint) into a single pull request for review and merge.

## Jira Metadata
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0

## Implementation Notes
Create a pull request from `TC-9003` to `main` in trustify-backend. The PR description should summarize the new `GET /api/v2/sbom/compare` endpoint and the comparison service logic. Ensure all integration tests pass before merging.

## Acceptance Criteria
- [ ] Pull request is created from `TC-9003` to `main` in trustify-backend
- [ ] All CI checks pass (build, tests, linting)
- [ ] PR is reviewed and approved
- [ ] Branch is merged to main

## Test Requirements
- [ ] All existing tests continue to pass (`cargo test`)
- [ ] New comparison endpoint integration tests pass
- [ ] No regressions in existing SBOM, advisory, or search endpoints

## Dependencies
- Depends on: Task 3 — Add SBOM comparison REST endpoint

[sdlc-workflow] Description digest: sha256-md:1d1643b9c601dfb6330482a5234075b94643d8092b3b57b16098279f12019929
