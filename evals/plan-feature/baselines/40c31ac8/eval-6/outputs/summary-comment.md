## Implementation Plan: TC-9006 — Add vulnerability remediation tracking dashboard

### Epics Created

| Epic | Issue Type | Parent | Repository |
|---|---|---|---|
| TC-9006: trustify-backend | Epic (level-1) | TC-9006 | trustify-backend |
| TC-9006: trustify-ui | Epic (level-1) | TC-9006 | trustify-ui |

Incorporates links created from Feature TC-9006 to each Epic (not to individual tasks).

### Tasks Created

| Task | Summary | Repository | Parent Epic |
|---|---|---|---|
| Task 1 | Add remediation summary model and aggregation service | trustify-backend | TC-9006: trustify-backend |
| Task 2 | Add remediation REST endpoints and register routes | trustify-backend | TC-9006: trustify-backend |
| Task 3 | Add remediation endpoint integration tests | trustify-backend | TC-9006: trustify-backend |
| Task 4 | Add remediation API types, client functions, and React Query hooks | trustify-ui | TC-9006: trustify-ui |
| Task 5 | Add remediation dashboard page with summary cards, progress chart, and filterable table | trustify-ui | TC-9006: trustify-ui |
| Task 6 | Add frontend tests for remediation dashboard | trustify-ui | TC-9006: trustify-ui |

### Repositories Affected

- **trustify-backend** — 3 tasks: remediation model and service, REST endpoints, and integration tests
- **trustify-ui** — 3 tasks: API client layer, dashboard page with summary cards and filterable table, and frontend tests

### Architecture Summary

**Backend**: New model and service methods added to the existing advisory module provide two aggregation endpoints:
- `GET /api/v2/remediation/summary` — aggregated counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — per-product remediation breakdown with pagination

Aggregations are computed from existing vulnerability and SBOM relationship data via SQL GROUP BY queries (no new database tables). The implementation follows the established module pattern.

**Frontend**: A new `RemediationDashboard` page at `/remediation` displays:
- Summary cards with Open, In Progress, and Resolved counts broken down by severity
- A progress chart showing remediation status by severity
- A filterable, sortable, paginated vulnerability table with severity, product, and status filters

The frontend uses React Query hooks for data fetching and PatternFly 5 components for the UI.

### Field Propagation

- Priority: Major (propagated to all Epics and tasks)
- Fix Versions: RHTPA 1.5.0 (propagated to all Epics and tasks)
- Labels: ai-generated-jira (on all tasks)

### Hierarchy Links

- Feature TC-9006 --Incorporates--> Epic "TC-9006: trustify-backend"
- Feature TC-9006 --Incorporates--> Epic "TC-9006: trustify-ui"

### Dependency Order

Backend tasks (1-3) are numbered before frontend tasks (4-6) to reflect the dependency: frontend API client and hooks (Task 4) depend on backend endpoint definitions (Task 2).
