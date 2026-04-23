# Impact Map: TC-9003 — SBOM Comparison View

## Goal

Reduce SBOM-to-SBOM comparison time from ~15 minutes (manual, side-by-side page review) to <30 seconds (automated structured diff), enabling security analysts and compliance officers to quickly understand what changed between two SBOM versions.

## Actors

- **Security analysts** — review dependency updates and need to identify newly introduced vulnerabilities
- **Compliance officers** — document release-over-release changes for audit evidence

## Impacts

### Impact 1: Analysts can get a structured diff between two SBOMs in <30 seconds

**Deliverables**:
- Task 1: Backend diff service and `GET /api/v2/sbom/compare` endpoint (trustify-backend)
- Task 2: TypeScript API client, response models, and React Query hook for the compare endpoint (trustify-ui)

### Impact 2: Analysts can navigate the diff in a dedicated comparison UI

**Deliverables**:
- Task 3: `SbomComparePage` with SBOM selectors, collapsible diff sections, and URL-shareable state (trustify-ui)

### Impact 3: High-risk changes are immediately visible

**Deliverables**:
- Task 3: Critical-severity rows highlighted in the New Vulnerabilities section using PatternFly row styling (trustify-ui)

### Impact 4: Compliance officers can share and bookmark comparison results

**Deliverables**:
- Task 3: URL query params (`?left={id}&right={id}`) encode both SBOM selections; page pre-populates selectors from URL on load (trustify-ui)

## Task Summary

| # | Title | Repository | Depends On |
|---|---|---|---|
| 1 | SBOM diff service and compare endpoint | trustify-backend | — |
| 2 | API client, models, and React Query hook for SBOM compare | trustify-ui | Task 1 |
| 3 | SbomComparePage UI with diff sections and URL state | trustify-ui | Task 2 |

## Out of Scope (Non-MVP)

- Export diff as JSON or CSV (feature requirement marked non-MVP)
- Pagination or filtering for large diffs >1000 package changes
