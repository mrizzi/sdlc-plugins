# Repository Impact Map

**Feature:** TC-9006 — Add vulnerability remediation tracking dashboard
**Workflow Mode:** direct-to-main

## Epic Grouping (by-repository)

### Epic 1: TC-9006: trustify-backend
- Issue type: Epic (level 1), parent: TC-9006
- Tasks 1-3 assigned to this Epic

### Epic 2: TC-9006: trustify-ui
- Issue type: Epic (level 1), parent: TC-9006
- Tasks 4-6 assigned to this Epic

## Incorporates Links
- Feature TC-9006 → Epic "TC-9006: trustify-backend" (Incorporates)
- Feature TC-9006 → Epic "TC-9006: trustify-ui" (Incorporates)
- Note: links go from Feature to Epics, NOT from Feature to individual Tasks

## Field Inheritance
- Priority: Major (propagated to all Epics and Tasks)
- Fix Versions: RHTPA 1.5.0 (propagated to all Epics and Tasks, fixVersion scope defaults to 'both')

## trustify-backend
changes:
  - Add remediation summary aggregation endpoint GET /api/v2/remediation/summary
  - Add per-product breakdown endpoint GET /api/v2/remediation/by-product
  - Add integration tests for new endpoints

## trustify-ui
changes:
  - Add API types, client functions, and React Query hooks for remediation endpoints
  - Add RemediationDashboard page with summary cards, progress chart, and filterable table
  - Add MSW mocks and component tests
