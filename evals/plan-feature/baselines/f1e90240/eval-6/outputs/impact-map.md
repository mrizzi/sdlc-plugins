# Impact Map: TC-9006 — Add vulnerability remediation tracking dashboard

## Workflow Mode

**direct-to-main** — All tasks target `main` as their base branch. The feature spans two repositories (trustify-backend, trustify-ui), making feature-branch mode impractical since feature branches would need coordination across separate repos.

## Epic Hierarchy

### Issue Type Discovery

A level-1 issue type named **Epic** is available in the project (hierarchyLevel: 1). The Feature issue type is at hierarchyLevel 2. Because a level-1 type exists, the plan uses the Feature -> Epic -> Task three-level hierarchy.

### Epic Grouping Strategy

**by-repository** — One Epic per repository, as configured in the project's Hierarchy Configuration.

### Epic Creation Parameters

| Epic | Issue Type | Parent | Summary |
|---|---|---|---|
| Epic 1 | Epic (level-1 issue type) | TC-9006 (parent feature) | TC-9006: trustify-backend |
| Epic 2 | Epic (level-1 issue type) | TC-9006 (parent feature) | TC-9006: trustify-ui |

Both Epics are created with:
- **Issue type**: `Epic` (the level-1 issue type name discovered from the Jira project)
- **Parent**: `TC-9006` (the feature issue key, setting the parent link so each Epic is a child of the Feature)
- **Labels**: `["ai-generated-jira"]`
- **Priority**: Major (inherited from Feature TC-9006)
- **Fix Versions**: RHTPA 1.5.0 (inherited from Feature TC-9006)

## Incorporates Links

The Feature issue TC-9006 links to each Epic via **Incorporates** links. Feature does NOT link directly to individual Tasks.

| Source | Link Type | Target |
|---|---|---|
| TC-9006 (Feature) | Incorporates | Epic: TC-9006: trustify-backend |
| TC-9006 (Feature) | Incorporates | Epic: TC-9006: trustify-ui |

**Rationale**: With Epic hierarchy enabled, the Feature-to-Epic Incorporates links provide the structural connection. Individual Tasks are children of their respective Epics, so transitive traceability is maintained without direct Feature-to-Task links.

## Epic-to-Task Assignments

### Epic: TC-9006: trustify-backend

| Task # | Slug | Summary |
|---|---|---|
| Task 1 | task-1-remediation-module-summary-endpoint | Create remediation module with model types, aggregation service, and summary endpoint |
| Task 2 | task-2-by-product-endpoint-integration-tests | Add by-product remediation endpoint and integration tests |

### Epic: TC-9006: trustify-ui

| Task # | Slug | Summary |
|---|---|---|
| Task 3 | task-3-api-types-hooks-remediation | Add API model types, REST client functions, and React Query hooks for remediation endpoints |
| Task 4 | task-4-remediation-dashboard-page | Create RemediationDashboardPage with summary cards and progress chart |
| Task 5 | task-5-filterable-vulnerability-table | Add filterable vulnerability table component to remediation dashboard |
| Task 6 | task-6-documentation-remediation-dashboard | Documentation for remediation dashboard and API endpoints |

Tasks are created with their parent set to the respective Epic issue key (not directly to the Feature).

## Task Dependency Graph

```
Task 1 (backend: remediation module + summary endpoint)
  |
  v
Task 2 (backend: by-product endpoint + integration tests)
  |
  +-------+-------+
  v               v
Task 3 (frontend: API types + hooks)
  |
  +-------+-------+
  v               v
Task 4 (frontend: dashboard page)    Task 5 (frontend: vulnerability table)
  |                                     |
  +----> depends on Task 4 <-----------+
  |
  v
Task 6 (documentation)
```

- Tasks 1-2 are backend tasks with lower numbers, executed before frontend tasks
- Task 3 (frontend API layer) depends on Tasks 1-2 (backend endpoints must exist)
- Tasks 4-5 (frontend UI) depend on Task 3 (hooks and types must exist)
- Task 5 integrates into the page created by Task 4
- Task 6 (documentation) depends on all implementation tasks being complete

## Repository Impact Summary

### trustify-backend

| Area | Files |
|---|---|
| New module | `modules/fundamental/src/remediation/` (mod.rs, model/, service/, endpoints/) |
| Route mounting | `server/src/main.rs` |
| Integration tests | `tests/api/remediation.rs` |

### trustify-ui

| Area | Files |
|---|---|
| API types | `src/api/models.ts`, `src/api/rest.ts` |
| Hooks | `src/hooks/useRemediationSummary.ts`, `src/hooks/useRemediationByProduct.ts` |
| Dashboard page | `src/pages/RemediationDashboardPage/` (main component, test, components/) |
| Routing | `src/routes.tsx`, `src/App.tsx` |
| Test mocks | `tests/mocks/handlers.ts`, `tests/mocks/fixtures/` |

## Non-Functional Requirements Mapping

| NFR | Addressed By |
|---|---|
| Summary endpoint p95 < 500ms | Task 1 — efficient aggregation queries, caching middleware |
| Handle 10,000 vulnerabilities | Task 1 (backend aggregation), Task 5 (frontend pagination) |
| No new database tables | Task 1, Task 2 — aggregate from existing entity tables |
| >50 products pagination | Task 2 — PaginatedResults response wrapper |

## MVP Scope

All 6 tasks cover MVP requirements. The non-MVP requirement (CSV export) is intentionally excluded from this plan and can be addressed in a follow-up feature.

## Field Inheritance

- **Priority**: Major — inherited from Feature TC-9006, propagated to both Epics and all Tasks
- **Fix Versions**: RHTPA 1.5.0 — inherited from Feature TC-9006, propagated to both Epics and all Tasks
