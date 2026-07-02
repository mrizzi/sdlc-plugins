# File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: CREATE

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the exact pattern established by the sibling migration `m0001_initial/mod.rs`.

## Detailed Changes

### Full file content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
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

/// Entity reference enum for the advisory table, used by the migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Design decisions

1. **`up()` method**: Uses `Table::alter().drop_column()` as specified in the Implementation Notes. This issues an `ALTER TABLE advisory DROP COLUMN status` SQL statement.

2. **`down()` method**: Re-adds the column as `string().null()` to allow rollback. The column is nullable because existing rows would not have a value after re-adding. This matches the Implementation Notes specification.

3. **`Advisory` enum**: Defines a local `Iden` enum with `Table` and `Status` variants for type-safe references to the table and column names. This is the standard SeaORM pattern for migrations (the migration should not depend on the entity crate's column enum, since the entity may have already removed the `Status` variant).

4. **Documentation**: Includes a doc comment on the `Migration` struct and the `Advisory` enum explaining their purpose, following the code quality practices requirement.

### Conventions applied

- Follows the `m0001_initial/mod.rs` migration pattern exactly
- Uses `sea_orm_migration::prelude::*` import
- Implements `MigrationName` and `MigrationTrait` traits
- Uses `async_trait` attribute on the trait impl
- Error propagation via `Result<(), DbErr>` return type
