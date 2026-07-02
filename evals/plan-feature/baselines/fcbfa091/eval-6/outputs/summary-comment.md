# Plan Summary — TC-9006: Add vulnerability remediation tracking dashboard

## Overview
Implementation plan for a vulnerability remediation tracking dashboard spanning two repositories. The backend provides aggregation endpoints for remediation status by severity and by product, while the frontend renders a dashboard page with summary cards, a progress chart, and a filterable vulnerability table.

## Epic Structure
Using **by-repository** Epic grouping strategy:

| Epic | Repository | Tasks | Description |
|------|-----------|-------|-------------|
| TC-9006: trustify-backend | trustify-backend | 4 tasks (1-4) | Remediation module: models, service, endpoints, integration tests |
| TC-9006: trustify-ui | trustify-ui | 5 tasks (5-9) | Dashboard UI: API layer, page components, routing, tests |

## Task Summary

### Backend (TC-9006: trustify-backend)
1. **Task 1 — Remediation module models**: Create `RemediationSummary`, `SeverityBreakdown`, and `ProductRemediation` structs in a new `modules/remediation/` module
2. **Task 2 — Remediation service**: Implement aggregation queries against existing SBOM/advisory data; no new database tables
3. **Task 3 — Remediation endpoints**: Create `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints; register routes in server
4. **Task 4 — Backend integration tests**: Add integration tests in `tests/api/remediation.rs` covering both endpoints

### Frontend (TC-9006: trustify-ui)
5. **Task 5 — API layer**: Add TypeScript interfaces, REST client functions, and React Query hooks for remediation endpoints
6. **Task 6 — Dashboard page**: Build `RemediationDashboardPage` with summary cards (open/in-progress/resolved by severity) and progress chart
7. **Task 7 — Vulnerability table**: Build filterable, paginated vulnerability table with severity/product/status filters
8. **Task 8 — Routing and navigation**: Register `/remediation` route and add sidebar navigation entry
9. **Task 9 — Frontend tests**: Add unit tests, MSW handlers, mock fixtures, and Playwright E2E test

## Inherited Fields
All tasks inherit from TC-9006:
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0
- **Labels**: ai-generated-jira

## Dependency Chain
```
Task 1 (models) → Task 2 (service) → Task 3 (endpoints) → Task 4 (backend tests)
                                              ↓
Task 5 (API layer) → Task 6 (dashboard page) → Task 7 (vulnerability table) → Task 9 (frontend tests)
                                              → Task 8 (routing/navigation) → Task 9 (frontend tests)
```

## Key Design Decisions
- **No new database tables**: Aggregations computed from existing `sbom`, `advisory`, and `sbom_advisory` entities
- **Performance**: Summary endpoint targets p95 < 500ms for up to 10,000 vulnerabilities
- **Non-MVP deferred**: CSV export of remediation reports is excluded from this plan
- **Code reuse**: Leverages existing `SeverityBadge`, `FilterToolbar`, `EmptyStateCard`, `LoadingSpinner` components on the frontend; follows established module pattern (`model/ + service/ + endpoints/`) on the backend

## API Surface
| Method | Endpoint | Response Type |
|--------|----------|---------------|
| GET | `/api/v2/remediation/summary` | `RemediationSummary` |
| GET | `/api/v2/remediation/by-product` | `PaginatedResults<ProductRemediation>` |
