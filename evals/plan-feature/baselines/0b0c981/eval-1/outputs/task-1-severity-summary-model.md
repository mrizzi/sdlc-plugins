## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct to the SBOM model module. This struct represents the response shape for the new advisory severity aggregation endpoint (`GET /api/v2/sbom/{id}/advisory-summary`). It contains fields for each severity level count (critical, high, medium, low) and a total count. The struct must derive `Serialize` and `Deserialize` for JSON serialization via Axum, consistent with existing model structs in the module.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New file defining the `AdvisorySeveritySummary` struct with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }` (this task creates the response type; the endpoint handler is a separate task)

## Implementation Notes
Follow the existing model struct pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). Both files show the standard pattern: derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and use `utoipa::ToSchema` for OpenAPI spec generation.

Define the struct as:

```rust
#[derive(Clone, Debug, Serialize, Deserialize, ToSchema)]
pub struct AdvisorySeveritySummary {
    pub critical: u64,
    pub high: u64,
    pub medium: u64,
    pub low: u64,
    pub total: u64,
}
```

The severity field values should align with the severity enum used in `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`), which includes a `severity` field. Inspect that file to confirm the exact severity enum values and ensure the model field names match.

Per constraints §5.2: inspect the existing model files before creating the new one.
Per constraints §5.3: follow the patterns referenced in these Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Existing SBOM model struct demonstrating the standard derive macros, field naming, and module re-export pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition; inspect to align severity level naming

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with expected field names using a unit test
- [ ] Verify the struct can be deserialized from JSON with expected field names using a unit test

## Verification Commands
- `cargo check -p trustify-fundamental` — expected: compiles without errors


[sdlc-workflow] Description digest: sha256:a6d082226a7c6c177351f57cf2a27b538fe28d65633372914db1dbabbd017e81
