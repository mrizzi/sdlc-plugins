# Discovered Conventions

## Conventions from CONVENTIONS.md Lookup

The repository includes a `CONVENTIONS.md` at the root. Its contents would be read during Step 4 to extract:
- Project-level naming rules and directory structure conventions
- CI check commands (formatting, linting, compilation checks)
- Code generation commands (if any)

These commands would be recorded and executed during Step 9's CI verification sub-step.

## Discovered Conventions from Sibling Analysis

### Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

- **Module naming:** Migration modules follow the `m<NNNN>_<descriptive_name>` naming pattern with zero-padded sequential numbering (e.g., `m0001_initial`, `m0002_drop_advisory_status`)
- **Directory structure:** Each migration lives in its own directory under `migration/src/` with a single `mod.rs` file
- **Struct naming:** All migration modules export a `pub struct Migration` with `#[derive(DeriveMigrationName)]`
- **Trait implementation:** Migrations implement `MigrationTrait` using `#[async_trait::async_trait]`
- **Method signatures:** Both `up` and `down` methods take `&self` and `&SchemaManager` and return `Result<(), DbErr>`
- **Registration pattern:** Migrations are registered in `migration/src/lib.rs` via `Box::new(<module>::Migration)` inside the `migrations()` function's `vec![]`
- **Column identifiers:** Migrations define local `Iden` enums for table and column names rather than importing from entity crate, ensuring migration stability independent of entity evolution

### Entity Conventions (from `entity/src/advisory.rs` and siblings)

- **Framework:** SeaORM for all database entities
- **Entity location:** All entity definitions reside in `entity/src/<entity_name>.rs`
- **Entity structure:** Each entity file defines a Model struct with SeaORM derive macros

### General Code Conventions (from repository key conventions)

- **Framework:** Axum for HTTP, SeaORM for database
- **Module pattern:** Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)
- **Response types:** List endpoints return `PaginatedResults<T>`
- **Testing:** Integration tests in `tests/api/` use a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern

### Test Conventions (from `tests/api/advisory.rs` and siblings)

- **Assertion style:** All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- **Test setup:** Tests use a real PostgreSQL test database; setup creates test data before assertions
- **Error cases:** Endpoint tests include tests for 404/not-found scenarios

## Convention Conflicts

No conflicts detected between the task's Implementation Notes and the discovered conventions. The Implementation Notes explicitly reference the `m0001_initial` pattern, which aligns with all discovered migration conventions.
