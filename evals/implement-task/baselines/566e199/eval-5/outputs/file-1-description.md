# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration file that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file would be created following the exact pattern observed in the sibling migration
`migration/src/m0001_initial/mod.rs`. The structure follows SeaORM's migration pattern:

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

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

    /// Re-adds the `status` column as a nullable string for rollback support.
    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .add_column(
                        ColumnDef::new(Advisory::Status)
                            .string()
                            .null()
                            .to_owned(),
                    )
                    .to_owned(),
            )
            .await
    }
}

/// Enum identifiers for the advisory table and its columns, used by SeaORM's
/// schema alteration API.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **`Advisory` enum defined locally**: The `Iden` enum for `Advisory::Table` and `Advisory::Status` is defined within the migration module itself (not imported from the entity crate). This follows standard SeaORM migration practice -- migrations must be self-contained and not depend on the entity crate, which may change over time.

2. **`down` method re-adds as nullable string**: Per the Implementation Notes, the rollback adds the column back as `.string().null()` so that existing rows do not fail the migration rollback (no NOT NULL constraint on a column with no data).

3. **Naming convention**: The migration module name `m0002_drop_advisory_status` follows the sequential numbering pattern established by `m0001_initial`.

4. **Documentation comments**: Every public symbol and both `up`/`down` methods have doc comments explaining what they do, per the skill's code quality requirements.
