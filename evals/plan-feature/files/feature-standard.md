# Mock Jira Feature Issue

**Key**: TC-9001
**Summary**: Add advisory severity aggregation endpoint
**Status**: New
**Labels**: ai-generated-jira
**Linked Issues**: None

---

## Feature Overview

Add a new REST API endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Consumers need a quick summary of how many advisories at each severity level (Critical, High, Medium, Low) affect a given SBOM, without fetching and counting individual advisories client-side. This reduces frontend round-trips and enables dashboard widgets to render severity breakdowns efficiently.

## Background and Strategic Fit

The Trusted Profile Analyzer platform ingests SBOMs and correlates them with known vulnerability advisories. Currently, the frontend fetches all advisories for an SBOM and counts severities client-side, which is slow for SBOMs with hundreds of advisories. A server-side aggregation endpoint aligns with the platform's strategy of pushing computation to the backend and serving pre-computed summaries.

## Goals

- **Who benefits**: Frontend dashboard team, API consumers building severity widgets
- **Current state**: Frontend fetches `GET /api/v2/sbom/{id}/advisories` (paginated), iterates all pages, counts by severity client-side
- **Target state**: Single `GET /api/v2/sbom/{id}/advisory-summary` call returns severity counts directly
- **Goal statements**:
  - Reduce advisory summary load time from ~2s (multi-page fetch) to <200ms (single call)
  - Eliminate client-side counting logic from the dashboard

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical: N, high: N, medium: N, low: N, total: N }` | Counts only unique advisories (deduplicate by advisory ID) | Yes |
| Endpoint returns 404 if SBOM ID does not exist | Consistent with existing SBOM endpoints | Yes |
| Response is cached for 5 minutes | Use existing cache infrastructure | Yes |
| Support optional `?threshold=critical` query param to filter counts above a severity | Useful for alerting integrations | No |

## Non-Functional Requirements

- Response time: p95 < 200ms for SBOMs with up to 500 advisories
- No new database tables — use existing advisory-SBOM relationship tables
- Cache invalidation: advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM

## Use Cases (User Experience & Workflow)

### UC-1: Dashboard severity widget

**Persona**: Platform user viewing an SBOM detail page
**Pre-conditions**: SBOM has been ingested and advisories have been correlated
**Steps**:
1. User navigates to SBOM detail page
2. Dashboard widget calls `GET /api/v2/sbom/{id}/advisory-summary`
3. Widget renders severity breakdown bar chart

**Expected outcome**: Severity counts display within 200ms of page load

### UC-2: Alerting integration

**Persona**: External system polling for critical advisories
**Pre-conditions**: Integration configured with SBOM ID and severity threshold
**Steps**:
1. Integration calls `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical`
2. If `critical > 0`, integration triggers an alert

**Expected outcome**: Only critical count is returned when threshold filter is applied

## Customer Considerations

- No new prerequisites — uses existing SBOM and advisory data
- Requires advisory correlation to have completed for the target SBOM

## Customer Information/Supportability

- Add the new endpoint to the API latency Grafana dashboard
- Alert if p95 exceeds 500ms

## Documentation Considerations

- **Doc Impact**: Updates — add endpoint to REST API reference
- **User purpose**: API consumers need to know the endpoint path, parameters, and response shape
- **Reference material**: Existing SBOM advisory endpoints documentation
