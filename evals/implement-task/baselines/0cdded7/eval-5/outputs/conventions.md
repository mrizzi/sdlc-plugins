# Conventions Discovered from Sibling Analysis

## Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

1. **Module naming**: Migrations use the pattern `m{NNNN}_{snake_case_description}/mod.rs` where `NNNN` is a zero-padded sequential number. The next migration would be `m0002_drop_advisory_status/mod.rs`.

2. **Trait implementation**: Each migration module implements `MigrationTrait` from SeaORM, providing:
   - `fn name(&self) -> &str` returning a descriptive migration name
   - `async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr>` for the forward migration
   - `async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr>` for the rollback

3. **Migration registration**: Migrations are registered in `migration/src/lib.rs` by adding an instance to the `vec![]` returned by the `migrations()` function on the `Migrator` struct. Each entry follows the pattern `Box::new(m0001_initial::Migration)`.

4. **Module declaration**: New migration modules are declared with `mod m0002_drop_advisory_status;` in `migration/src/lib.rs`.

## Entity Conventions (from `entity/src/advisory.rs`)

1. **SeaORM entity pattern**: Entity files define a `Model` struct with `DeriveEntityModel`, a `Column` enum, and `Relation` enum. The `Column` enum lists all database columns.
2. **Table/Column enum**: An enum (e.g., `Advisory`) with variants for `Table` and each column name (e.g., `Status`, `Severity`) is used in migration statements to reference table and column identifiers type-safely.

## General Codebase Conventions

1. **Framework**: Axum for HTTP, SeaORM for database ORM and migrations
2. **Error handling**: All functions return `Result<T, DbErr>` (migrations) or `Result<T, AppError>` (handlers) with `.context()` wrapping
3. **Module structure**: Domain modules follow `model/ + service/ + endpoints/` structure
4. **Rust edition**: Standard Rust project with Cargo workspace
5. **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database

## Commit Message Conventions

1. **Format**: Conventional Commits -- `type(scope): description`
2. **Trailer**: Include `Assisted-by: Claude Code` trailer
3. **Footer**: Reference the Jira task key (e.g., `Refs: TC-9205`)

## Branch Conventions

1. **Task branches**: Named after the Jira issue key (e.g., `TC-9205`)
2. **Feature branches**: Named after the parent feature issue key (e.g., `TC-9005`)
3. **Target Branch**: When a task specifies a Target Branch, branch from and PR into that branch, not `main`
