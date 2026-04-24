# Discovered Conventions for TC-9201

## Source: Sibling analysis of trustify-backend repository structure

The following conventions were discovered by analyzing sibling files in the repository
(files serving similar roles in sibling modules like `sbom/`, `advisory/`, and `package/`),
cross-referenced with the Key Conventions section in the repository manifest and
CONVENTIONS.md at the repository root.

---

## Production Code Conventions

### Module structure
- Every domain module follows a strict `model/ + service/ + endpoints/` three-directory pattern.
- Each directory has a `mod.rs` that re-exports public items and registers sub-modules.
- Siblings: `sbom/`, `advisory/`, `package/` all follow this exact layout.

### Endpoint conventions
- **Framework**: Axum HTTP framework.
- **Route registration**: Each module's `endpoints/mod.rs` registers routes using
  `Router::new().route("/path", get(handler))`. The `server/main.rs` mounts all modules.
- **Handler pattern** (from `advisory/endpoints/get.rs` and `sbom/endpoints/get.rs`):
  - Extract path parameters via `Path<Id>`.
  - Call the corresponding service method.
  - Return the result directly -- Axum's `Json` extractor handles serialization.
- **Handler return type**: `Result<Json<T>, AppError>`.
- **Endpoint files**: One handler per file (e.g., `list.rs` for listing, `get.rs` for get-by-id).
  New endpoints get their own file in `endpoints/`.

### Service conventions
- **ORM**: SeaORM for database access.
- **Service method signature**: Methods take `&self`, domain-specific ID parameters, and
  `tx: &Transactional<'_'>` for transaction support.
- **Method naming**: `verb_noun` pattern -- existing methods include `fetch`, `list`, `search`, `ingest`.
- **Error handling**: All service methods return `Result<T, AppError>` using `.context()` wrapping
  from `common/src/error.rs`.

### Model conventions
- Each model has its own file (e.g., `summary.rs`, `details.rs`).
- Models are registered in their parent `model/mod.rs` via `pub mod <name>;`.
- Response structs derive `Serialize` (and likely `Deserialize`) for JSON serialization.
- **List responses**: Use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Single-item responses**: Return the struct directly wrapped in `Json<T>`.

### Error handling conventions
- The `AppError` enum in `common/src/error.rs` implements Axum's `IntoResponse`.
- Errors are wrapped with `.context("descriptive message")` before returning.
- 404 responses use a specific `AppError` variant for "not found" cases.

### Import organization
- Common imports from `common/` crate (error types, DB helpers, pagination).
- Entity imports from `entity/` crate (SeaORM models and join tables).
- Module-internal imports for service and model types.

### Database conventions
- **Join tables**: Named as `<entity1>_<entity2>` (e.g., `sbom_advisory`, `sbom_package`).
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`.
- **Connection pooling**: Managed via `common/src/db/limiter.rs`.

### Caching
- Uses `tower-http` caching middleware, with cache configuration in endpoint route builders.

---

## Test Conventions

### Test location and structure
- Integration tests live in `tests/api/` directory.
- Test files are named after the domain module (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database (not mocked).

### Assertion patterns
- Status code assertion: `assert_eq!(resp.status(), StatusCode::OK)`.
- Response body is deserialized into the expected struct type for field-level assertions.
- Error cases: `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 tests.

### Test naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`).

### Test documentation
- Per SKILL.md requirements, every test function must have a `///` doc comment explaining
  what it verifies, even if sibling tests do not currently have them (AI-generated standard).
- Non-trivial tests should include `// Given`, `// When`, `// Then` section comments.

---

## Repository-Level Conventions

### CONVENTIONS.md
- The repository contains a `CONVENTIONS.md` file at root level.
- CI check commands and code generation commands would be extracted from this file
  (in a real implementation, these would be read and executed during Step 9).

### Commit message format
- Conventional Commits specification.
- Format: `<type>[optional scope]: <description>` with Jira issue ID in footer.
- Must include `--trailer="Assisted-by: Claude Code"`.

### Branch naming
- Feature branches named after Jira issue ID (e.g., `TC-9201`).
