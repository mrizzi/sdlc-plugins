# File 3: Verification -- `entity/src/advisory.rs`

## Action: VERIFY ONLY (no modifications)

## Purpose

Confirm that the `advisory` entity definition no longer references the `status` column. This is a prerequisite check from the Implementation Notes: "The advisory entity in `entity/src/advisory.rs` no longer references the `status` column -- verify this before proceeding."

## Verification steps

1. Read `entity/src/advisory.rs` using Serena's `get_symbols_overview` to see all fields/columns defined on the entity
2. Confirm that no `Status` variant exists in the entity's column enum
3. Confirm that no `status` field exists in the entity's Model struct
4. If `status` is still referenced, stop and report to the user -- the entity must be updated before this migration can safely drop the column

## Additional cross-codebase verification

Search for any remaining references to the `status` column on the `advisory` table across the entire codebase:

- `modules/fundamental/src/advisory/service/advisory.rs` -- verify no query filters or selects on `status`
- `modules/fundamental/src/advisory/model/summary.rs` -- verify `AdvisorySummary` does not include `status`
- `modules/fundamental/src/advisory/model/details.rs` -- verify `AdvisoryDetails` does not include `status`
- `modules/fundamental/src/advisory/endpoints/list.rs` -- verify no filtering on `status`
- `modules/fundamental/src/advisory/endpoints/get.rs` -- verify no mapping of `status`
- `modules/ingestor/src/graph/advisory/mod.rs` -- verify ingestion does not write to `status`
- `tests/api/advisory.rs` -- verify tests do not assert on `status` field

Use Grep to search for patterns like `Advisory::Status`, `advisory.status`, `.status`, `"status"` scoped to advisory-related code.

## Acceptance criteria addressed

- No service or entity code references the `status` column
