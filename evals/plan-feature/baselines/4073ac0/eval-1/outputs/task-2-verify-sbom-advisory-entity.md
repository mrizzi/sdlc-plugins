## Repository
trustify-backend

## Target Branch
main

## Description
Verify that the existing `sbom_advisory` join table entity in `entity/src/sbom_advisory.rs` has the necessary columns and relationships to support severity aggregation queries. The advisory severity field is expected to exist on the `advisory` entity (`entity/src/advisory.rs`). Confirm that the join between `sbom_advisory` and `advisory` provides access to the severity field needed for GROUP BY counting. If the entity lacks any required relation or column, add it.

## Files to Modify
- `entity/src/sbom_advisory.rs` — Verify join table entity has the necessary relations to the advisory entity for severity access
- `entity/src/advisory.rs` — Verify the advisory entity has a severity field suitable for aggregation

## Implementation Notes
The `entity/src/sbom_advisory.rs` file defines the SeaORM entity for the SBOM-Advisory join table. The `entity/src/advisory.rs` file defines the Advisory entity which should include a severity field (as indicated by `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` which "includes severity field" per the repo structure).

Inspect both entities to confirm:
1. `sbom_advisory` has foreign keys to both `sbom` and `advisory` tables
2. `advisory` has a `severity` column (likely an enum or string type)
3. SeaORM `Relation` definitions exist so a join query can be built

Per CONVENTIONS.md §Framework: use SeaORM entity patterns consistent with existing entities.
Applies: task modifies `entity/src/sbom_advisory.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `entity/src/sbom_advisory.rs` — Existing join table entity to verify/extend
- `entity/src/advisory.rs` — Advisory entity with severity field to verify
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Shows how the severity field is used in the model layer

## Acceptance Criteria
- [ ] `sbom_advisory` entity has relations to both `sbom` and `advisory` entities
- [ ] `advisory` entity has a severity column accessible via SeaORM
- [ ] A join query from `sbom_advisory` to `advisory` can access the severity field
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify entity relations compile and are consistent with the database schema