# Repository Impact Map — TC-9004: Add License Compliance Report Endpoint

## trustify-backend

### Changes

- Add `LicenseReport` and `LicenseGroup` response model structs in a new `license_report` model module under `modules/fundamental/src/sbom/model/`
- Add license policy configuration: a JSON config file defining allowed/denied licenses and a Rust type to deserialize it
- Add `LicenseReportService` in `modules/fundamental/src/sbom/service/` to aggregate package-license data from the existing `package_license` entity, walk transitive dependencies via `sbom_package`, group by license, and flag non-compliant licenses against the configured policy
- Add `GET /api/v2/sbom/{id}/license-report` endpoint handler in `modules/fundamental/src/sbom/endpoints/`
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Add integration tests for the license report endpoint in `tests/api/`
- Update `README.md` to document the new endpoint and license policy configuration

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes land in a single repository (trustify-backend). The new endpoint is purely additive — it does not modify existing API contracts or database schema, and no other tasks depend on it. Each task can be merged independently without leaving `main` in a broken state.
