# Repository Impact Map -- TC-9006: Add vulnerability remediation tracking dashboard

## trustify-backend

changes:
  - Add remediation domain module with model/service/endpoints structure under modules/fundamental/src/remediation/
  - Implement GET /api/v2/remediation/summary endpoint with severity-by-status aggregation from existing advisory and SBOM tables
  - Implement GET /api/v2/remediation/by-product endpoint with per-product remediation breakdown supporting pagination
  - Mount remediation module routes in server/src/main.rs
  - Add integration tests for both remediation endpoints in tests/api/remediation.rs

## trustify-ui

changes:
  - Add TypeScript interfaces for RemediationSummary and ProductRemediation response types in src/api/models.ts
  - Add API client functions (fetchRemediationSummary, fetchRemediationByProduct) in src/api/rest.ts
  - Create React Query hooks (useRemediationSummary, useRemediationByProduct) in src/hooks/
  - Create RemediationDashboardPage with summary cards and progress chart in src/pages/RemediationDashboardPage/
  - Add filterable vulnerability table component with severity/product/status filters
  - Register /remediation route in src/routes.tsx and add navigation entry in src/App.tsx

## Workflow Mode

**Selected mode:** feature-branch

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present -- the frontend remediation dashboard page requires the backend GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product endpoints that do not yet exist. Merging the frontend changes without the backend would result in a broken dashboard page with failing API calls.

Interdependent tasks:
- Frontend Tasks 5-8 depend on backend Tasks 2-3 for API endpoint availability
- The dashboard page (Task 6) and vulnerability table (Task 7) cannot function without the API hooks (Task 5), which in turn require the backend endpoints (Tasks 2-3)

The `workflow:feature-branch` label will be applied to the feature issue TC-9006 in Step 6a.

## Epic Grouping

**Strategy:** by-repository (from CLAUDE.md Hierarchy Configuration)

| Epic | Summary | Issue Type | Parent | Tasks |
|---|---|---|---|---|
| Epic A | TC-9006: trustify-backend | Epic (level 1) | TC-9006 | Task 1, Task 2, Task 3, Task 4, Task 9, Task 10 |
| Epic B | TC-9006: trustify-ui | Epic (level 1) | TC-9006 | Task 5, Task 6, Task 7, Task 8 |

### Epic Creation Details

Epics are created with issue type "Epic" (hierarchyLevel 1) with parent set to feature issue key TC-9006.

**Epic A -- TC-9006: trustify-backend**
- Issue type: Epic (level 1)
- Parent: TC-9006
- Summary: TC-9006: trustify-backend
- Description: Backend implementation for the vulnerability remediation tracking dashboard. Includes the remediation domain module with summary and by-product aggregation endpoints, integration tests, feature branch bookend tasks, and documentation.
- additional_fields:
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```

**Epic B -- TC-9006: trustify-ui**
- Issue type: Epic (level 1)
- Parent: TC-9006
- Summary: TC-9006: trustify-ui
- Description: Frontend implementation for the vulnerability remediation tracking dashboard. Includes API client layer with TypeScript types and React Query hooks, dashboard page with summary cards and progress chart, filterable vulnerability table, and route registration.
- additional_fields:
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```

### Incorporates Links

- TC-9006 "Incorporates" Epic A (TC-9006: trustify-backend)
- TC-9006 "Incorporates" Epic B (TC-9006: trustify-ui)

Note: Incorporates links go from Feature to Epics only, not from Feature to individual Tasks. Tasks inherit hierarchy through their Epic parent field.

### Task-to-Epic Assignment

| Task | Summary | Repository | Parent Epic |
|---|---|---|---|
| Task 1 | Create feature branch TC-9006 from main | trustify-backend | Epic A (TC-9006: trustify-backend) |
| Task 2 | Add remediation module with summary aggregation service and endpoint | trustify-backend | Epic A (TC-9006: trustify-backend) |
| Task 3 | Add per-product remediation breakdown endpoint | trustify-backend | Epic A (TC-9006: trustify-backend) |
| Task 4 | Add integration tests for remediation endpoints | trustify-backend | Epic A (TC-9006: trustify-backend) |
| Task 5 | Add remediation API types, client functions, and React Query hooks | trustify-ui | Epic B (TC-9006: trustify-ui) |
| Task 6 | Create remediation dashboard page with summary cards and progress chart | trustify-ui | Epic B (TC-9006: trustify-ui) |
| Task 7 | Add filterable vulnerability table to remediation dashboard | trustify-ui | Epic B (TC-9006: trustify-ui) |
| Task 8 | Register /remediation route and add navigation entry | trustify-ui | Epic B (TC-9006: trustify-ui) |
| Task 9 | Document remediation dashboard and API endpoints | trustify-backend | Epic A (TC-9006: trustify-backend) |
| Task 10 | Merge feature branch TC-9006 to main | trustify-backend | Epic A (TC-9006: trustify-backend) |

## Excluded Requirements

- **Export remediation report as CSV** (non-MVP) -- This requirement is marked as non-MVP in the Feature description. It can be planned in a follow-up iteration after the MVP dashboard is delivered. No missing inputs prevent planning; deferred by MVP scope decision.
