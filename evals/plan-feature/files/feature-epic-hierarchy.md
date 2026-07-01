<!-- SYNTHETIC TEST DATA — names, URLs, and identifiers are fictional -->

# Mock Jira Feature Issue

**Key**: TC-9006
**Summary**: Add vulnerability remediation tracking dashboard
**Status**: New
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0
**Labels**: ai-generated-jira
**Linked Issues**: None

---

## Feature Overview

Add a vulnerability remediation tracking dashboard that shows the progress of fixing known vulnerabilities across all ingested SBOMs. The backend provides aggregation endpoints for remediation status by severity and by product, while the frontend renders a dashboard page with summary cards, a progress chart, and a filterable table of outstanding vulnerabilities.

## Background and Strategic Fit

Security teams need visibility into remediation progress across the entire portfolio. Currently, users must navigate individual SBOM detail pages and manually tally vulnerability statuses. A centralized dashboard with backend aggregation reduces time-to-insight and supports management reporting on remediation SLAs.

## Goals

- **Who benefits**: Security managers tracking remediation SLAs, engineering leads prioritizing fix work
- **Current state**: No aggregated remediation view — users manually check individual SBOMs
- **Target state**: A dashboard page showing remediation progress with drill-down to individual vulnerabilities
- **Goal statements**:
  - Provide portfolio-wide remediation visibility in a single page
  - Enable filtering by severity, product, and remediation status

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| `GET /api/v2/remediation/summary` returns aggregated counts by severity and status | Groups by: severity (Critical/High/Medium/Low) × status (Open/In Progress/Resolved) | Yes |
| `GET /api/v2/remediation/by-product` returns per-product remediation breakdown | Each product entry includes total, open, resolved counts | Yes |
| Dashboard page at `/remediation` with summary cards and progress chart | Cards show total open, in-progress, resolved; chart shows trend over time | Yes |
| Filterable vulnerability table on the dashboard | Filter by severity, product, status | Yes |
| Export remediation report as CSV | For management reporting | No |

## Non-Functional Requirements

- Summary endpoint response time: p95 < 500ms
- Dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation
- No new database tables — compute aggregations from existing vulnerability and SBOM relationship data

## Use Cases (User Experience & Workflow)

### UC-1: View remediation summary

**Persona**: Security manager checking weekly remediation progress
**Pre-conditions**: Vulnerabilities have been correlated with ingested SBOMs
**Steps**:
1. User navigates to `/remediation`
2. Dashboard loads summary cards showing total Open, In Progress, and Resolved counts
3. Progress chart shows remediation trend over the past 30 days
4. User reviews the filterable table below for outstanding Critical vulnerabilities

**Expected outcome**: Full remediation status visible on a single page

### UC-2: Filter by product

**Persona**: Engineering lead prioritizing fix work for a specific product
**Pre-conditions**: Multiple products have ingested SBOMs with correlated vulnerabilities
**Steps**:
1. User navigates to `/remediation`
2. User selects a product from the product filter dropdown
3. Dashboard updates to show only vulnerabilities affecting that product
4. User sorts by severity to identify critical items first

**Expected outcome**: Product-specific remediation view for prioritization

## Customer Considerations

- Remediation status depends on advisory correlation being up to date
- Large portfolios (>50 products) may require pagination in the product breakdown

## Documentation Considerations

- **Doc Impact**: New Content — document the remediation dashboard and aggregation endpoints
- **User purpose**: Security teams need a guide for using the dashboard; API consumers need endpoint reference
