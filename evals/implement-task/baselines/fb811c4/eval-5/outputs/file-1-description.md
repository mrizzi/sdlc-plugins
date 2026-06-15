# File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

## Purpose

New migration file that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file implements the `MigrationTrait` following the exact pattern established by the sibling migration `m0001_initial/mod.rs`.

### Full file content

```rust
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the deprecated `status` column from the `advisory` table.
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
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}

/// Iden enum for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Design Decisions

1. **`#[derive(DeriveMigrationName)]`**: Follows SeaORM convention to auto-derive the migration name from the module path.
2. **`up` method**: Uses `TableAlterStatement` with `drop_column` as specified in the Implementation Notes.
3. **`down` method**: Re-adds the column as `string().null()` to allow rollback without data loss. The column is nullable because existing rows won't have values after rollback.
4. **`Advisory` Iden enum**: Defined locally within the migration module (not imported from `entity/src/advisory.rs`) because the entity module no longer contains the `Status` variant. Migrations must be self-contained to remain valid even as entity definitions evolve.
5. **Doc comments**: Added on both `up` and `down` methods per the skill's code quality practices requirement.
