# Task 6: Documentation for remediation dashboard and API endpoints

**Epic**: TC-9006: trustify-ui

## Repository

trustify-ui

## Target Branch

main

## Description

Create documentation for the new remediation tracking dashboard and its supporting API endpoints. This includes a user guide for the dashboard page explaining summary cards, progress chart, and filterable table, as well as API reference documentation for the `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` endpoints. The feature's Documentation Considerations specify "New Content" doc impact for both security team users and API consumers.

## Acceptance Criteria

- [ ] User guide documents the remediation dashboard page layout: summary cards, progress chart, filterable table
- [ ] User guide explains filtering by severity, product, and status
- [ ] API reference documents `GET /api/v2/remediation/summary` request/response format
- [ ] API reference documents `GET /api/v2/remediation/by-product` request/response format with pagination
- [ ] Documentation covers the use case of security managers tracking remediation SLAs
- [ ] Documentation covers the use case of engineering leads filtering by product for prioritization

## Test Requirements

- Review documentation for accuracy against implemented endpoints and UI components
- Verify all API request/response examples match actual endpoint behavior
