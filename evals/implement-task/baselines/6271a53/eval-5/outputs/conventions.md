# Conventions Discovered from Sibling Analysis

## Source of Convention Analysis

Primary sibling: `migration/src/m0001_initial/mod.rs` -- the only existing migration module, serving as the canonical pattern for all new migrations.

Secondary references: `migration/src/lib.rs` for registration patterns, `entity/src/advisory.rs` for entity-column alignment verification.

---

## Migration Module Conventions

### 1. Module Naming Convention
- Migration modules follow the pattern `m{NNNN}_{descriptive_name}` where `NNNN` is a zero-padded sequential number
- Example: `m0001_initial` -> next migration: `m0002_drop_advisory_status`
- Each migration is a directory with a `mod.rs` file inside

### 2. Migration Struct Pattern
- Each migration module exports a `pub struct Migration;` (unit struct)
- The struct derives `DeriveMigrationName` (to be confirmed during inspection) or implements `fn name() -> &'static str` manually
- The naming convention for the migration name string should match whatever `m0001_initial` uses

### 3. MigrationTrait Implementation
- Implements `MigrationTrait` from `sea_orm_migration::prelude::*`
- Uses `#[async_trait::async_trait]` attribute (to be confirmed -- may use a re-exported version)
- Both `up` and `down` methods are implemented (never just `up` alone)
- Methods return `Result<(), DbErr>`

### 4. Table/Column Identifiers
- Migrations define their own `#[derive(Iden)] enum` for table and column names rather than importing from the entity crate
- This ensures migrations remain self-contained and are not affected by future entity changes
- The enum variants use PascalCase (e.g., `Table`, `Status`) and SeaORM's `Iden` derive maps them to snake_case SQL identifiers

### 5. Import Style
- Standard prelude import: `use sea_orm_migration::prelude::*;`
- Additional imports as needed for specific operations

---

## Migration Registration Conventions (lib.rs)

### 6. Module Declaration Order
- Module declarations (`mod m0001_...;`) are listed in sequential order at the top of `lib.rs`

### 7. Migration List Order
- Migrations are added to a `vec![]` inside a `migrations()` function
- Each entry is wrapped in `Box::new(module_name::Migration)`
- Order matches the module declaration order (chronological)

### 8. MigratorTrait
- A struct (likely `Migrator`) implements `MigratorTrait` and returns the migration vec

---

## General Rust Conventions (from repository structure)

### 9. Code Organization
- Each major domain concept gets its own directory with `mod.rs`
- Service/endpoint/model separation within modules

### 10. Entity Pattern
- Entities in `entity/src/` define the current schema state
- Migrations in `migration/src/` define schema transitions
- Entity files should not reference dropped columns (verified: `advisory.rs` no longer references `status`)

---

## Conventions Requiring Confirmation During Inspection

The following items must be verified by reading `m0001_initial/mod.rs` before implementation:

- [ ] Whether `DeriveMigrationName` derive macro or manual `name()` is used
- [ ] Whether `#[async_trait::async_trait]` or a re-exported attribute is used
- [ ] Exact formatting: indentation style, trailing commas, line breaks in method chains
- [ ] Whether the `Iden` enum is defined at the top or bottom of the file
- [ ] Whether `pub` visibility is used on the enum or kept private
