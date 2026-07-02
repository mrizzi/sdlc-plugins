# Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Epic Grouping Strategy
by-repository

## Workflow Mode
direct-to-main

## Repositories Impacted

### trustify-backend
**Epic**: TC-9006: trustify-backend

| Area | Files | Change Type | Description |
|------|-------|-------------|-------------|
| Module structure | `modules/remediation/Cargo.toml` | Create | New crate manifest for the remediation module |
| Module structure | `modules/remediation/src/lib.rs` | Create | Module root re-exporting model, service, and endpoints |
| Models | `modules/remediation/src/model/mod.rs` | Create | Model submodule root |
| Models | `modules/remediation/src/model/summary.rs` | Create | `RemediationSummary` and `SeverityBreakdown` structs for severity-by-status aggregation |
| Models | `modules/remediation/src/model/by_product.rs` | Create | `ProductRemediation` struct for per-product remediation breakdown |
| Service | `modules/remediation/src/service/mod.rs` | Create | `RemediationService` with `get_summary()` and `get_by_product()` aggregation methods |
| Endpoints | `modules/remediation/src/endpoints/mod.rs` | Create | Route registration for `/api/v2/remediation` namespace |
| Endpoints | `modules/remediation/src/endpoints/summary.rs` | Create | Handler for `GET /api/v2/remediation/summary` |
| Endpoints | `modules/remediation/src/endpoints/by_product.rs` | Create | Handler for `GET /api/v2/remediation/by-product` with pagination |
| Server | `server/src/main.rs` | Modify | Mount remediation module routes |
| Workspace | `Cargo.toml` | Modify | Add `trustify-remediation` workspace member |
| Tests | `tests/api/remediation.rs` | Create | Integration tests for remediation endpoints |
| Tests | `tests/Cargo.toml` | Modify | Add dev-dependency for remediation module |

**API Changes**:
- `GET /api/v2/remediation/summary` — NEW: Returns aggregated vulnerability counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- `GET /api/v2/remediation/by-product` — NEW: Returns paginated per-product remediation breakdown with total/open/in-progress/resolved counts

**Database Changes**: None — aggregations computed from existing `sbom`, `advisory`, `sbom_advisory` tables

### trustify-ui
**Epic**: TC-9006: trustify-ui

| Area | Files | Change Type | Description |
|------|-------|-------------|-------------|
| API types | `src/api/models.ts` | Modify | Add `RemediationSummary`, `SeverityBreakdown`, `ProductRemediation` interfaces |
| API client | `src/api/rest.ts` | Modify | Add `fetchRemediationSummary()` and `fetchRemediationByProduct()` functions |
| Hooks | `src/hooks/useRemediationSummary.ts` | Create | React Query hook for remediation summary data |
| Hooks | `src/hooks/useRemediationByProduct.ts` | Create | React Query hook for per-product remediation data |
| Pages | `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` | Create | Main dashboard page with summary cards and chart layout |
| Components | `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` | Create | Summary cards showing open/in-progress/resolved counts by severity |
| Components | `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` | Create | Progress chart for remediation trend visualization |
| Components | `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` | Create | Filterable, paginated vulnerability table with severity/product/status filters |
| Routing | `src/routes.tsx` | Modify | Add `/remediation` route with lazy-loaded page component |
| Navigation | `src/App.tsx` | Modify | Add "Remediation" navigation menu entry |
| Tests | `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` | Create | Unit tests for dashboard page |
| Test mocks | `tests/mocks/handlers.ts` | Modify | Add MSW handlers for remediation API endpoints |
| Test fixtures | `tests/mocks/fixtures/remediation-summary.json` | Create | Mock remediation summary data |
| Test fixtures | `tests/mocks/fixtures/remediation-by-product.json` | Create | Mock per-product remediation data |
| E2E tests | `tests/e2e/remediation-dashboard.spec.ts` | Create | Playwright E2E test for dashboard navigation and filter interactions |

**Reused Components**:
- `src/components/SeverityBadge.tsx` — Severity level badges in summary cards and table
- `src/components/FilterToolbar.tsx` — Filter toolbar for vulnerability table
- `src/components/EmptyStateCard.tsx` — Empty state when no data
- `src/components/LoadingSpinner.tsx` — Loading indicator
- `src/utils/severityUtils.ts` — Severity ordering and color mapping
- `src/utils/formatDate.ts` — Date formatting for table columns

## Cross-Repository Dependencies
- Frontend tasks (task-5 through task-9) depend on backend API endpoints (task-3) being defined
- No shared libraries or packages between repositories
- API contract is defined by the backend response types mirrored as TypeScript interfaces

## Non-Functional Considerations
- Summary endpoint p95 response time < 500ms
- Dashboard must handle up to 10,000 tracked vulnerabilities
- No new database tables — aggregations computed from existing data
- By-product endpoint requires pagination for large portfolios (>50 products)

## Out of Scope (Non-MVP)
- CSV export of remediation report — marked as non-MVP in requirements
