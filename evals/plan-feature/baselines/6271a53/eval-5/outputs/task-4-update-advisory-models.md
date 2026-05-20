## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory model structs (`AdvisorySummary` and `AdvisoryDetails`) to use the enum status directly instead of requiring a join to the `advisory_status` lookup table. The models should derive the status string from the `AdvisoryStatusEnum` value on the `advisory` entity, eliminating the need for a separate status struct or joined field.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- Replace any `status_id`-based or joined status field with a direct `status: String` (or `AdvisoryStatusEnum`) field derived from the advisory entity's enum column
- `modules/fundamental/src/advisory/model/details.rs` -- Same change as summary: use the enum status directly
- `modules/fundamental/src/advisory/model/mod.rs` -- Update any model re-exports or shared type definitions if they reference the old status join

## Implementation Notes
- The `AdvisorySummary` struct likely has a status field that is populated by joining the `advisory_status` table. Replace this with a field that reads directly from `advisory.status` (the new enum column)
- Follow the same struct pattern used in `SbomSummary` (`modules/fundamental/src/sbom/model/summary.rs`) for field definitions and serialization
- The status field in the API response must remain a `String` (e.g., "New", "Analyzing", "Fixed", "Rejected") to maintain backward compatibility -- the `AdvisoryStatusEnum` should be converted to a string for serialization
- If using serde, ensure the enum serializes to the same string values as the old lookup table returned (exact case match: "New" not "new")
- No API response shape changes -- the consumer-facing JSON remains identical

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs` -- Reference for model struct layout and serialization patterns
- `modules/fundamental/src/sbom/model/details.rs` -- Reference for details struct patterns

## Acceptance Criteria
- [ ] `AdvisorySummary` struct uses the enum status directly without requiring a join
- [ ] `AdvisoryDetails` struct uses the enum status directly without requiring a join
- [ ] Status field serializes to the same string values as before (backward compatible)
- [ ] `cargo check -p fundamental` compiles without errors

## Test Requirements
- [ ] Verify `AdvisorySummary` correctly maps the enum status to a string in serialization
- [ ] Verify `AdvisoryDetails` correctly maps the enum status to a string in serialization
- [ ] Verify backward compatibility: serialized JSON output matches the previous format

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
