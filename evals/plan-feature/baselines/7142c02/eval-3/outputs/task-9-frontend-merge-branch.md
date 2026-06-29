## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the TC-9003 feature branch back into main in the trustify-ui repository. This collects all frontend SBOM comparison work (API types, hooks, comparison page UI, routing, SBOM selection, export, and E2E tests) into a single pull request for review and merge.

## Jira Metadata
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0

## Implementation Notes
Create a pull request from `TC-9003` to `main` in trustify-ui. The PR description should summarize the new SBOM comparison page, the routing setup, the SBOM list page selection enhancement, and the export functionality. Ensure all unit tests, E2E tests, and type checks pass before merging.

## Acceptance Criteria
- [ ] Pull request is created from `TC-9003` to `main` in trustify-ui
- [ ] All CI checks pass (build, unit tests, E2E tests, type check, linting)
- [ ] PR is reviewed and approved
- [ ] Branch is merged to main

## Test Requirements
- [ ] All existing tests continue to pass (`npm test`)
- [ ] New comparison page unit tests pass
- [ ] New E2E tests pass (`npx playwright test`)
- [ ] Type check passes (`npx tsc --noEmit`)
- [ ] No regressions in existing SBOM list, SBOM detail, advisory, or search pages

## Dependencies
- Depends on: Task 8 — Add routing, SBOM list page selection, and export functionality

[sdlc-workflow] Description digest: sha256-md:992bceec0b6112a7dd5cf39bc439089a5bb94d0b58fd51d67c9b61b6ef6c608c
