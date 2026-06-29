# Impact Map: TC-9003 — SBOM Comparison View

## Goal
Reduce SBOM comparison time from ~15 minutes (manual) to <30 seconds (automated diff) and provide exportable diff reports for compliance documentation.

## Actors
- **Security analysts** — comparing SBOM versions after dependency updates to understand what changed
- **Compliance officers** — documenting changes between releases for audit trails

## Impacts
- Security analysts can quickly identify added/removed packages, version changes, and new/resolved vulnerabilities between two SBOM versions
- Compliance officers can export structured diff reports (JSON/CSV) without manual data collection
- Teams can share comparison URLs for collaborative review

## Deliverables

### Backend (trustify-backend)

| Task | Title | What it delivers |
|------|-------|-----------------|
| Task 1 | Create feature branch | Isolated `TC-9003` branch for backend work |
| Task 2 | Comparison model + service | `SbomComparison` model types and `SbomService::compare()` method that computes on-the-fly diffs using existing package, advisory, and license data |
| Task 3 | Comparison REST endpoint | `GET /api/v2/sbom/compare?left={id1}&right={id2}` returning structured diff JSON with proper validation and error handling |
| Task 4 | Merge feature branch | PR to merge all backend comparison work into main |

### Frontend (trustify-ui)

| Task | Title | What it delivers |
|------|-------|-----------------|
| Task 5 | Create feature branch | Isolated `TC-9003` branch for frontend work |
| Task 6 | API types + client + hook | TypeScript interfaces for comparison response, Axios client function, and `useSbomComparison` React Query hook |
| Task 7 | Comparison page UI | Full comparison page with SBOM selectors, collapsible diff sections (6 categories), empty/loading states — all per Figma design using PatternFly 5 components |
| Task 8 | Routing + selection + export | Route registration, SBOM list page checkbox selection with "Compare selected" action, JSON/CSV export, MSW mocks, and E2E tests |
| Task 9 | Merge feature branch | PR to merge all frontend comparison work into main |

## Architecture Diagram

```
                    trustify-backend                         trustify-ui
                ┌─────────────────────┐              ┌───────────────────────┐
                │  GET /api/v2/sbom/  │              │  SbomListPage         │
                │  compare?left&right │◄─────────────│  (checkbox selection) │
                │                     │   HTTP GET   │                       │
                │  SbomService::      │              │  SbomComparePage      │
                │    compare()        │              │  ├─ CompareToolbar    │
                │                     │              │  ├─ DiffSection (x6)  │
                │  SbomComparison     │              │  ├─ CompareEmptyState │
                │  (model types)      │              │  └─ useExportComparison│
                └─────────────────────┘              └───────────────────────┘
                         │                                      │
                    Uses existing:                         Uses existing:
                    - PackageService                       - useSboms hook
                    - AdvisoryService                      - SeverityBadge
                    - sbom_package entity                  - PatternFly 5
                    - sbom_advisory entity
                    - package_license entity
```

## Cross-Repository Dependencies

```
Task 1 (backend create-branch)
  └─► Task 2 (backend model + service)
       └─► Task 3 (backend endpoint)
            └─► Task 4 (backend merge)
                 └─► Task 5 (frontend create-branch)
                      └─► Task 6 (frontend API types + hooks)
                           └─► Task 7 (frontend comparison page)
                                └─► Task 8 (frontend routing + export)
                                     └─► Task 9 (frontend merge)
```

Backend tasks (1-4) must complete before frontend tasks (5-9) begin, as the frontend depends on the backend comparison endpoint.

## Non-Functional Constraints
- **Performance**: p95 < 1s for SBOMs with up to 2000 packages each
- **No new DB tables**: Diff computed on-the-fly from existing data
- **Virtualization**: Frontend uses virtualized lists for >100 changed packages
- **URL shareability**: Comparison URLs encode both SBOM IDs for bookmarking

## MVP vs Post-MVP
- **MVP**: Comparison endpoint, comparison page UI, URL shareability, critical vulnerability highlighting
- **Post-MVP**: Export as JSON/CSV (included in Task 8 but marked non-MVP in requirements)
