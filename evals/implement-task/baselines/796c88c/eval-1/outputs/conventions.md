# Discovered Conventions — TC-9201

## Conventions from Sibling Analysis

### Production Code Conventions

**Module structure:**
- Each domain module follows `model/ + service/ + endpoints/` structure
- Models are in separate files under `model/`, registered via `pub mod <name>;` in `model/mod.rs`
- Services are in separate files under `service/`, with the main service struct (e.g., `AdvisoryService`)
- Endpoints are in separate files under `endpoints/`, registered in `endpoints/mod.rs`

**Error handling:**
- All handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Error wrapping uses `.context()` pattern for adding context to errors
- Non-existent resources return 404 via `AppError`

**Naming conventions:**
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`)
- Service method signatures follow `(&self, <entity_id>: Id, tx: &Transactional<'_>)` pattern
- Endpoint handlers extract path params via `Path<Id>`
- Model structs use PascalCase (e.g., `SbomSummary`, `AdvisoryDetails`, `AdvisorySummary`)

**Endpoint registration:**
- Routes registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern
- `server/src/main.rs` mounts all modules — routes auto-mount via module registration
- No need to modify `server/src/main.rs` when adding routes within an existing module

**Response types:**
- Single-entity endpoints return the struct directly (Axum's `Json` extractor handles serialization)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Query helpers (filtering, pagination, sorting) come from `common/src/db/query.rs`

**Framework patterns:**
- HTTP framework: Axum
- ORM: SeaORM for database operations
- Entity definitions in `entity/src/` (e.g., `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`)
- Join tables are separate entity files (e.g., `sbom_advisory.rs` for SBOM-Advisory relationships)

**Import organization:**
- Standard library imports first, external crate imports next, local module imports last
- `use` statements grouped by origin

### Test Conventions

**Assertion style:**
- Endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code checks
- Body deserialization follows status assertion
- `StatusCode::NOT_FOUND` used for 404 assertions

**Response validation:**
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Single-entity tests validate key fields of the returned struct

**Error cases:**
- All endpoint tests include a 404 test with non-existent ID
- Error responses checked via status code assertion

**Test naming:**
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

**Test infrastructure:**
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Tests are in separate files per domain area

**Test documentation:**
- Every test function must have a `///` doc comment explaining what it verifies (per skill requirement, regardless of sibling practice)
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments

### CONVENTIONS.md

- Check for `CONVENTIONS.md` at repository root — if present, follow its conventions and extract CI check commands
- Repository key conventions list: Axum for HTTP, SeaORM for DB, `tower-http` caching middleware
