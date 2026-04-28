## Repository
trustify-ui

## Description
Add checkbox-based multi-selection to the SBOM list page so users can select exactly two SBOMs and click a "Compare selected" button to navigate to the comparison page. This implements the entry point for UC-1 where users discover and initiate a comparison from the main SBOM listing.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox column to the SBOM table, selection state management, and a "Compare selected" toolbar action button that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
Follow the existing patterns in `src/pages/SbomListPage/SbomListPage.tsx` for table configuration and toolbar layout.

**Checkbox selection:**
- Add a checkbox column to the existing SBOM PatternFly `Table` using PatternFly's composable table select functionality
- Track selected SBOM IDs in component state: `const [selectedIds, setSelectedIds] = useState<string[]>([])`
- Limit selection to exactly two SBOMs. When a third is selected, deselect the oldest selection (FIFO) or disable further checkboxes — follow whichever UX pattern is more consistent with PatternFly conventions

**Compare selected button:**
- Add a "Compare selected" PatternFly `Button` to the toolbar area (alongside any existing filter controls from `FilterToolbar`)
- Button is disabled when fewer than 2 SBOMs are selected
- On click, navigate using React Router's `useNavigate()`:
  ```typescript
  navigate(`/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}`);
  ```

**Figma design context:**
The Figma mockup shows the comparison flow starting from SBOM selection (UC-1 steps 1-3). The selectors on the comparison page itself are the primary selection mechanism, but the list page provides a convenience entry point for users already browsing SBOMs.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — this is the file being modified; study its current table and toolbar structure
- `src/components/FilterToolbar.tsx` — existing toolbar pattern; add the Compare button alongside it

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] Users can select exactly two SBOMs via checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Existing SBOM list functionality (filtering, pagination, sorting) is unaffected

## Test Requirements
- [ ] Unit test: checkbox column renders in the SBOM table
- [ ] Unit test: selecting two SBOMs enables the Compare button
- [ ] Unit test: clicking Compare navigates to the comparison page with correct query params
- [ ] Unit test: existing SBOM list filtering and pagination still work after adding selection

## Dependencies
- Depends on: Task 5 — Frontend comparison page (the navigation target must exist)
