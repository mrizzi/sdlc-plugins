# TC-9003 — SBOM Comparison View: Implementation Plan Summary

## Task Breakdown

| # | Task | Repository | Target Branch | Dependencies |
|---|------|-----------|---------------|-------------|
| 1 | Create feature branch (backend) | trustify-backend | main | None |
| 2 | Comparison model types + service logic | trustify-backend | TC-9003 | Task 1 |
| 3 | Comparison REST endpoint | trustify-backend | TC-9003 | Task 2 |
| 4 | Merge feature branch (backend) | trustify-backend | main | Task 3 |
| 5 | Create feature branch (frontend) | trustify-ui | main | Task 4 |
| 6 | API types, client function, React Query hook | trustify-ui | TC-9003 | Task 5, Task 3 (cross-repo) |
| 7 | Comparison page UI (Figma) | trustify-ui | TC-9003 | Task 6 |
| 8 | Routing, SBOM selection, export, E2E tests | trustify-ui | TC-9003 | Task 7 |
| 9 | Merge feature branch (frontend) | trustify-ui | main | Task 8 |

## Repository Distribution
- **trustify-backend**: 4 tasks (Tasks 1-4) — model types, service logic, REST endpoint, feature-branch bookends
- **trustify-ui**: 5 tasks (Tasks 5-9) — API layer, comparison page UI, routing, export, feature-branch bookends

## Architecture Summary

### Backend
- New `SbomComparison` model types in `modules/fundamental/src/sbom/model/comparison.rs`
- New `SbomService::compare()` method in `modules/fundamental/src/sbom/service/compare.rs` computing on-the-fly diffs from existing package, advisory, and license data (no new DB tables)
- New `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/compare.rs`

### Frontend
- TypeScript interfaces and API client function in `src/api/models.ts` and `src/api/rest.ts`
- `useSbomComparison` React Query hook in `src/hooks/useSbomComparison.ts`
- Full comparison page at `src/pages/SbomComparePage/` with PatternFly 5 components per Figma design:
  - `CompareToolbar` with SBOM selectors (Select, typeahead), Compare button, Export dropdown
  - 6 `DiffSection` components (ExpandableSection + Table) with color-coded Badge counts
  - `CompareEmptyState` with CodeBranchIcon
  - Skeleton loading states
- SBOM list page enhanced with checkbox selection and "Compare selected" action
- Route registered at `/sbom/compare` with lazy loading
- Export functionality (JSON/CSV) for compliance documentation

### Cross-Repo Flow
Backend feature branch completes and merges first (Tasks 1-4), then frontend feature branch begins (Tasks 5-9). Task 6 has an explicit cross-repo dependency on Task 3 (backend endpoint).

## Workflow Mode
Feature-branch workflow with bookend tasks:
- Backend: Task 1 (create-branch) and Task 4 (merge-branch)
- Frontend: Task 5 (create-branch) and Task 9 (merge-branch)
- Intermediate tasks target branch `TC-9003`

## Inherited Fields
- **Priority**: Critical — inherited from feature TC-9003, included in all tasks via ## Jira Metadata
- **Fix Versions**: RHTPA 1.5.0 — inherited from feature TC-9003, included in all tasks via ## Jira Metadata

## Convention Enrichment
Both repositories have conventions applied per CONVENTIONS.md:
- **trustify-backend**: Error handling (Result<T, AppError>), module pattern (model/service/endpoints), endpoint registration, testing (integration tests with PostgreSQL)
- **trustify-ui**: Component library (PatternFly 5), page structure (directory per page), API layer (client/rest/hooks), state management (React Query), routing (React Router v6 lazy-loaded), testing (Vitest + RTL + Playwright + MSW), naming conventions (PascalCase components, camelCase hooks)

All convention citations include applicability rationales per convention-applicability-rules.md.
