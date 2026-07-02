## TC-9003: SBOM Comparison View -- Implementation Plan

### Architecture Summary

This feature adds a side-by-side SBOM comparison capability across two repositories. The **trustify-backend** provides a new `GET /api/v2/sbom/compare` endpoint that computes a structured diff between two SBOMs on-the-fly (no new database tables), covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The **trustify-ui** provides a Figma-driven comparison page at `/sbom/compare` with PatternFly components (Select dropdowns, ExpandableSection diffs, composable Tables, Badge counts), plus a "Compare selected" action on the existing SBOM list page.

**Workflow mode**: Feature branch (`TC-9003`) -- tightly coupled frontend/backend requiring the new backend endpoint before the frontend can integrate.

### Task Breakdown

| # | Task | Repository | Dependencies |
|---|---|---|---|
| 1 | Create feature branch (backend) | trustify-backend | -- |
| 2 | Create feature branch (frontend) | trustify-ui | -- |
| 3 | SBOM comparison model types and diff service | trustify-backend | Task 1 |
| 4 | SBOM comparison endpoint and integration tests | trustify-backend | Task 1, Task 3 |
| 5 | API types, client function, and React Query hook | trustify-ui | Task 2, Task 4 |
| 6 | SBOM comparison page UI (Figma design) | trustify-ui | Task 2, Task 5 |
| 7 | Route registration and compare action from SBOM list | trustify-ui | Task 2, Task 6 |
| 8 | Merge feature branch (backend) | trustify-backend | Task 3, Task 4 |
| 9 | Merge feature branch (frontend) | trustify-ui | Task 5, Task 6, Task 7 |

### Cross-repo Dependencies

- Task 5 (frontend API types/hook) depends on Task 4 (backend endpoint) -- the frontend data layer requires the backend comparison endpoint to exist.
- Backend tasks (3-4) have lower task numbers than all frontend tasks (5-7), ensuring the API contract is established before UI integration begins.

### Convention Coverage

**trustify-backend (CONVENTIONS.md)**:
- Error Handling: applied to Tasks 3, 4 (all `.rs` files wrap errors with `.context()`)
- Test Patterns: applied to Task 4 (integration tests use real PostgreSQL, `assert_eq!` pattern)
- Migration Patterns: excluded (no migration files modified)

**trustify-ui (CONVENTIONS.md)**:
- Component naming (PascalCase): applied to Tasks 6, 7 (`.tsx` components)
- Mutation pattern (React Query): applied to Task 5 (`.ts` hook with query key management)
- MSW mocking: applied to Task 6 (`.test.tsx` files use MSW handlers)

### Field Propagation

- Priority: Critical (propagated to all tasks)
- Fix Versions: RHTPA 1.5.0 (propagated to all tasks)
