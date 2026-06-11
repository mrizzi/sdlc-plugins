# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the pattern established by the sibling migration `m0001_initial/mod.rs`.

## Detailed Implementation

This file implements the `MigrationTrait` for a SeaORM migration. The implementation follows the existing migration pattern in `m0001_initial/mod.rs`.

### Full file content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drop the `status` column from the `advisory` table.
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

    /// Re-add the `status` column as a nullable string to allow rollback.
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

/// Enum identifying the advisory table and its columns for use in migration statements.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **`#[derive(DeriveMigrationName)]`**: Uses SeaORM's derive macro to automatically generate the migration name from the module path, following the pattern in `m0001_initial`.

2. **`Advisory` Iden enum**: Defines a local `Iden` enum for the table and column names. This is standard SeaORM migration practice — the migration defines its own identifiers rather than importing from the entity module, ensuring the migration remains self-contained and reproducible regardless of future entity changes.

3. **`up()` method**: Uses `TableAlterStatement` to drop the `status` column, as specified in the Implementation Notes.

4. **`down()` method**: Re-adds the column as a nullable string (`string().null()`), allowing rollback without data loss concerns. The column is nullable because there would be no data to populate it after rollback.

5. **Documentation comments**: Every public symbol and method has a doc comment (`///`) explaining its purpose, following the skill's code quality practices.

### Conventions Followed

- Implements `MigrationTrait` with both `up` and `down` methods (contract completeness)
- Uses `async_trait` attribute macro (matching sibling pattern)
- Uses `SchemaManager` parameter pattern (matching sibling)
- Returns `Result<(), DbErr>` (matching sibling error handling)
- Uses `.to_owned()` on builder to finalize the statement (matching SeaORM convention)
- File placed in `migration/src/m0002_drop_advisory_status/mod.rs` following the `m<NNNN>_<descriptive_name>/mod.rs` naming convention
