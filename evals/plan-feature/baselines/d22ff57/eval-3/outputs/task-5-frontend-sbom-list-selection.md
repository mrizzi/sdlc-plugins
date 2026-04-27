# Task 5 — Frontend: Add SBOM selection and "Compare selected" action to SBOM list page

## Repository
trustify-ui

## Description
Enhance the existing SBOM list page to support selecting two SBOMs for comparison. Add row checkboxes to the SBOM table and a "Compare selected" toolbar action that navigates to the comparison page (`/sbom/compare?left={id1}&right={id2}`) with the selected SBOM IDs. This implements the primary entry point for comparison as described in UC-1.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection to the SBOM table, add "Compare selected" button to the page toolbar
- `tests/mocks/handlers.ts` — add MSW handler for the comparison endpoint (for test support)
- `tests/mocks/fixtures/sboms.json` — ensure mock data has at least two distinct SBOMs for comparison testing

## Implementation Notes
- **Checkbox selection**: Add PatternFly table row selection (checkbox variant) to the existing SBOM list table. Track selected SBOM IDs in local component state (e.g., `useState<string[]>([])`).
- **Selection limit**: Allow selecting exactly two SBOMs. Disable further checkboxes once two are selected, or show a validation message. The "Compare selected" button should be disabled unless exactly two SBOMs are selected.
- **Compare selected button**: Add a PatternFly `Button` (secondary variant) to the page toolbar area. On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router's `useNavigate`.
- **Toolbar placement**: Place the "Compare selected" button alongside existing toolbar actions, following the toolbar layout pattern already used on the page.
- Follow existing patterns in `src/pages/SbomListPage/SbomListPage.tsx` for toolbar actions and table configuration.
- Per project conventions: use React Router `useNavigate` for navigation; PascalCase for components.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the page being modified; follow its existing table and toolbar patterns
- `src/components/FilterToolbar.tsx` — existing toolbar component; reference for toolbar action placement

## Acceptance Criteria
- [ ] SBOM list table rows have checkboxes for selection
- [ ] Users can select exactly two SBOMs
- [ ] "Compare selected" button appears in the page toolbar
- [ ] "Compare selected" button is disabled when fewer or more than two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Checkboxes can be toggled to change selection before comparing

## Test Requirements
- [ ] Unit test: SBOM list table renders with checkbox column
- [ ] Unit test: selecting two SBOMs enables the "Compare selected" button
- [ ] Unit test: selecting fewer than two SBOMs keeps the button disabled
- [ ] Unit test: clicking "Compare selected" navigates to the comparison page with correct query params
- [ ] Unit test: deselecting an SBOM disables the button again

## Dependencies
- Depends on: Task 4 — Frontend: Create SBOM comparison page with diff sections
