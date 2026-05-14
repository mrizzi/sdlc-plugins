# Conventions Discovered from Sibling Analysis

These conventions would be discovered by inspecting sibling files in the `migration/src/` directory and related entity files in `entity/src/`.

## Migration Module Conventions

**Source: `migration/src/m0001_initial/mod.rs` (sibling migration)**

- **Module naming**: Migration modules follow the pattern `m{NNNN}_{description}/mod.rs` where `{NNNN}` is a zero-padded sequential number and `{description}` is a snake_case description of the migration's purpose.
- **Struct naming**: Each migration module exports a public `Migration` struct with `#[derive(DeriveMigrationName)]` for automatic name derivation from the module path.
- **Trait implementation**: Migrations implement `MigrationTrait` using `#[async_trait::async_trait]`, with both `up()` and `down()` methods required.
- **Return type**: Both `up()` and `down()` return `Result<(), DbErr>`.
- **Table/column identifiers**: Migrations define local `#[derive(Iden)]` enums for table and column names rather than importing from entity modules. This decouples migrations from the current entity state (important since entities may have already been updated to reflect the post-migration schema).
- **Imports**: Migrations use `use sea_orm_migration::prelude::*;` as the standard import.

## Migration Registration Conventions

**Source: `migration/src/lib.rs`**

- **Module declarations**: Each migration module is declared with `mod m{NNNN}_{description};` in numerical order.
- **Registration**: Migrations are registered in a `migrations()` function that returns `Vec<Box<dyn MigrationTrait>>`. Each entry is `Box::new(<module>::Migration)`.
- **Ordering**: Entries in the `vec![]` follow the same numerical order as the module declarations. Execution order matches declaration order.

## Entity Conventions

**Source: `entity/src/advisory.rs` (related entity)**

- **Column references**: Entity files define an enum with variants for each active column. When a column is deprecated and removed via migration, the entity enum should no longer include that variant — this is verified as a precondition before implementing the migration.

## General Rust Conventions

- **Error handling**: SeaORM migrations propagate errors via `Result` return types with `?` operator.
- **Async patterns**: All migration methods are `async` and use `.await` for database operations.
- **Documentation**: Migration structs and methods should include doc comments describing the migration's purpose and its reversibility.

## Test Conventions

No sibling test files were identified for migrations specifically. Test requirements from the task description indicate:
- Migration forward execution should be tested against a test database
- Migration rollback (down) should be tested to verify column re-addition
- Existing advisory queries should be verified to still work after column removal
