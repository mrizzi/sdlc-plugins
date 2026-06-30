# Conventions Discovered from Sibling Analysis

## Migration Conventions (from m0001_initial/mod.rs)

The following conventions were identified by analyzing the existing migration at `migration/src/m0001_initial/mod.rs`:

1. **Module naming**: Migrations follow the pattern `m{NNNN}_{snake_case_description}/mod.rs` where NNNN is a zero-padded sequential number. The first migration is `m0001_initial`, so the next should be `m0002_drop_advisory_status`.

2. **Trait implementation**: Each migration implements `MigrationTrait` from SeaORM, which requires three methods:
   - `name()` — returns a string identifier for the migration
   - `up()` — applies the migration (forward)
   - `down()` — reverts the migration (rollback)

3. **Reversibility**: Migrations must be reversible. The `down()` method undoes what `up()` does, enabling safe rollback.

4. **SeaORM schema API**: Migrations use SeaORM's schema builder API (`Table::alter()`, `Table::create()`, `ColumnDef::new()`, etc.) rather than raw SQL, ensuring database-agnostic migrations.

5. **Entity enum references**: Table and column names are referenced via enum variants (e.g., `Advisory::Table`, `Advisory::Status`) rather than raw strings, providing type safety and consistency with the entity definitions.

## Migration Registration (from migration/src/lib.rs)

1. **Module declaration**: Each migration directory is declared as a `mod` in `lib.rs`.
2. **Migration vector**: All migrations are registered in a `migrations()` function that returns `Vec<Box<dyn MigrationTrait>>`, with each migration boxed as `Box::new(module_name::Migration)`.
3. **Ordering**: Migrations are listed in chronological/numerical order in the vector.

## Entity Conventions (from entity/src/advisory.rs)

1. **SeaORM entities**: Database tables are modeled as SeaORM entities in the `entity/` crate.
2. **Column mapping**: Each column in the database table corresponds to an enum variant and a struct field in the entity definition.
3. **Verification pattern**: Before dropping a column via migration, verify the corresponding entity no longer references it, confirming no service code depends on the column.

## General Repository Conventions (from repo structure)

1. **Module structure**: Domain modules follow `model/ + service/ + endpoints/` pattern.
2. **Error handling**: Functions return `Result<T, AppError>` using `.context()` wrapping.
3. **Framework stack**: Axum for HTTP, SeaORM for database ORM and migrations.
4. **Crate separation**: Distinct crates for `entity`, `migration`, `common`, `server`, and domain `modules`.
