# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

Create a new SeaORM migration that drops the deprecated `status` column from the `advisory` table.

## Pre-Implementation Inspection

Before creating this file, inspect the sibling migration to understand the exact pattern:

1. `mcp__serena_backend__get_symbols_overview` on `migration/src/m0001_initial/mod.rs` to see its structure
2. `mcp__serena_backend__find_symbol` on the `Migration` struct and `MigrationTrait` impl with `include_body=true` to read the full implementation pattern
3. Also inspect `entity/src/advisory.rs` using `mcp__serena_backend__get_symbols_overview` to verify that the `Advisory` entity no longer includes a `status` field, confirming it is safe to drop the column

## File Content

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
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

    /// Re-adds the `status` column as a nullable string to allow rollback.
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

/// Iden enum for the advisory table and its columns used by this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`#[derive(DeriveMigrationName)]`** — Follows the SeaORM convention for auto-generating migration names from the module path, matching the pattern in `m0001_initial`.

2. **`up` method** — Uses `TableAlterStatement` to drop the column, as specified in the Implementation Notes. This is the standard SeaORM approach for schema alterations.

3. **`down` method** — Re-adds the column as `string().null()` to allow rollback without data loss. The column is nullable since any data that existed before the migration would be lost.

4. **Local `Advisory` Iden enum** — Defines a local `Iden` enum for the table and column identifiers used in this migration, rather than importing from the entity crate. This is the standard practice for migrations since entity definitions can change over time, but migration files must remain stable.

5. **Documentation comments** — Every public struct and method has a `///` doc comment explaining its purpose, following the skill's code quality practices.

## Convention Adherence

- File structure matches `m0001_initial/mod.rs` (struct + MigrationTrait impl)
- Uses `async_trait` for the async trait implementation
- Uses `Result<(), DbErr>` return type consistent with SeaORM patterns
- Module directory naming follows `m<NNNN>_<descriptive_name>` pattern
