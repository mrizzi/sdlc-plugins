# Task 8: Register comparison route and add frontend tests

- **Jira parent**: TC-9003
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0
- **Dependencies**: Task 7

## Repository

trustify-ui

## Target Branch

TC-9003

## Description

Register the SBOM comparison page in the application route configuration with lazy loading. Add MSW mock handlers and test fixtures for the comparison API endpoint. Write unit tests for the comparison page and an E2E test for the full comparison workflow.

## Files to Create

- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- Unit tests using Vitest + React Testing Library
- `tests/mocks/fixtures/sbom-comparison.json` -- Mock comparison API response fixture
- `tests/e2e/sbom-compare.spec.ts` -- Playwright E2E test for the comparison workflow

## Files to Modify

- `src/routes.tsx` -- Add lazy-loaded route for `/sbom/compare` pointing to `SbomComparePage`
- `tests/mocks/handlers.ts` -- Add MSW handler for `GET /api/v2/sbom/compare`

## Acceptance Criteria

- [ ] Route `/sbom/compare` is registered in `src/routes.tsx` with lazy loading via `React.lazy()`
- [ ] Navigating to `/sbom/compare` renders the `SbomComparePage` component
- [ ] MSW handler intercepts `GET /api/v2/sbom/compare` and returns the fixture data
- [ ] Unit tests cover: empty state rendering, loading state, populated diff sections, error state
- [ ] E2E test: navigates to comparison page, selects two SBOMs, clicks Compare, verifies diff sections appear
- [ ] All tests pass in CI

## Test Requirements

- Unit tests (Vitest + RTL):
  - Renders empty state when no query params provided
  - Shows loading skeletons when fetching
  - Renders all six diff sections with correct item counts from fixture data
  - Displays error message when API returns error
- E2E test (Playwright):
  - Navigate to `/sbom/compare`
  - Select left SBOM from dropdown
  - Select right SBOM from dropdown
  - Click Compare button
  - Assert diff section headers are visible with count badges
  - Assert URL contains `left` and `right` query parameters

## Implementation Notes

In `src/routes.tsx`, add the route following the existing lazy-loading pattern:

```typescript
const SbomComparePage = React.lazy(() => import("./pages/SbomComparePage/SbomComparePage"));

// Inside route definitions:
{ path: "/sbom/compare", element: <SbomComparePage /> }
```

Place the route before the `/sbom/:id` route to avoid the dynamic segment capturing "compare" as an ID.

In `tests/mocks/handlers.ts`, add a handler following the existing pattern:

```typescript
rest.get("/api/v2/sbom/compare", (req, res, ctx) => {
  return res(ctx.json(sbomComparisonFixture));
})
```

The `tests/mocks/fixtures/sbom-comparison.json` fixture should include at least one item in each of the six diff categories for comprehensive test coverage.

For E2E tests, follow the pattern in `tests/e2e/sbom-list.spec.ts`.

### Figma Design References

- Test assertions should verify the Figma-specified UI elements: EmptyState with "Select two SBOMs to compare" title, ExpandableSection headers with Badge counts, and correct column headers in data tables.

## Applicable Conventions

- **Routing** (React Router v6 with lazy-loaded page components): Applies: task modifies `src/routes.tsx` matching the convention's routing scope.
- **Testing** (Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking): Applies: task creates test files in `src/pages/SbomComparePage/` and `tests/` matching the convention's testing scope.
