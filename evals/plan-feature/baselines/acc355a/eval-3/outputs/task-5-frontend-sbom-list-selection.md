# Task 5 — Add checkbox selection and Compare action to SBOM list page

## Repository
trustify-ui

## Target Branch
main

## Description
Enhance the existing SBOM list page to support selecting two SBOMs via checkboxes and navigating to the comparison page. This implements UC-1 from the feature requirements where a user selects two SBOMs from the list and clicks "Compare selected" to navigate to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — Add checkbox selection column to the SBOM table, add "Compare selected" toolbar action button, and implement navigation to comparison page with selected SBOM IDs as query params
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` to support testing
- `tests/mocks/fixtures/sboms.json` — Add additional mock SBOM entries if needed for comparison testing

## Files to Create
- `src/pages/SbomListPage/SbomListPage.test.tsx` — Update or extend existing tests to cover checkbox selection and Compare navigation (if the existing test file needs new test cases)
- `tests/mocks/fixtures/sbom-comparison.json` — Mock fixture for SBOM comparison API response

## Implementation Notes
- Add a PatternFly checkbox column to the existing SBOM table in `SbomListPage.tsx`. Use PatternFly's `Table` select variant or manual checkbox cells.
- Track selected SBOM IDs in component state (e.g., `useState<string[]>([])`). Limit selection to exactly 2 SBOMs — disable further checkboxes when 2 are selected, or show a validation message.
- Add a "Compare selected" button to the toolbar area (alongside existing filter controls in `FilterToolbar`). The button should be disabled when fewer than 2 SBOMs are selected.
- On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`.
- Follow the existing `SbomListPage.tsx` patterns for toolbar actions and table configuration.
- The MSW mock handler for the comparison endpoint should return the fixture from `tests/mocks/fixtures/sbom-comparison.json` with the expected response shape.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table and toolbar implementation to extend
- `src/components/FilterToolbar.tsx` — reference for toolbar action button placement
- `tests/mocks/handlers.ts` — follow existing handler patterns for the new comparison endpoint mock
- `tests/mocks/fixtures/sboms.json` — existing SBOM mock data to reference

## Acceptance Criteria
- [ ] SBOM list table has a checkbox column for row selection
- [ ] Users can select exactly 2 SBOMs via checkboxes
- [ ] "Compare selected" button appears in the toolbar area
- [ ] "Compare selected" button is disabled when fewer than 2 SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] MSW mock handler exists for the comparison endpoint
- [ ] Mock fixture file contains a valid comparison response

## Test Requirements
- [ ] Unit test: checkbox column renders in the SBOM list table
- [ ] Unit test: selecting two SBOMs enables the "Compare selected" button
- [ ] Unit test: "Compare selected" button is disabled with fewer than 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct comparison URL with both SBOM IDs
- [ ] Unit test: deselecting an SBOM disables the "Compare selected" button

## Dependencies
- Depends on: Task 4 — Add SBOM comparison page with diff section components
