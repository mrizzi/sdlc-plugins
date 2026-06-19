## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add MSW (Mock Service Worker) request handlers and test fixtures for the SBOM comparison endpoint. These mocks enable frontend component tests to run without a live backend. Also add comprehensive component tests for the ComparisonPage that exercise the full user flow: selecting SBOMs, triggering a comparison, and verifying the rendered diff sections.

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture with representative data across all six diff categories

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` that returns the mock fixture
- `src/pages/ComparisonPage/ComparisonPage.test.tsx` — Add comprehensive component tests (extend the test file created in Task 8)

## Implementation Notes

### MSW Handler

Add to `tests/mocks/handlers.ts` following the existing handler patterns:

```typescript
rest.get("/api/v2/sbom/compare", (req, res, ctx) => {
  const left = req.url.searchParams.get("left");
  const right = req.url.searchParams.get("right");

  if (!left || !right) {
    return res(ctx.status(400), ctx.json({ message: "Missing left or right parameter" }));
  }

  return res(ctx.status(200), ctx.json(sbomComparisonFixture));
});
```

### Mock Fixture (`sbom-comparison.json`)

Create a fixture with representative data:
- 2-3 added packages (with varying advisory counts)
- 1-2 removed packages
- 2 version changes (one upgrade, one downgrade)
- 2 new vulnerabilities (one critical, one medium -- to test highlighted row styling)
- 1 resolved vulnerability
- 1 license change

### Component Tests

Using Vitest + React Testing Library + MSW:

1. **Empty state test**: Render ComparisonPage without query params. Assert that the EmptyState component is visible with "Select two SBOMs to compare" text.
2. **Comparison flow test**: Render ComparisonPage, select two SBOMs from the selectors, click Compare. Assert that all six diff sections appear with correct item counts in badges.
3. **URL pre-population test**: Render ComparisonPage with `?left=id1&right=id2` query params. Assert that the comparison loads automatically and results are displayed.
4. **Section expansion test**: Assert that sections with >0 items are expanded by default and sections with 0 items are collapsed.
5. **Critical vulnerability highlighting test**: Assert that rows with severity "Critical" in the New Vulnerabilities section have the highlighted CSS class.
6. **Loading state test**: Assert that skeleton placeholders are visible while the comparison API call is in progress.

## Reuse Candidates
- `tests/mocks/handlers.ts` — Existing MSW handler patterns for other endpoints
- `tests/mocks/fixtures/sboms.json` — Reference for fixture data structure
- `tests/setup.ts` — Test setup with MSW server and render helpers
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Reference for page component test patterns

## Acceptance Criteria
- [ ] MSW handler intercepts `GET /api/v2/sbom/compare` and returns mock data
- [ ] Mock fixture contains representative data for all six diff categories
- [ ] All component tests pass with `npm test` / `vitest`
- [ ] Tests cover empty state, comparison flow, URL pre-population, section expansion, critical highlighting, and loading state

## Test Requirements
- [ ] Empty state renders when no query params are present
- [ ] Comparison results render after user selects SBOMs and clicks Compare
- [ ] Pre-populated URL triggers automatic comparison load
- [ ] Sections with items are expanded by default
- [ ] Critical vulnerability rows have highlighted styling
- [ ] Loading skeleton is visible during API call

## Dependencies
- Depends on: Task 8 — Frontend ComparisonPage
