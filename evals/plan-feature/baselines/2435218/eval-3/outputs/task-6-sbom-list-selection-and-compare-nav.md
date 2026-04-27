# Task 6 — SBOM list page checkbox selection and compare navigation

## Repository
trustify-ui

## Description
Enhance the existing SBOM list page to allow users to select two SBOMs via checkboxes and navigate to the comparison page. This implements UC-1 from the feature specification: the user selects two SBOMs from the list and clicks a "Compare selected" button that navigates to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection column to the SBOM table, selection state management, and a "Compare selected" toolbar action

## Implementation Notes
- **Selection pattern**: add a checkbox column to the existing SBOM list table. Use React state (`useState<string[]>([])`) to track selected SBOM IDs. Limit selection to exactly 2 — disable remaining checkboxes once 2 are selected, or show a validation message if the user tries to select more than 2.
- **"Compare selected" button**: add a primary action button to the page toolbar (near existing filter controls). The button should:
  - Be disabled when fewer than 2 SBOMs are selected
  - Show selection count (e.g., "Compare selected (2)")
  - On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`
- **PatternFly table selection**: PatternFly 5's `Table` (composable) supports row selection via checkbox. Follow the PF5 selectable table pattern. Reference the existing table implementation in `src/pages/SbomListPage/SbomListPage.tsx` for the current column definition pattern.
- **Toolbar integration**: the existing page likely uses `FilterToolbar` from `src/components/FilterToolbar.tsx`. Add the "Compare selected" button alongside existing toolbar actions, using PatternFly's `ToolbarItem` component.
- **UX consideration**: clear the selection when the user changes filter or pagination state, to prevent comparing SBOMs that are no longer visible.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — the existing page component being modified; contains the table and toolbar to extend
- `src/components/FilterToolbar.tsx` — existing toolbar component; reference for toolbar item placement
- `src/routes.tsx` — route definitions; the comparison route `/sbom/compare` must already exist (from Task 5)

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] Users can select exactly 2 SBOMs via checkboxes
- [ ] Selecting more than 2 is prevented (remaining checkboxes disabled after 2 selections)
- [ ] "Compare selected" button appears in the page toolbar
- [ ] "Compare selected" button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selection is cleared when filters or pagination change

## Test Requirements
- [ ] Unit test: checkbox column renders in the SBOM table
- [ ] Unit test: selecting 2 SBOMs enables the "Compare selected" button
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both IDs
- [ ] Unit test: selecting more than 2 SBOMs is prevented
- [ ] Unit test: changing filters clears the selection

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation passes
- `npx vitest run --reporter=verbose` — unit tests pass

## Dependencies
- Depends on: Task 5 — SBOM comparison page and routing (comparison page must exist for navigation to work)
