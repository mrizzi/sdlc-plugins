# Repository Impact Map — TC-9004: Add license compliance report endpoint

## trustify-backend

Changes:
- Add license policy configuration model and loader (JSON config file for defining allowed/denied licenses)
- Add license report service that aggregates package-license data from existing entities, groups by license type, walks transitive dependencies, and flags non-compliant licenses against the configured policy
- Add `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured compliance report grouped by license with policy violation flags
- Add integration tests for the license report endpoint covering compliant SBOMs, non-compliant SBOMs, transitive dependency resolution, and missing policy configuration
- Add API documentation for the license report endpoint and license policy configuration

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The feature is contained within a single repository (trustify-backend), introduces no schema migrations, does not break any existing API contracts, does not require cross-cutting refactors, and has no tightly coupled frontend/backend components. Each task can be merged independently without leaving `main` in a broken state.
