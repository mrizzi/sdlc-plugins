## Repository
trustify-ui

## Target Branch
main

## Description
Add SBOM selection capability and a "Compare selected" action to the SBOM list page. Users can select exactly two SBOMs using checkboxes in the existing SBOM table, then click "Compare selected" to navigate to the comparison page with the selected SBOM IDs in the URL query parameters. This implements the entry point for UC-1 (Compare two SBOM versions) from the feature requirements, where users begin the comparison workflow from the SBOM list.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Critical", "fixVersions": "RHTPA 1.5.0" }

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` -- add checkbox selection column to the SBOM table and a "Compare selected" action button in the toolbar area that navigates to `/sbom/compare?left={id1}&right={id2}`

## Implementation Notes
**Figma design reference:** Per UC-1 in the feature requirements, the SBOM list page is the primary entry point where users select two SBOMs for comparison. The Figma comparison view design (figma-context.md) shows the target page with PatternFly `Select` selectors on the comparison page itself; this task adds the list-page entry point that navigates to that page.

**Checkbox selection column:**
- Use PatternFly `Table` composable select variant to add a checkbox column to the existing SBOM table in `SbomListPage.tsx`
- Track selected row IDs in component state (e.g., `useState<string[]>([])`)
- Limit selection to exactly two SBOMs -- disable additional checkboxes once two are selected, or show a PatternFly tooltip explaining the limit

**"Compare selected" action button:**
- Place in the page toolbar area alongside existing filters (reference `src/components/FilterToolbar.tsx` for toolbar layout)
- Use PatternFly `Button` (secondary variant)
- Disabled until exactly two SBOMs are selected
- On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router's `useNavigate`

Ensure existing list page functionality (filters, pagination, sorting) remains unaffected by the selection additions.

Per CONVENTIONS.md §Component Library: PatternFly 5 -- all UI components use PF5 equivalents.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- the existing page to modify; understand the current table structure and toolbar layout before adding selection
- `src/components/FilterToolbar.tsx` -- existing filter toolbar component; reference for toolbar action button placement alongside filters
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- existing test file; extend with new test cases for selection and compare navigation

## Acceptance Criteria
- [ ] SBOM list table has a checkbox selection column
- [ ] Users can select exactly two SBOMs using checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] Button is disabled when fewer or more than two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}` with the correct IDs
- [ ] Existing list page functionality (filters, pagination, sorting) is unaffected

## Test Requirements
- [ ] Unit test: checkbox selection column renders in the SBOM table
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs

## Verification Commands
- `npx tsc --noEmit` -- TypeScript compilation passes
- `npx vitest run src/pages/SbomListPage` -- list page tests pass

## Dependencies
- Depends on: Task 5 -- Create SBOM comparison page (the navigation target route must exist)
