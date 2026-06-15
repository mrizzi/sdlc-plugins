# Discovered Conventions (from sibling analysis)

## Production Code Conventions

### Migration module structure
- Each migration lives in its own subdirectory under `migration/src/`, named with an
  incrementing prefix: `m0001_initial`, `m0002_drop_advisory_status`, etc.
- Each migration module contains a single `mod.rs` file.
- Migrations implement the `MigrationTrait` trait with `up` and `down` methods.

### Migration registration
- Migrations are registered in `migration/src/lib.rs` inside a `migrations()` function
  that returns a `Vec<Box<dyn MigrationTrait>>`.
- New migrations are appended to the `vec![]` in order.
- Each migration module is declared with `mod m000N_<name>;` at the top of `lib.rs`.

### SeaORM patterns
- Column operations use `TableAlterStatement` via `Table::alter()`.
- Drop column: `manager.alter_table(Table::alter().table(Entity::Table).drop_column(Entity::Column).to_owned()).await`
- Add column: `manager.alter_table(Table::alter().table(Entity::Table).add_column(ColumnDef::new(Entity::Column).<type>().<constraints>()).to_owned()).await`
- Rollback (`down`) re-adds dropped columns as nullable to avoid data-loss issues.

### Entity conventions
- SeaORM entities live in `entity/src/`, one file per database table.
- Entity files define an enum for column names (e.g., `Advisory::Status`, `Advisory::Table`).
- The `advisory.rs` entity no longer references the `status` column (it was previously removed
  from the entity definition when the `severity` enum field replaced it).

### Error handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`).

### Framework
- Axum for HTTP, SeaORM for database ORM.

### Naming
- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`).

## Test Conventions

### Integration tests
- Integration tests live in `tests/api/` and hit a real PostgreSQL test database.
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- Test naming follows `test_<endpoint>_<scenario>` pattern.
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields.
- Error case tests include a 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

### Migration tests
- Migration tests verify that `up` runs successfully against a test database.
- Migration tests verify that `down` (rollback) re-adds dropped columns.
- After migration, existing queries are tested to confirm they still work.
