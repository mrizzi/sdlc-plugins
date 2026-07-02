## TC-9003: SBOM Comparison View — Implementation Plan Summary

### Tasks Created

9 tasks created for feature TC-9003:

| Task | Repository | Description |
|---|---|---|
| Task 1 | trustify-ui | Create feature branch `TC-9003` (bookend: create-branch) |
| Task 2 | trustify-backend | SBOM comparison diff model structs |
| Task 3 | trustify-backend | SBOM comparison service logic |
| Task 4 | trustify-backend | SBOM comparison endpoint and integration tests |
| Task 5 | trustify-ui | API types, client function, and React Query hook for SBOM comparison |
| Task 6 | trustify-ui | SBOM comparison page UI with diff sections |
| Task 7 | trustify-ui | SBOM list compare selection, MSW mocks, unit tests, and E2E test |
| Task 8 | trustify-backend | Documentation for SBOM comparison feature |
| Task 9 | trustify-ui | Merge feature branch `TC-9003` to `main` (bookend: merge-branch) |

### Repositories Affected

- **trustify-backend** — 4 tasks (model, service, endpoint/tests, documentation)
- **trustify-ui** — 5 tasks (2 bookends + API layer, comparison page, list integration/tests)

### Architecture Summary

**Workflow mode**: Feature-branch (`TC-9003`) — cross-repo atomicity required because the frontend comparison page depends on the backend comparison endpoint; neither side functions independently.

**Backend**: New `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint computes a structured diff on-the-fly from existing SBOM, package, advisory, and license data (no new database tables). The diff covers six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The comparison service reuses existing `SbomService`, `PackageService`, and `AdvisoryService` for data retrieval.

**Frontend**: New comparison page at `/sbom/compare` built with PatternFly 5 components following Figma design specifications — header toolbar with typeahead SBOM `Select` dropdowns, Compare/Export actions, and six collapsible `ExpandableSection` diff sections with color-coded count `Badge` indicators and sortable composable `Table` components. URL-encoded SBOM IDs via query params support bookmarking and sharing. The SBOM list page gains checkbox selection and a "Compare selected" navigation action. Virtualized rendering handles large diffs (>100 rows).

### Propagated Fields

```
additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

Priority **Critical** propagated from parent feature TC-9003 to all tasks.
Fix Version **RHTPA 1.5.0** propagated from parent feature TC-9003 to all tasks.
