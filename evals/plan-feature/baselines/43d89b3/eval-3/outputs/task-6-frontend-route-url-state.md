## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Register the `/sbom/compare` route in the application router and implement URL-shareable comparison state. The comparison page URL encodes both SBOM IDs as query parameters (`?left={id1}&right={id2}`) so comparisons can be bookmarked and shared. Add a "Compare selected" action to the existing SBOM list page that navigates to the comparison page with the selected SBOM IDs pre-populated.

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` pointing to the SbomComparePage component with lazy loading
- `src/App.tsx` — Ensure the new route is included in the router setup (if not auto-discovered from routes.tsx)
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection for SBOMs and a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
For route registration in `src/routes.tsx`, follow the existing pattern of lazy-loaded page components:
```typescript
const SbomComparePage = React.lazy(() => import("./pages/SbomComparePage/SbomComparePage"));
```

Add the route alongside the existing SBOM routes. Use React Router v6 route definition pattern as established in the existing routes.

For URL state management, use React Router's `useSearchParams` hook to read and write the `left` and `right` query parameters. When the user selects SBOMs and clicks Compare, update the URL search params. When the page loads with query params present, auto-populate the selectors and trigger the comparison.

For the SBOM list page integration, add PatternFly `Table` row selection (checkbox column) and a "Compare selected" toolbar action button. The button should be disabled unless exactly two SBOMs are selected. On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`.

Follow the existing PatternFly component patterns used in `src/pages/SbomListPage/SbomListPage.tsx` for toolbar actions and table interactions.

## Reuse Candidates
- `src/routes.tsx` — Existing route definitions; follow the same lazy-loading pattern for the new comparison route
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing SBOM list page; add selection and compare action following the established toolbar pattern
- `src/components/FilterToolbar.tsx` — Existing toolbar component; reference for adding toolbar action buttons

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and renders SbomComparePage
- [ ] Route uses lazy loading consistent with other page routes
- [ ] URL query params `left` and `right` are read on page load to pre-populate SBOM selectors
- [ ] Changing SBOM selection and clicking Compare updates the URL query params
- [ ] Comparison URL is shareable — opening the URL in a new browser tab loads the same comparison
- [ ] SBOM list page has checkbox selection for SBOM rows
- [ ] "Compare selected" button appears in the SBOM list toolbar, disabled unless exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`

## Test Requirements
- [ ] Unit test: `/sbom/compare` route renders the SbomComparePage component
- [ ] Unit test: page loads with `?left=id1&right=id2` query params and pre-populates selectors
- [ ] Unit test: clicking Compare updates URL search params
- [ ] Unit test: "Compare selected" button on SBOM list page is disabled with fewer than 2 selections
- [ ] Unit test: "Compare selected" button navigates to comparison page with correct query params

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Implement SBOM comparison page with PatternFly components
