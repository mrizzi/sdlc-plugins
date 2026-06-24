## Repository
trustify-ui

## Target Branch
main

## Description
Add checkbox selection and a "Compare selected" action button to the existing SBOM list page. Users select exactly two SBOMs via checkboxes, then click "Compare selected" to navigate to the comparison page with the selected IDs as URL query parameters. This implements UC-1 from the feature requirements.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row checkboxes, selection state, and a "Compare selected" toolbar action button

## Implementation Notes
Modify the existing `SbomListPage` in `src/pages/SbomListPage/SbomListPage.tsx` to add multi-select capability:

1. Add selection state using React `useState` to track selected SBOM IDs (array of strings).
2. Add PatternFly checkbox selection to the existing SBOM `Table` using the composable table's `select` prop/column. Each row gets a checkbox.
3. Add a "Compare selected" PatternFly `Button` to the page toolbar (alongside existing filters in `FilterToolbar` from `src/components/FilterToolbar.tsx`). The button should:
   - Be disabled when fewer or more than 2 SBOMs are selected
   - Show the selected count as helper text (e.g., "2 selected")
   - On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`
4. Add a "Clear selection" link/button to clear all checkboxes.

Reference the existing table implementation in `SbomListPage.tsx` and add the checkbox column as the first column. Use PatternFly's `Table` composable pattern for row selection.

Per Key Conventions (Component library): All UI components use PatternFly 5 — use PatternFly `Table` select/checkbox pattern and `Button` component. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's component library scope.

Per Key Conventions (Routing): Use React Router v6 `useNavigate` for programmatic navigation. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` which uses React Router for navigation matching the convention's routing scope.

## Acceptance Criteria
- [ ] Each SBOM row in the list has a checkbox for selection
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when not exactly 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection can be cleared
- [ ] Existing list page functionality (filters, pagination) is not broken

## Test Requirements
- [ ] Unit test: checkboxes render for each SBOM row
- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button navigates with correct query params when 2 are selected
- [ ] Existing `SbomListPage.test.tsx` tests continue to pass

## Dependencies
- Depends on: Task 8 — Frontend routing (comparison page must be routable)

[sdlc-workflow] Description digest: sha256-md:4b8bf4cb00815c5e016eb0ccf6494d1649b7e2ce532b360f126e6a319e5390df
