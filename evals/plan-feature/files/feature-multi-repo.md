# Mock Jira Feature Issue

**Key**: TC-9003
**Summary**: SBOM comparison view
**Status**: New
**Labels**: ai-generated-jira
**Linked Issues**: None
**Figma**: https://www.figma.com/design/mock123/SBOMCompare (see figma-context.md for extracted design context)

---

## Feature Overview

Add a side-by-side SBOM comparison view that lets users select two SBOM versions and see what changed: added/removed packages, new/resolved vulnerabilities, and license changes. The comparison requires a new backend diffing endpoint and a frontend comparison UI built from Figma mockups.

## Background and Strategic Fit

When a new SBOM version is ingested (e.g., after a dependency update), users need to understand what changed. Currently they must manually open two SBOM detail pages and compare visually. A structured diff endpoint and dedicated comparison UI reduces time-to-insight and supports compliance workflows that require documenting what changed between releases.

## Goals

- **Who benefits**: Security analysts comparing SBOM versions, compliance officers documenting changes
- **Current state**: No comparison capability — users manually compare two SBOM detail pages
- **Target state**: Users select two SBOMs, see a structured diff with added/removed/changed packages and their vulnerability/license impact
- **Goal statements**:
  - Reduce comparison time from ~15 minutes (manual) to <30 seconds (automated diff)
  - Provide exportable diff report for compliance documentation

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns structured diff | Diff includes: added packages, removed packages, changed versions, new vulnerabilities, resolved vulnerabilities, license changes | Yes |
| Frontend comparison page at `/sbom/compare` | Side-by-side layout with collapsible sections per diff category | Yes |
| URL-shareable comparison | URL encodes both SBOM IDs for bookmarking | Yes |
| Export diff as JSON or CSV | For compliance documentation | No |
| Highlight packages with new critical vulnerabilities | Visual emphasis on high-risk changes | Yes |

## Non-Functional Requirements

- Comparison endpoint response time: p95 < 1s for SBOMs with up to 2000 packages each
- Frontend must handle large diffs without browser freezing — use virtualized lists for >100 changed packages
- No new database tables — compute diff on-the-fly from existing package and advisory data

## Use Cases (User Experience & Workflow)

### UC-1: Compare two SBOM versions

**Persona**: Security analyst reviewing a dependency update
**Pre-conditions**: Two SBOM versions exist for the same product (e.g., before and after a Renovate PR)
**Steps**:
1. User navigates to the SBOM list page
2. User selects two SBOMs using checkboxes
3. User clicks "Compare selected"
4. Frontend calls `GET /api/v2/sbom/compare?left={id1}&right={id2}`
5. Comparison view renders with sections: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes
6. User expands "New Vulnerabilities" to see advisory details for newly introduced packages

**Expected outcome**: All changes between the two SBOMs are visible in a structured, navigable view

### UC-2: Share comparison with compliance team

**Persona**: Compliance officer documenting a release
**Pre-conditions**: Comparison has been generated
**Steps**:
1. User copies the comparison URL from the browser
2. User shares URL with compliance team
3. Compliance team opens URL and sees the same comparison view

**Expected outcome**: URL loads the comparison directly without re-selecting SBOMs

## Customer Considerations

- Both SBOMs must be from the same product/project for a meaningful comparison
- Large SBOM diffs (>1000 package changes) may require pagination or filtering

## Customer Information/Supportability

- Add comparison endpoint to the API latency Grafana dashboard
- Monitor for timeouts on large SBOM comparisons (>2000 packages per SBOM)

## Documentation Considerations

- **Doc Impact**: New Content — document the comparison endpoint and comparison UI
- **User purpose**: API consumers need endpoint reference; UI users need a guide for the comparison workflow
- **Reference material**: Existing SBOM detail page documentation, package/advisory data model docs
