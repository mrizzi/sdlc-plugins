# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

Create a new SeaORM migration that drops the deprecated `status` column from the `advisory` table. The `up` method removes the column, and the `down` method re-adds it as a nullable string for rollback capability.

## Pre-implementation Inspection

Before creating this file, use Serena to inspect the sibling migration `m0001_initial/mod.rs`:
- `mcp__serena_backend__get_symbols_overview` on `migration/src/m0001_initial/mod.rs` to see the struct and trait implementation structure
- `mcp__serena_backend__find_symbol` with `include_body=true` on the `Migration` struct, `up`, and `down` methods to see the exact implementation pattern

Also verify:
- `mcp__serena_backend__get_symbols_overview` on `entity/src/advisory.rs` to confirm no `Status` column enum variant exists in the entity
- `mcp__serena_backend__search_for_pattern` for `Advisory::Status` or `status` across the codebase to confirm no code references this column

## File Contents

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code.

use sea_orm_migration::prelude::*;

/// Migration that removes the unused `status` column from the advisory table.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the `status` column from the `advisory` table.
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .drop_column(Advisory::Status)
                    .to_owned(),
            )
            .await
    }

    /// Re-adds the `status` column as a nullable string for rollback.
    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}

/// Identifiers for the advisory table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`#[derive(DeriveMigrationName)]`** -- Follows the pattern from `m0001_initial` to auto-generate the migration name from the module path.

2. **`Advisory` enum with `DeriveIden`** -- Defined locally within this migration module (not imported from the entity crate) because the entity's `Advisory` enum no longer contains a `Status` variant. Migrations must be self-contained so they remain valid even as entities evolve.

3. **Nullable string in `down`** -- The rollback re-adds the column as `.string().null()` so that existing rows are not affected and the column can be repopulated if needed. This matches the implementation note in the task description.

4. **Documentation comments** -- Every public struct and method has a `///` doc comment explaining its purpose, per the SKILL.md code quality requirements.

## Conventions Followed

- Same struct name `Migration` as used in `m0001_initial`
- Same `use sea_orm_migration::prelude::*;` import
- Same `#[async_trait::async_trait]` attribute on the trait impl
- Same `Result<(), DbErr>` return type for `up` and `down`
- Local `DeriveIden` enum for table/column identifiers (self-contained migration)
- Module file placed at `migration/src/m0002_drop_advisory_status/mod.rs` following the directory-per-migration pattern
