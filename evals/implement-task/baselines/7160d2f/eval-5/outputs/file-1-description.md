# File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This follows the existing migration pattern established by `m0001_initial/mod.rs`.

## Detailed Implementation

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Apply the migration: drop the deprecated `status` column from the `advisory` table.
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

    /// Rollback the migration: re-add the `status` column as a nullable string.
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

/// Enum identifying the `advisory` table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions Applied

- **Follows `m0001_initial/mod.rs` pattern:** Implements `MigrationTrait` with `up` and `down` async methods.
- **Uses `DeriveMigrationName`:** Automatically derives the migration name from the module path, matching the sibling migration pattern.
- **SeaORM `TableAlterStatement`:** Uses the fluent API (`Table::alter().table(...).drop_column(...)`) as specified in the Implementation Notes.
- **Enum-based identifiers:** Defines a local `Advisory` enum with `#[derive(Iden)]` for type-safe table/column references, rather than raw strings.
- **Rollback support:** The `down` method re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` -- nullable string to allow safe rollback without data loss concerns.
- **Documentation comments:** Both `up` and `down` methods have doc comments explaining their purpose. The `Advisory` enum also has a doc comment.

## Directory Structure

Creates a new directory `migration/src/m0002_drop_advisory_status/` with a single file `mod.rs`. This follows the naming convention `m<NNNN>_<descriptive_name>/` established by `m0001_initial/`.
