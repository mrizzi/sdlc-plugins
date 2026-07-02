# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This column was replaced by the `severity` enum field in a previous migration and is no longer referenced by any service or entity code.

## Detailed Changes

Create a new file at `migration/src/m0002_drop_advisory_status/mod.rs` with the following structure:

### Imports

```rust
use sea_orm_migration::prelude::*;
```

Following the same import pattern as `m0001_initial/mod.rs`.

### Migration struct

```rust
/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was superseded by the `severity` enum field added in a
/// previous migration. No service or entity code references it.
#[derive(DeriveMigrationName)]
pub struct Migration;
```

A unit struct with `#[derive(DeriveMigrationName)]` to auto-generate the migration name from the module path. Includes a documentation comment explaining the purpose.

### MigrationTrait implementation

```rust
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
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}
```

- **`up()` method**: Uses `Table::alter()` builder to drop the `status` column from the `advisory` table. The `Advisory::Table` and `Advisory::Status` enum variants are used as identifiers (following SeaORM conventions). Errors propagate via `?` / `Result<(), DbErr>`.
- **`down()` method**: Re-adds the column as a nullable string (`ColumnDef::new(Advisory::Status).string().null()`) to allow rollback. The column is nullable so that existing rows (which lost their `status` value during `up()`) do not fail a NOT NULL constraint.

### Column identifier enum

A local enum to provide the table/column identifiers used in the migration:

```rust
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

This is a standard SeaORM pattern for referencing table and column names in migrations without depending on the entity module. The `#[derive(Iden)]` macro converts PascalCase variants to snake_case SQL identifiers (`Advisory` -> `advisory`, `Status` -> `status`).

## Conventions Applied

- Follows the exact module structure of `m0001_initial/mod.rs`
- Uses SeaORM enum identifiers rather than raw strings for table/column names
- Unit struct with `#[derive(DeriveMigrationName)]`
- `async_trait` for the trait implementation
- Builder pattern with `.to_owned()` termination
- Documentation comments on the struct and both methods
