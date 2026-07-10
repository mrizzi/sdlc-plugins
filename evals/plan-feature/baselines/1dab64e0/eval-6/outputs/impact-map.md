# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Impact Map

```
trustify-backend:
  changes:
    - Add remediation domain model with severity x status aggregation structs (RemediationSummary, ProductRemediation)
    - Add RemediationService with query-based aggregation from existing entity tables (no new database tables)
    - Add GET /api/v2/remediation/summary endpoint returning severity x status counts
    - Add GET /api/v2/remediation/by-product endpoint with pagination support
    - Mount remediation module routes in server/src/main.rs
    - Add integration tests for remediation endpoints in tests/api/remediation.rs

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types in src/api/models.ts
    - Add API client functions (fetchRemediationSummary, fetchRemediationByProduct) in src/api/rest.ts
    - Add React Query hooks (useRemediationSummary, useRemediationByProduct) in src/hooks/
    - Create RemediationDashboardPage at /remediation with summary cards (Open/In Progress/Resolved)
    - Add progress chart showing remediation trend over 30 days
    - Add filterable vulnerability table with severity, product, and status filters
    - Register /remediation route in src/routes.tsx with lazy loading
```

## Excluded Requirements

- **Export remediation report as CSV** — Non-MVP requirement per feature specification. Can be planned in a follow-up iteration once the core dashboard is delivered.

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified. All changes are additive:
- Backend endpoints are new (do not modify existing API contracts)
- Frontend page is new (does not modify existing pages or routes)
- No coordinated schema migrations (no new database tables — aggregations computed from existing data)
- No breaking API changes
- No cross-cutting refactors

The frontend depends on the backend endpoints existing, but the backend can land independently on main without breaking anything. Task dependencies (frontend tasks depend on backend tasks) ensure correct ordering.

## Epic Hierarchy

**Grouping strategy:** by-repository (from CLAUDE.md Hierarchy Configuration)

### Epic 1: TC-9006: trustify-backend
- **Issue type:** Epic (hierarchyLevel 1)
- **Parent:** TC-9006 (Feature)
- **Summary:** TC-9006: trustify-backend
- **Description:** Backend implementation for the vulnerability remediation tracking dashboard. Includes the remediation domain model, aggregation service, REST API endpoints, and integration tests.
- **Tasks:** Task 1, Task 2, Task 3, Task 7
- **Creation parameters:**
  ```
  jira.create_issue(
    projectKey="TC",
    issueTypeName="Epic",
    summary="TC-9006: trustify-backend",
    description="Backend implementation for the vulnerability remediation tracking dashboard. Includes the remediation domain model, aggregation service, REST API endpoints (GET /api/v2/remediation/summary, GET /api/v2/remediation/by-product), and integration tests.",
    parent="TC-9006",
    additional_fields={
      "labels": ["ai-generated-jira"],
      "priority": {"name": "Major"},
      "fixVersions": [{"name": "RHTPA 1.5.0"}]
    }
  )
  ```

### Epic 2: TC-9006: trustify-ui
- **Issue type:** Epic (hierarchyLevel 1)
- **Parent:** TC-9006 (Feature)
- **Summary:** TC-9006: trustify-ui
- **Description:** Frontend implementation for the vulnerability remediation tracking dashboard. Includes the API client layer, React Query hooks, dashboard page with summary cards and progress chart, and filterable vulnerability table.
- **Tasks:** Task 4, Task 5, Task 6
- **Creation parameters:**
  ```
  jira.create_issue(
    projectKey="TC",
    issueTypeName="Epic",
    summary="TC-9006: trustify-ui",
    description="Frontend implementation for the vulnerability remediation tracking dashboard. Includes the API client layer, React Query hooks, dashboard page with summary cards and progress chart, and filterable vulnerability table.",
    parent="TC-9006",
    additional_fields={
      "labels": ["ai-generated-jira"],
      "priority": {"name": "Major"},
      "fixVersions": [{"name": "RHTPA 1.5.0"}]
    }
  )
  ```

## Incorporates Links

Links are created from the Feature to each **Epic** (not to individual Tasks):
- TC-9006 --Incorporates--> [Epic: TC-9006: trustify-backend]
- TC-9006 --Incorporates--> [Epic: TC-9006: trustify-ui]

Tasks inherit hierarchy through their Epic parent field.

## Task Creation Parameters

All tasks are created with the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

**Inheritance rationale:**
- **Priority:** "Major" — inherited from Feature TC-9006 (priority is set and not "Undefined")
- **fixVersions:** ["RHTPA 1.5.0"] — inherited from Feature TC-9006 (Feature has non-empty fixVersions and fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)

Each task's `parent` field is set to its assigned Epic key:
- Tasks 1, 2, 3, 7 → parent = [Epic: TC-9006: trustify-backend]
- Tasks 4, 5, 6 → parent = [Epic: TC-9006: trustify-ui]

## Task Summary

| # | Summary | Repository | Epic | Dependencies |
|---|---|---|---|---|
| 1 | Add remediation domain model and aggregation service | trustify-backend | TC-9006: trustify-backend | None |
| 2 | Add remediation REST API endpoints | trustify-backend | TC-9006: trustify-backend | Task 1 |
| 3 | Add remediation endpoint integration tests | trustify-backend | TC-9006: trustify-backend | Task 2 |
| 4 | Add remediation API client, types, and React Query hooks | trustify-ui | TC-9006: trustify-ui | Task 2 |
| 5 | Create remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui | Task 4 |
| 6 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui | Task 5 |
| 7 | Document remediation dashboard and aggregation endpoints | trustify-backend | TC-9006: trustify-backend | Tasks 1-6 |
