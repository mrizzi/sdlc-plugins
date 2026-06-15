# Impact Map: TC-9003 — SBOM Comparison View

## Workflow Mode

**Feature-branch** — Backend API must exist before frontend can consume it, and merging the backend comparison endpoint to main without the corresponding UI would expose an unused API surface. Cross-repo API dependencies require coordinated delivery via a feature branch.

## Task Dependency Graph

```
TC-9003-1 (create-branch, backend)
    |
    v
TC-9003-2 (backend: comparison models + diff service)
    |
    v
TC-9003-3 (backend: comparison endpoint + integration tests)
    |
    v
TC-9003-4 (frontend: API types + client + hook)
    |
    v
TC-9003-5 (frontend: comparison page + diff sections UI)
    |
    v
TC-9003-6 (frontend: SBOM list page selection + routing)
    |
    v
TC-9003-7 (merge-branch, backend)
```

## Repositories Impacted

| Repository | Tasks | Nature of Changes |
|---|---|---|
| trustify-backend | TC-9003-1, TC-9003-2, TC-9003-3, TC-9003-7 | New comparison diff service, endpoint, models, integration tests |
| trustify-ui | TC-9003-4, TC-9003-5, TC-9003-6 | API types, React Query hook, comparison page UI, SBOM list selection UX |

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Large SBOM diffs (>2000 packages) cause slow response times | NFR requires p95 < 1s; service must stream/compute diff efficiently; frontend uses virtualized lists |
| No new database tables — diff computed on-the-fly | Relies on existing package/advisory data being queryable efficiently; may need query optimization |
| Frontend depends on backend API contract | API types defined in task 4 must match backend response shape from task 3; feature branch enables coordinated validation |

## Feature Branch Lifecycle

1. **TC-9003-1**: Create feature branch `TC-9003` in `trustify-backend`
2. **TC-9003-2 through TC-9003-6**: Implementation tasks targeting `TC-9003` branch
3. **TC-9003-7**: Merge feature branch to main after all tasks complete
