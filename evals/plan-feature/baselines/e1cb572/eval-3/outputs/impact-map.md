# Repository Impact Map: TC-9003 — SBOM Comparison View

## Workflow Mode

**Feature-branch** — The frontend comparison page depends on the backend comparison endpoint (`GET /api/v2/sbom/compare`). Merging the frontend without the backend would result in a broken page calling a non-existent endpoint. These are tightly coupled, atomically dependent changes across two repositories, satisfying the atomicity criteria for feature-branch mode.

**Label**: `workflow:feature-branch`
**Feature Branch**: `TC-9003`
**Base Branch**: `main`

## trustify-backend

### New Files

| File | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/compare.rs` | `SbomComparison` response struct with diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes) |
| `modules/fundamental/src/sbom/service/compare.rs` | Comparison service logic — fetches packages and advisories for two SBOMs, computes structured diff |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler |
| `tests/api/sbom_compare.rs` | Integration tests for the comparison endpoint |

### Modified Files

| File | Change |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod compare;` re-export |
| `modules/fundamental/src/sbom/service/mod.rs` | Add `pub mod compare;` re-export |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register comparison route in router |

### Unchanged (Reuse Candidates)

| File | Symbol | Reuse Reason |
|---|---|---|
| `modules/fundamental/src/sbom/service/sbom.rs` | `SbomService` | Fetch SBOM details and associated packages |
| `modules/fundamental/src/advisory/service/advisory.rs` | `AdvisoryService` | Query advisories linked to SBOM packages |
| `modules/fundamental/src/package/service/mod.rs` | `PackageService` | Fetch package lists for diff computation |
| `modules/fundamental/src/package/model/summary.rs` | `PackageSummary` | Package struct with license field, used in diff output |
| `modules/fundamental/src/advisory/model/summary.rs` | `AdvisorySummary` | Advisory struct with severity field, used in vulnerability diff |
| `common/src/error.rs` | `AppError` | Error handling for invalid IDs, missing SBOMs |
| `entity/src/sbom_package.rs` | SBOM-Package join entity | Query packages per SBOM for diff |
| `entity/src/sbom_advisory.rs` | SBOM-Advisory join entity | Query advisories per SBOM for vulnerability diff |

## trustify-ui

### New Files

| File | Purpose |
|---|---|
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Main comparison page component with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Unit tests for the comparison page |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Reusable collapsible diff section with ExpandableSection, Badge count, and data Table |
| `src/pages/SbomComparePage/components/SbomSelector.tsx` | SBOM selector dropdown using PatternFly Select with typeahead |
| `src/hooks/useSbomComparison.ts` | React Query hook for `GET /api/v2/sbom/compare` |
| `tests/mocks/fixtures/sbom-comparison.json` | Mock comparison response data for tests |

### Modified Files

| File | Change |
|---|---|
| `src/api/models.ts` | Add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` |
| `src/api/rest.ts` | Add `fetchSbomComparison(leftId, rightId)` API client function |
| `src/routes.tsx` | Add route: `/sbom/compare` pointing to `SbomComparePage` |
| `src/pages/SbomListPage/SbomListPage.tsx` | Add checkbox selection and "Compare selected" button to navigate to comparison page |
| `tests/mocks/handlers.ts` | Add MSW handler for `GET /api/v2/sbom/compare` |

### Unchanged (Reuse Candidates)

| File | Symbol | Reuse Reason |
|---|---|---|
| `src/components/SeverityBadge.tsx` | `SeverityBadge` | Display severity in New/Resolved Vulnerabilities tables |
| `src/components/EmptyStateCard.tsx` | `EmptyStateCard` | Empty state when no comparison performed |
| `src/components/LoadingSpinner.tsx` | `LoadingSpinner` | Loading state during comparison API call |
| `src/components/FilterToolbar.tsx` | `FilterToolbar` | Potential reuse for filtering large diffs |
| `src/hooks/useSboms.ts` | `useSboms` | Fetch SBOM list for selector dropdowns |
| `src/api/client.ts` | Axios instance | Base HTTP client for comparison API call |
| `src/utils/severityUtils.ts` | Severity ordering/colors | Sort and color-code vulnerability severity |

## Cross-Repository Dependencies

```
trustify-backend                          trustify-ui
─────────────────                         ────────────
Task 2: Comparison model + service ──┐
Task 3: Comparison endpoint + tests ─┤
                                     ├──▶ Task 4: API types + hook
                                     └──▶ Task 5: Comparison page (Figma)
                                          Task 6: SbomListPage compare action
```

Frontend tasks 4, 5, and 6 depend on backend tasks 2 and 3 being complete (the endpoint must exist before the frontend can integrate). Within the feature branch, this ordering is enforced by task numbering: backend tasks (2-3) precede frontend tasks (4-6).
