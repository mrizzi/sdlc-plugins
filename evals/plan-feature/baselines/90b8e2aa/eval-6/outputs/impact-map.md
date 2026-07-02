# Repository Impact Map — TC-9006

## Feature: Add vulnerability remediation tracking dashboard

```
trustify-backend:
  changes:
    - Add remediation module with aggregation models (RemediationSummary, ProductRemediation)
    - Add RemediationService with queries to compute severity x status aggregation from existing advisory/SBOM data
    - Add GET /api/v2/remediation/summary endpoint returning aggregated counts by severity and status
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
    - Register remediation module routes in server/main.rs
    - Add integration tests for both remediation endpoints

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types
    - Add API client functions for remediation summary and by-product endpoints
    - Add React Query hooks for remediation data fetching
    - Add RemediationDashboardPage with summary cards, progress chart, and filterable vulnerability table
    - Register /remediation route and add navigation link
    - Add unit tests, MSW mock handlers, and E2E tests for the remediation dashboard
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **Coordinated schema migrations** — No. The feature explicitly requires no new database tables; aggregations are computed from existing data.
2. **Breaking API changes** — No. Both backend endpoints are entirely new additions (`/api/v2/remediation/summary` and `/api/v2/remediation/by-product`). No existing endpoints are modified.
3. **Cross-cutting refactors** — No. All changes are additive — a new backend module and a new frontend page.
4. **Tightly coupled feature components** — No. The backend endpoints can land on `main` independently and function as valid API endpoints. The frontend page can land after the backend without leaving `main` in a broken state, provided tasks are ordered (backend first).

Since no atomicity constraint is identified, `direct-to-main` mode applies. All tasks target `main`.

## Epic Grouping

**Strategy:** `by-repository` (from Hierarchy Configuration)

| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9006: trustify-backend | Tasks 1, 2, 3 |
| Epic 2 | TC-9006: trustify-ui | Tasks 4, 5, 6 |

## Field Inheritance

- **Priority:** Major (inherited from Feature TC-9006)
- **fixVersions:** RHTPA 1.5.0 (inherited from Feature TC-9006; no `fixVersion scope` override in Jira Field Defaults — defaulting to "both", so propagated to tasks)
