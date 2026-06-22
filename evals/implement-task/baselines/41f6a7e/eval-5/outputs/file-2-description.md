# File 2: `migration/src/m0002_drop_advisory_status/mod.rs` (Create)

## Purpose

Create a new SeaORM migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Pre-Implementation Inspection

Before creating this file:
1. Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `Migration` struct and its `MigrationTrait` implementation in `migration/src/m0001_initial/mod.rs` to understand the exact pattern to follow
2. Verify that `entity/src/advisory.rs` does not reference a `status` column by inspecting it with `mcp__serena_backend__get_symbols_overview`
3. Search for any remaining references to `Advisory::Status` across the codebase using `mcp__serena_backend__search_for_pattern` to confirm it is safe to drop

## Detailed Implementation

The file follows the established migration pattern from `m0001_initial/mod.rs`:

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer referenced by any service or entity code.
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

    /// Re-adds the `status` column as a nullable string for rollback.
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

/// Enum referencing the `advisory` table and its columns for use with SeaORM's
/// schema builder.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Design Decisions

1. **`Advisory` enum defined locally**: The migration defines its own `Advisory` enum with `Table` and `Status` variants using `#[derive(Iden)]`. This is standard practice for migrations -- migrations should be self-contained and not depend on entity definitions that may change over time.

2. **Nullable string for rollback**: The `down` method re-adds the column as `.string().null()` -- nullable because after dropping and re-adding, existing rows will not have values for this column. This matches the Implementation Notes specification.

3. **SeaORM `TableAlterStatement`**: Uses `Table::alter()` builder pattern as specified in the Implementation Notes, which is consistent with the SeaORM migration API.

4. **Documentation comments**: Every public symbol and both `up`/`down` methods have documentation comments, following the skill's code quality practices requirement.

## Convention Conformance

- Follows the `m<NNNN>_<description>/mod.rs` directory naming pattern from `m0001_initial`
- Implements `MigrationName` and `MigrationTrait` matching the sibling migration
- Uses the same import structure (`sea_orm_migration::prelude::*`)
- Uses `async_trait` attribute on the impl block matching the sibling pattern
- Returns `Result<(), DbErr>` for both methods matching the trait contract
