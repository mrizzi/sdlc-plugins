## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add checkbox selection support to the SBOM list page so users can select two SBOMs and navigate to the comparison page. This implements the primary entry point for the comparison workflow described in UC-1: users select two SBOMs from the list, click "Compare selected", and are navigated to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, track selected SBOMs, add "Compare selected" toolbar action button

## Implementation Notes
- Follow the existing table pattern in `src/pages/SbomListPage/SbomListPage.tsx` — add a checkbox column as the first column using PatternFly `Table` composable select pattern.
- Track selected SBOM IDs using React `useState<string[]>` — limit selection to exactly 2 items for comparison.
- Add a "Compare selected" `Button` to the existing toolbar area (reference `src/components/FilterToolbar.tsx` for toolbar layout patterns). The button should:
  - Be disabled when fewer than 2 SBOMs are selected
  - Use `useNavigate` from React Router to navigate to `/sbom/compare?left=${selected[0]}&right=${selected[1]}`
- When a third checkbox is selected, either deselect the oldest selection (FIFO) or disable further checkboxes — follow the UX pattern that best matches existing PatternFly table selection patterns.
- Use PatternFly `Toolbar` and `ToolbarItem` to position the Compare button alongside existing toolbar elements.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM list page with table to extend
- `src/components/FilterToolbar.tsx` — existing toolbar layout pattern to follow for button placement

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection is limited to 2 SBOMs maximum

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with both SBOM IDs
- [ ] Unit test: selecting a third SBOM handles the overflow correctly (FIFO deselection or disabled checkboxes)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
