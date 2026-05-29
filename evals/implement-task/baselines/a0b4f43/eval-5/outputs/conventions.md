# Conventions Discovered from Sibling Analysis

## Source: Repository Structure and Key Conventions (repo-backend.md)

The following conventions were identified from the repository structure and documented conventions in the trustify-backend repository.

### Production Code Conventions

- **Framework:** Axum for HTTP, SeaORM for database ORM and migrations
- **Module pattern:** Each domain module follows a `model/ + service/ + endpoints/` structure (observed in `modules/fundamental/src/sbom/`, `modules/fundamental/src/advisory/`, `modules/fundamental/src/package/`)
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)
- **Endpoint registration:** Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers:** Shared filtering, pagination, and sorting via `common/src/db/query.rs`

### Migration Conventions (from sibling: `migration/src/m0001_initial/mod.rs`)

- **Migration trait:** Each migration implements `MigrationTrait` with `up()` and `down()` methods
- **Migration naming:** Modules follow `m<NNNN>_<description>/mod.rs` pattern (e.g., `m0001_initial`)
- **Migration registration:** Migrations are registered in `migration/src/lib.rs` by adding to the `vec![]` in the `migrations()` function
- **Schema API:** Migrations use SeaORM's schema manager API (`TableAlterStatement`, `ColumnDef`, etc.)
- **Iden enums:** Table and column references use `#[derive(Iden)]` enums (pattern to be confirmed by reading `m0001_initial/mod.rs`)

### Entity Conventions (from sibling: `entity/src/advisory.rs` and siblings)

- **Entity definitions:** SeaORM entity files in `entity/src/` define the database schema model
- **Entity naming:** One file per entity (e.g., `advisory.rs`, `sbom.rs`, `package.rs`)
- **Join tables:** Separate entity files for join tables (e.g., `sbom_advisory.rs`, `sbom_package.rs`)

### Test Conventions (from: `tests/api/`)

- **Integration tests:** Tests in `tests/api/` hit a real PostgreSQL test database
- **Assertion pattern:** Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for response validation
- **Test organization:** One test file per domain module (e.g., `advisory.rs`, `sbom.rs`)
- **Naming convention:** Test files mirror the module names they test

### Caching Conventions

- **Middleware:** Uses `tower-http` caching middleware
- **Configuration:** Cache configuration is specified in endpoint route builders

## Conventions Relevant to TC-9205

For this migration task, the key binding conventions are:

1. **Follow `m0001_initial/mod.rs` exactly** for the `MigrationTrait` implementation structure
2. **Use the `migrations()` vec pattern** in `lib.rs` to register the new migration
3. **Maintain chronological ordering** of migrations in the vec (m0002 after m0001)
4. **Use SeaORM's `TableAlterStatement`** for schema changes (as specified in Implementation Notes and confirmed by framework convention)
5. **Use `#[derive(Iden)]` enums** for type-safe table/column references (to be confirmed by sibling inspection)
