# Impact Map: TC-9003 SBOM Comparison View

## Overview

This feature adds a side-by-side SBOM comparison view that lets users select two SBOM versions and see a structured diff of changes: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The implementation spans the backend (new diffing endpoint) and the frontend (comparison UI built from Figma mockups).

## Repository: trustify-backend

### New Files
| File | Purpose | Task |
|---|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Comparison result structs: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` | Task 1 |
| `modules/fundamental/src/sbom/service/compare.rs` | Service method that computes the SBOM diff by querying packages, advisories, and licenses for both SBOMs | Task 1 |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | REST handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}` | Task 2 |
| `tests/api/sbom_compare.rs` | Integration tests for the comparison endpoint | Task 3 |

### Modified Files
| File | Change | Task |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod comparison;` | Task 1 |
| `modules/fundamental/src/sbom/service/mod.rs` | Add `pub mod compare;` | Task 1 |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Add `pub mod compare;` and register `/compare` route | Task 2 |

### API Changes
| Endpoint | Method | Change |
|---|---|---|
| `/api/v2/sbom/compare?left={id1}&right={id2}` | GET | NEW — Returns structured diff between two SBOMs |

### Key Entities Referenced
| Entity | File | Relationship |
|---|---|---|
| SBOM | `entity/src/sbom.rs` | Primary entities being compared |
| Package | `entity/src/package.rs` | Compared for additions, removals, version changes |
| Advisory | `entity/src/advisory.rs` | Compared for new and resolved vulnerabilities |
| SBOM-Package join | `entity/src/sbom_package.rs` | Used to query packages per SBOM |
| SBOM-Advisory join | `entity/src/sbom_advisory.rs` | Used to query advisories per SBOM |
| Package-License | `entity/src/package_license.rs` | Used for license change detection |

---

## Repository: trustify-ui

### New Files
| File | Purpose | Task |
|---|---|---|
| `src/hooks/useSbomComparison.ts` | React Query hook for fetching SBOM comparison data | Task 4 |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Main comparison page with toolbar and diff sections | Task 5 |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Reusable collapsible diff section with `ExpandableSection`, `Badge`, and `Table` | Task 5 |
| `src/pages/SbomComparePage/components/SbomSelector.tsx` | SBOM selector dropdown using PatternFly `Select` with typeahead | Task 5 |
| `src/pages/SbomComparePage/components/ExportDropdown.tsx` | Export dropdown with JSON and CSV options | Task 5 |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Unit tests for the comparison page | Task 7 |
| `tests/mocks/fixtures/sbom-comparison.json` | Mock fixture for comparison API response | Task 7 |
| `tests/e2e/sbom-compare.spec.ts` | Playwright E2E test for comparison workflow | Task 7 |

### Modified Files
| File | Change | Task |
|---|---|---|
| `src/api/models.ts` | Add `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` interfaces | Task 4 |
| `src/api/rest.ts` | Add `fetchSbomComparison()` API function | Task 4 |
| `src/routes.tsx` | Add `/sbom/compare` route | Task 5 |
| `src/App.tsx` | Include new route in router setup if needed | Task 5 |
| `src/pages/SbomListPage/SbomListPage.tsx` | Add row selection checkboxes and "Compare selected" button | Task 6 |
| `tests/mocks/handlers.ts` | Add MSW handler for comparison endpoint | Task 7 |

### Reused Existing Components
| Component | File | Usage |
|---|---|---|
| `SeverityBadge` | `src/components/SeverityBadge.tsx` | Severity display in vulnerability diff tables |
| `EmptyStateCard` | `src/components/EmptyStateCard.tsx` | Reference for empty state pattern |
| `FilterToolbar` | `src/components/FilterToolbar.tsx` | Reference for toolbar layout patterns |
| `LoadingSpinner` | `src/components/LoadingSpinner.tsx` | Reference for loading indicator patterns |

---

## Task Dependency Graph

```
Task 1 (backend: model + service)
  └── Task 2 (backend: endpoint)
        ├── Task 3 (backend: integration tests)
        └── Task 4 (frontend: API client + hook)
              └── Task 5 (frontend: comparison page)
                    ├── Task 6 (frontend: list page compare action)
                    └── Task 7 (frontend: tests)
```

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Large SBOM diffs (>2000 packages) may cause slow endpoint response | Compute diff in memory using HashMaps after bulk loading; target p95 < 1s |
| Large diffs may cause browser freezing | Virtualized lists for >100 changed packages in frontend |
| Frontend depends on backend endpoint being available | Backend tasks (1-3) ordered before frontend tasks (4-7); frontend can be developed with MSW mocks in parallel |
