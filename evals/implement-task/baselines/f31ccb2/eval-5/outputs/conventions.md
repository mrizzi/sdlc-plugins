# Discovered Conventions

Conventions discovered from sibling analysis and repository structure inspection for task TC-9205.

## Production Code Conventions (from sibling migration analysis)

### Migration module structure
- **Directory naming**: Migrations follow the `m<NNNN>_<snake_case_description>` pattern (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **File structure**: Each migration is a directory containing a `mod.rs` file
- **Sequential numbering**: Migration numbers are zero-padded to 4 digits and increment sequentially

### Migration implementation pattern
- **Trait**: All migrations implement `MigrationTrait` from `sea_orm_migration`
- **Derive macro**: Migration structs use `#[derive(DeriveMigrationName)]` for automatic name generation from the module path
- **Async trait**: Methods use `#[async_trait::async_trait]` attribute
- **Required methods**: `up()` and `down()` returning `Result<(), DbErr>`
- **Self-contained identifiers**: Each migration defines its own `DeriveIden` enum for table/column references rather than importing from the entity crate (ensures migrations remain stable even as entities evolve)

### Import style
- **Prelude import**: Migrations use `use sea_orm_migration::prelude::*;` as the primary import

### Migration registration
- **Module declaration**: Each migration module is declared with `mod <module_name>;` in `migration/src/lib.rs`
- **Registration pattern**: Migrations are registered in a `migrations()` function using `vec![Box::new(<module>::Migration)]`
- **Ordering**: Migrations appear in chronological order in the vector

### Error handling
- **Return type**: All migration methods return `Result<(), DbErr>` -- SeaORM's standard database error type
- **Propagation**: Errors are propagated using `.await` with `?` -- no custom error wrapping in migrations

## Framework and Tooling Conventions (from repository structure)

- **Framework**: Axum for HTTP, SeaORM for database ORM
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Entity code**: Entity definitions live in `entity/src/` with one file per table
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database

## Test Conventions (from repository structure analysis)

- **Test location**: Integration tests live in `tests/api/` -- migration tests would be tested as part of the advisory endpoint tests or via direct database assertions
- **Test database**: Tests run against a real PostgreSQL test database, meaning migration execution is validated implicitly when the test database is set up
- **Test naming**: Tests follow `test_<action>_<scenario>` pattern based on test file conventions

## Branch and Commit Conventions

- **Commit format**: Conventional Commits -- `type(scope): description`
- **Commit trailer**: `--trailer="Assisted-by: Claude Code"` is required (constraint 2.3)
- **Jira reference**: Commit body must include `Implements <JIRA-ID>` (constraint 2.1)
- **Branch naming**: Task branches are named after the Jira issue ID (e.g., `TC-9205`) per constraint 3.1
- **Feature branch workflow**: When the Target Branch is a feature branch (e.g., `TC-9005`), the task branch is created from it and the PR targets it with `--base <target-branch>`

## CONVENTIONS.md

The repository may have a `CONVENTIONS.md` file at the root. During actual implementation, this file would be read to extract:
- Any CI check commands for verification
- Any code generation commands (e.g., `cargo fmt`, `cargo clippy`)
- Project-specific naming or structural conventions beyond what sibling analysis reveals
- Migration-specific guidance or conventions
