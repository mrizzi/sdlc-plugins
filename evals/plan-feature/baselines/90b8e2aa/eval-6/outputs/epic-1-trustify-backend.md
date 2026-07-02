# Epic: TC-9006: trustify-backend

**Issue Type:** Epic (level-1)
**Parent:** TC-9006
**Labels:** ai-generated-jira
**Priority:** Major
**Fix Versions:** RHTPA 1.5.0

## Description

Backend implementation for the vulnerability remediation tracking dashboard. Adds a new remediation module with aggregation service and REST API endpoints that compute remediation status from existing advisory and SBOM data. Includes GET /api/v2/remediation/summary for severity-by-status aggregation and GET /api/v2/remediation/by-product for per-product breakdown, along with integration tests for both endpoints.
