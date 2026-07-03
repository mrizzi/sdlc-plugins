# Impact Map: TC-9006 -- Add vulnerability remediation tracking dashboard

## Feature
Add a vulnerability remediation tracking dashboard that shows the progress of fixing known vulnerabilities across all ingested SBOMs. The backend provides aggregation endpoints for remediation status by severity and by product, while the frontend renders a dashboard page with summary cards, a progress chart, and a filterable table of outstanding vulnerabilities.

## Repositories Affected

| Repository | Role |
|---|---|
| trustify-backend | Backend -- remediation aggregation models, service methods, REST endpoints, integration tests, documentation |
| trustify-ui | Frontend -- API types, client functions, React Query hooks, dashboard page with summary cards, progress chart, and filterable table |

## Epic Hierarchy

**Grouping strategy**: by-repository (from CLAUDE.md Hierarchy Configuration)
**Issue type**: Epic (level 1)

| Epic Summary | Issue Type | Parent | Repositories | Tasks |
|---|---|---|---|---|
| TC-9006: trustify-backend | Epic (level 1) | TC-9006 | trustify-backend | Tasks 1, 2, 3, 6 |
| TC-9006: trustify-ui | Epic (level 1) | TC-9006 | trustify-ui | Tasks 4, 5 |

**Epic creation parameters:**
- Issue type: Epic (hierarchyLevel 1)
- Parent: TC-9006 (Feature)
- Labels: ["ai-generated-jira"]
- Priority: Major (inherited from TC-9006)
- Fix Versions: RHTPA 1.5.0 (inherited from TC-9006)

**Jira links**: Feature TC-9006 "Incorporates" each Epic (NOT individual Tasks).
- TC-9006 Incorporates Epic "TC-9006: trustify-backend"
- TC-9006 Incorporates Epic "TC-9006: trustify-ui"

## Specific Changes Needed

### trustify-backend

#### Model Layer
- Create `RemediationSummary` struct with severity x status counts: (Critical/High/Medium/Low) x (Open/In Progress/Resolved), plus totals
- Create `ProductRemediation` struct with per-product breakdown: product name/ID, total, open, in_progress, resolved counts
- Register new model modules in the remediation domain module

#### Service Layer
- Add `RemediationService` with `summary()` method to compute aggregated severity x status counts from existing vulnerability and SBOM relationship data
- Add `by_product()` method to compute per-product remediation breakdown with pagination
- Aggregation queries use existing entity relationships (no new database tables per NFR)

#### Endpoint Layer
- Create `GET /api/v2/remediation/summary` handler returning `RemediationSummary`
- Create `GET /api/v2/remediation/by-product` handler returning paginated `ProductRemediation` list
- Register routes in a new remediation endpoints module
- Mount routes in `server/src/main.rs`
- Apply caching for p95 < 500ms target

#### Integration Tests
- Create test suite in `tests/api/remediation.rs` covering both endpoints: valid responses, empty data, pagination, error cases

#### Documentation
- New Content: API endpoint reference for remediation endpoints and user guide for the dashboard

### trustify-ui

#### API Layer
- Add TypeScript interfaces for `RemediationSummary` and `ProductRemediation` in `src/api/models.ts`
- Add API client functions `fetchRemediationSummary()` and `fetchRemediationByProduct()` in `src/api/rest.ts`
- Create React Query hooks `useRemediationSummary` and `useRemediationByProduct` in `src/hooks/`

#### Dashboard Page
- Create `RemediationDashboardPage` at `/remediation` route
- Summary cards showing total Open, In Progress, and Resolved counts
- Progress chart showing remediation trend over time
- Filterable vulnerability table with severity, product, and status filters
- Route entry and navigation link for `/remediation`

## Excluded Requirements

| Requirement | Reason |
|---|---|
| Export remediation report as CSV | Non-MVP requirement -- deferred to a follow-up feature. The feature description marks this as not MVP. |

## Workflow Mode Decision

**Mode**: direct-to-main

**Rationale**: The backend changes are additive (new endpoints, no modifications to existing API contracts) and the frontend depends on the backend sequentially. No atomicity indicators are present:
- No coordinated schema migrations (no new database tables)
- No breaking API changes (all endpoints are new additions)
- No cross-cutting refactors (new domain module, no existing code reorganization)
- Components can be delivered sequentially (backend first, then frontend) without leaving main in a broken state

Each task PR can land on `main` independently.
