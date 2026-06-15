trustify-backend:
  changes:
    - Create PostgreSQL enum type `advisory_status_enum` with values (New, Analyzing, Fixed, Rejected)
    - Add `status` enum column to `advisory` table, backfill from `status_id` join, drop `status_id` FK column, drop `advisory_status` lookup table (single atomic migration)
    - Update SeaORM entity `entity/src/advisory.rs` to replace `status_id` foreign key with `status` enum field
    - Remove SeaORM entity file for the `advisory_status` lookup table
    - Update `modules/fundamental/src/advisory/service/advisory.rs` to query `status` column directly instead of joining `advisory_status`
    - Update `modules/fundamental/src/advisory/model/summary.rs` and `modules/fundamental/src/advisory/model/details.rs` to use enum status field
    - Update `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/get.rs` to filter/return enum status
    - Update `modules/ingestor/src/graph/advisory/mod.rs` to write enum values directly instead of inserting into lookup table
    - Update `common/src/db/query.rs` if advisory status filtering helpers exist
    - Add/update integration tests in `tests/api/advisory.rs` for enum-based status filtering

Workflow mode: feature-branch
Rationale: The migration and code changes have strict atomicity constraints — merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist. All changes must land together in a single atomic merge to main.

Label: workflow:feature-branch (to be applied to TC-9005)
