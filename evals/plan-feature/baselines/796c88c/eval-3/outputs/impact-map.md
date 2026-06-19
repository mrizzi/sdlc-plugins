# Impact Map: TC-9003 SBOM Comparison View

## Feature Summary

Add a side-by-side SBOM comparison view that lets users select two SBOM versions and see what changed: added/removed packages, new/resolved vulnerabilities, and license changes. Requires a new backend diffing endpoint and a frontend comparison UI built from Figma mockups.

## Workflow Mode

**Feature-branch workflow** — Both repositories use a shared `TC-9003` branch. Backend tasks are completed first, then frontend tasks. Bookend tasks (create-branch, merge-branch) manage the branch lifecycle.

## Repositories Impacted

| Repository | Role | Tasks |
|---|---|---|
| trustify-backend | REST API and diff computation | Tasks 1-5, 10 |
| trustify-ui | React frontend comparison page | Tasks 1, 6-10 |

## Task Dependency Graph

```
Task 1: Create feature branch (bookend)
├── Task 2: Backend comparison model
│   └── Task 3: Backend comparison service
│       └── Task 4: Backend comparison endpoint
│           ├── Task 5: Backend integration tests
│           └── Task 6: Frontend API types and client
│               └── Task 7: Frontend comparison hook
│                   └── Task 8: Frontend comparison page
│                       └── Task 9: Frontend MSW mocks and tests
│                           └── Task 10: Merge feature branch (bookend)
```

## Task Summary

| Task | Repository | Title | Target Branch | Dependencies |
|---|---|---|---|---|
| 1 | trustify-backend | Create feature branch | main | None |
| 2 | trustify-backend | Backend comparison model | TC-9003 | Task 1 |
| 3 | trustify-backend | Backend comparison service | TC-9003 | Task 2 |
| 4 | trustify-backend | Backend comparison endpoint | TC-9003 | Task 3 |
| 5 | trustify-backend | Backend integration tests | TC-9003 | Task 4 |
| 6 | trustify-ui | Frontend API types and client | TC-9003 | Tasks 1, 4 |
| 7 | trustify-ui | Frontend comparison hook | TC-9003 | Task 6 |
| 8 | trustify-ui | Frontend comparison page | TC-9003 | Tasks 6, 7 |
| 9 | trustify-ui | Frontend MSW mocks and tests | TC-9003 | Task 8 |
| 10 | trustify-backend | Merge feature branch | main | Tasks 5, 9 |

## Files Impacted

### trustify-backend

| File | Action | Task |
|---|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Create | 2 |
| `modules/fundamental/src/sbom/model/mod.rs` | Modify | 2 |
| `modules/fundamental/src/sbom/service/comparison.rs` | Create | 3 |
| `modules/fundamental/src/sbom/service/mod.rs` | Modify | 3 |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | Create | 4 |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Modify | 4 |
| `tests/api/sbom_compare.rs` | Create | 5 |

### trustify-ui

| File | Action | Task |
|---|---|---|
| `src/api/models.ts` | Modify | 6 |
| `src/api/rest.ts` | Modify | 6 |
| `src/hooks/useSbomComparison.ts` | Create | 7 |
| `src/pages/ComparisonPage/ComparisonPage.tsx` | Create | 8 |
| `src/pages/ComparisonPage/ComparisonPage.test.tsx` | Create | 8, 9 |
| `src/pages/ComparisonPage/components/DiffSection.tsx` | Create | 8 |
| `src/pages/ComparisonPage/components/SbomSelector.tsx` | Create | 8 |
| `src/routes.tsx` | Modify | 8 |
| `src/App.tsx` | Modify | 8 |
| `tests/mocks/handlers.ts` | Modify | 9 |
| `tests/mocks/fixtures/sbom-comparison.json` | Create | 9 |

## API Changes

| Endpoint | Method | Action | Task |
|---|---|---|---|
| `/api/v2/sbom/compare?left={id1}&right={id2}` | GET | NEW | 4 |

## Cross-Repository Dependencies

Frontend Task 6 (API types and client) depends on Backend Task 4 (comparison endpoint) for the finalized API contract. The JSON response shape defined by the backend `SbomComparison` struct must match the TypeScript `SbomComparison` interface exactly.

The feature-branch workflow ensures both repositories coordinate via the `TC-9003` branch. Backend tasks (2-5) complete first, establishing the API. Frontend tasks (6-9) follow, consuming the API.

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Large SBOM diffs (>1000 packages) may cause slow response times | Backend service uses batch queries and HashMaps for O(1) lookups; p95 target < 1s |
| Large diffs may cause browser freezing | Frontend uses virtualized lists for >100 changed packages |
| API contract mismatch between backend and frontend | TypeScript interfaces derived directly from Rust struct definitions; mock fixture validates shape |
| Merge conflicts from parallel development | Feature-branch workflow with sequential backend-then-frontend ordering minimizes conflicts |
