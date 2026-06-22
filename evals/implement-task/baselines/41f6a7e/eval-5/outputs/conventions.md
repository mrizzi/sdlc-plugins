# Discovered Conventions from Sibling Analysis

## Production Code Conventions

### Migration Pattern (from `migration/src/m0001_initial/mod.rs`)

- **Structure**: Each migration lives in its own subdirectory under `migration/src/` named `m<NNNN>_<description>/mod.rs`
- **Trait implementation**: All migrations implement `MigrationTrait` with two required methods: `up` (apply) and `down` (rollback)
- **Registration**: Migrations are registered in `migration/src/lib.rs` by adding a `mod` declaration and appending `Box::new(<module>::Migration)` to the `vec![]` returned by the `migrations()` function
- **Naming**: Module names follow the pattern `m<sequence_number>_<snake_case_description>` (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Error handling**: Migration methods return `Result<(), DbErr>` using SeaORM's error type, with `await?` propagation

### SeaORM Conventions (from entity and migration code)

- **Table references**: Use SeaORM enum variants for table and column references (e.g., `Advisory::Table`, `Advisory::Status`) rather than raw strings
- **Alter table operations**: Use `Table::alter()` builder pattern with `.table()`, `.drop_column()` or `.add_column()`, and `.to_owned()` before passing to `manager.alter_table()`
- **Column definitions**: Use `ColumnDef::new()` with chained type and constraint methods (e.g., `.string().null()`)

### General Project Conventions

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Domain modules follow `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>`

## Test Conventions (from `tests/api/advisory.rs` and siblings)

- **Assertion style**: Integration tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test database**: Tests run against a real PostgreSQL test database (not mocks)
- **Test naming**: Tests follow `test_<action>_<scenario>` pattern
- **Test location**: Integration tests live in `tests/api/` directory, organized by domain entity
- **Migration testing**: Verify migration runs successfully, verify rollback re-adds the column, verify existing queries still work after the column is dropped

## CONVENTIONS.md

The repository contains a `CONVENTIONS.md` at the root. Its contents should be read during implementation to extract:
- Any CI check commands for Step 9 verification
- Any code generation commands that may produce artifacts to commit
- Any additional naming, directory structure, or code pattern conventions
