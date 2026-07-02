## additional_fields
```
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the backend SBOM comparison model, service, and endpoint; the frontend API layer, comparison page, SBOM list integration, and tests; and the documentation. This is the final task that delivers the complete SBOM comparison view feature to `main`.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes made across all intermediate tasks
- [ ] All CI checks pass on the PR
- [ ] No merge conflicts with `main`

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify CI pipeline passes on the merge PR

## Dependencies
- Depends on: Task 2 — Backend comparison model structs
- Depends on: Task 3 — Backend comparison service
- Depends on: Task 4 — Backend comparison endpoint and tests
- Depends on: Task 5 — Frontend API layer
- Depends on: Task 6 — Frontend comparison page
- Depends on: Task 7 — Frontend SBOM list and tests
- Depends on: Task 8 — Documentation
