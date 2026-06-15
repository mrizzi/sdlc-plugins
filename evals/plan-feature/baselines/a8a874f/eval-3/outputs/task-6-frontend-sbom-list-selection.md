# TC-9003-6: SBOM list page selection and comparison navigation

## Repository

trustify-ui

## Target Branch

TC-9003

## Description

Add multi-select capability to the SBOM list page so users can select two SBOMs and navigate to the comparison view. This implements UC-1 from the feature requirements: users select two SBOMs via checkboxes on the list page, click "Compare selected", and are routed to `/sbom/compare?left={id1}&right={id2}`.

## Files to Modify

- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes and a "Compare selected" toolbar action

## Files to Create

- `src/pages/SbomListPage/SbomListPage.test.tsx` — Update existing tests (or create if the test file needs new comparison-specific test cases)
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison API response fixture for MSW handlers
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` (modify existing file)

## Dependencies

- TC-9003-5 (comparison page must exist for navigation target)

## Implementation Notes

### Figma Design Reference

The SBOM list page modifications follow the comparison workflow entry point from the Figma design:

- Add PatternFly `Table` row selection using the composable table's `select` variant. Each row gets a checkbox. Selection is managed via React state (`useState<string[]>` for selected SBOM IDs).
- Add a PatternFly `Button` labeled "Compare selected" in the toolbar area (alongside existing filters in `src/pages/SbomListPage/SbomListPage.tsx`). The button should:
  - Be disabled when fewer than 2 SBOMs are selected
  - Be disabled when more than 2 SBOMs are selected (show tooltip: "Select exactly two SBOMs to compare")
  - On click: navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate`
- Use the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` as a pattern for toolbar integration.

### MSW Mock Data
- Create `tests/mocks/fixtures/sbom-comparison.json` with a representative comparison response matching the `SbomComparison` interface.
- Add a handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` that returns the fixture data.

## Acceptance Criteria

- [ ] SBOM list table rows have selection checkboxes
- [ ] "Compare selected" button appears in the toolbar
- [ ] Button is disabled when selection count is not exactly 2
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Selected SBOM IDs are passed correctly as URL parameters

## Test Requirements

- [ ] Unit test: "Compare selected" button is disabled with 0, 1, or 3+ selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking "Compare selected" navigates to the correct URL with SBOM IDs
- [ ] MSW fixture provides realistic comparison data for downstream test usage

## Verification Commands

- `npx vitest run src/pages/SbomListPage/` — run SBOM list page tests
- `npx vitest run src/pages/SbomComparePage/` — run comparison page tests (validate no regressions)

## Reuse Candidates

- `src/components/FilterToolbar.tsx` — Toolbar integration pattern
- `src/hooks/useSboms.ts` — Already used by SbomListPage, no changes needed

## Convention Compliance

- `Applies: task modifies src/pages/SbomListPage/SbomListPage.tsx matching the convention's page structure scope.`
- `Applies: task creates tests/mocks/fixtures/sbom-comparison.json matching the convention's MSW testing scope (tests/mocks/).`

[Description digest: sha256-md:f8c2b6d4e1a7c3f9b5e0a6d2f8c4e1b7a3d9f5c0e6b2a8d4f1c7e3b9a5d0f6c2]
