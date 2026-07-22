# Plan Summary: TC-9006 — Add vulnerability remediation tracking dashboard

## Inherited Field Propagation

Feature TC-9006 has the following fields that are propagated to child issues:

| Field | Value | Propagated To |
|---|---|---|
| Priority | Major | Epics and Tasks |
| Fix Versions | RHTPA 1.5.0 | Epics and Tasks |

### Propagation Details

- **Priority: Major** — inherited from Feature TC-9006. Set on both Epics (TC-9006: trustify-backend, TC-9006: trustify-ui) and all 6 Tasks at creation time.
- **Fix Versions: RHTPA 1.5.0** — inherited from Feature TC-9006. Set on both Epics and all 6 Tasks at creation time.

Both fields are inherited by **Epics AND Tasks**. The hierarchy is:
- Feature TC-9006 (Priority: Major, Fix Versions: RHTPA 1.5.0)
  - Epic: TC-9006: trustify-backend (Priority: Major, Fix Versions: RHTPA 1.5.0)
    - Task 1: Create remediation module with model types, aggregation service, and summary endpoint (Priority: Major, Fix Versions: RHTPA 1.5.0)
    - Task 2: Add by-product remediation endpoint and integration tests (Priority: Major, Fix Versions: RHTPA 1.5.0)
  - Epic: TC-9006: trustify-ui (Priority: Major, Fix Versions: RHTPA 1.5.0)
    - Task 3: Add API model types, REST client functions, and React Query hooks (Priority: Major, Fix Versions: RHTPA 1.5.0)
    - Task 4: Create RemediationDashboardPage with summary cards and progress chart (Priority: Major, Fix Versions: RHTPA 1.5.0)
    - Task 5: Add filterable vulnerability table component to remediation dashboard (Priority: Major, Fix Versions: RHTPA 1.5.0)
    - Task 6: Documentation for remediation dashboard and API endpoints (Priority: Major, Fix Versions: RHTPA 1.5.0)

## Epic Hierarchy Summary

| Epic | Repository | Child Tasks |
|---|---|---|
| TC-9006: trustify-backend | trustify-backend | Tasks 1, 2 |
| TC-9006: trustify-ui | trustify-ui | Tasks 3, 4, 5, 6 |

Epics are created with the `Epic` issue type (level-1) and parent set to TC-9006. Incorporates links connect Feature TC-9006 to each Epic (not to individual Tasks).

## Plan Statistics

- **Total tasks**: 6
- **Backend tasks**: 2 (trustify-backend)
- **Frontend tasks**: 4 (trustify-ui, including 1 documentation task)
- **Epics created**: 2 (one per repository)
- **Workflow mode**: direct-to-main
- **Target branch**: main (all tasks)
- **MVP scope**: All 6 tasks cover MVP requirements; CSV export (non-MVP) deferred
