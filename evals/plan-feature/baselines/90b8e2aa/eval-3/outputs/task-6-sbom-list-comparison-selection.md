## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection to the SBOM list page so users can select exactly two SBOMs and navigate to the comparison page. Add a "Compare selected" button to the toolbar that is enabled only when exactly two SBOMs are selected. Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the table, selection state management (limited to 2 selections), and "Compare selected" button in the toolbar

## Implementation Notes
- Follow the existing table and toolbar patterns in `src/pages/SbomListPage/SbomListPage.tsx`.
- Add a checkbox column using PatternFly `Table` composable selection (`isSelected`, `onSelect` row props).
- Track selected SBOM IDs in component state using `useState<string[]>([])`, limiting the array to at most 2 entries.
- When a user selects a third SBOM, either deselect the oldest selection (FIFO) or prevent the selection and display a tooltip indicating the 2-selection limit.
- Add a "Compare selected" PatternFly `Button` with `variant="secondary"` to the toolbar area, positioned alongside existing filter/action controls.
- The button is disabled when fewer than 2 SBOMs are selected, enabled when exactly 2 are selected.
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate` hook.
- Per the frontend key conventions (Component library): PatternFly 5 — all UI components use PF5 equivalents.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.
- Per the frontend key conventions (Routing): React Router v6 — use `useNavigate` for programmatic navigation.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.
- Selection state should be cleared when the user navigates away from the list page (React component unmount handles this naturally with local state).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table structure and toolbar layout to extend
- `src/components/FilterToolbar.tsx` — existing toolbar component pattern for button placement

## Acceptance Criteria
- [ ] SBOM list page displays checkboxes for each row
- [ ] A maximum of 2 SBOMs can be selected at any time
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer than 2 SBOMs are selected
- [ ] Button is enabled when exactly 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs
- [ ] Selection state is cleared when navigating away from the page

## Test Requirements
- [ ] Unit test: checkboxes render for each SBOM row
- [ ] Unit test: selecting a third SBOM does not exceed the 2-selection limit
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the comparison page with correct query params

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with diff section components
