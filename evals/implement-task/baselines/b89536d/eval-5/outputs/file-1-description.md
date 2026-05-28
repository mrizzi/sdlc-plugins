# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This is a new file. The full content would be:

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous migration
/// (m0001_initial) and is no longer read or written by any service or entity code.
/// Removing it reduces confusion and prevents accidental usage.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

#[async_trait::async_trait]
impl MigrationTrait for Migration {
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

/// Iden enum for the advisory table and its columns referenced by this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions Followed

- Follows the exact pattern from `m0001_initial/mod.rs` for struct definition, trait implementations, and SeaORM API usage
- Implements both `MigrationName` and `MigrationTrait`
- Uses `sea_orm_migration::prelude::*` import
- Defines a local `Iden` enum for the table and column identifiers used in this migration
- The `up` method uses `TableAlterStatement` with `drop_column` as specified in Implementation Notes
- The `down` method re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback, matching the Implementation Notes exactly
- Documentation comment on the struct explains the purpose and rationale
