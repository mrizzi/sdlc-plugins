# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the exact pattern established by `migration/src/m0001_initial/mod.rs`.

## Detailed Changes

Create a new file implementing `MigrationTrait` from SeaORM with `up` and `down` methods.

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
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

/// Enum identifying the `advisory` table and its columns for use in SeaORM migration statements.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Implementation Decisions

1. **Follow the m0001_initial pattern**: The migration struct implements `MigrationTrait` with async `up` and `down` methods, matching the exact pattern from the existing migration.

2. **`up` method**: Uses `TableAlterStatement` via `Table::alter()` to drop the `status` column, as specified in the Implementation Notes.

3. **`down` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback. The column is nullable so that existing rows (which will have no status value after dropping) are valid after rollback.

4. **`Iden` enum**: Defines `Advisory::Table` and `Advisory::Status` identifiers for use in the migration statements. This is the standard SeaORM pattern for referencing tables and columns in migration code.

5. **Documentation**: Every public symbol has a doc comment explaining its purpose, following the skill's code quality requirements.
