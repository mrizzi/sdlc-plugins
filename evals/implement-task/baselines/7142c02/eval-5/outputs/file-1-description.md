# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Pre-Implementation Inspection

Before writing this file, read the sibling migration `migration/src/m0001_initial/mod.rs` to understand:
- How `MigrationTrait` is implemented (struct definition, trait impl)
- How `up` and `down` methods are structured
- How `MigrationName` is implemented (naming convention)
- Import patterns and module organization
- How `Table::alter()` and column operations are used (if present), or how `TableCreateStatement` is structured for reference

Also read `entity/src/advisory.rs` to confirm:
- The `Advisory` entity enum exists and has a `Table` variant
- The `Status` column variant exists in the enum (needed for the migration to reference it) OR determine what identifier to use
- The entity no longer actively uses `status` in its column definitions

## Detailed Implementation

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drop the deprecated `status` column from the `advisory` table.
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

    /// Re-add the `status` column as a nullable string for rollback.
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
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions Followed

- Follows the same structure as `m0001_initial/mod.rs` (sibling migration pattern)
- Uses `#[derive(DeriveMigrationName)]` for automatic migration naming
- Uses `async_trait` for the `MigrationTrait` implementation
- Defines a local `Iden` enum for table/column identifiers (scoped to this migration, not importing from entity crate -- this is the standard SeaORM migration pattern to avoid coupling migrations to entity definitions that may change)
- Documentation comments on both `up` and `down` methods explaining their purpose
- The `down` method re-adds the column as nullable string to allow safe rollback without data loss concerns

## Acceptance Criteria Coverage

- [x] Migration drops the `status` column from the `advisory` table (via `up` method)
- [x] Migration `down` method re-adds the column as nullable string for rollback
