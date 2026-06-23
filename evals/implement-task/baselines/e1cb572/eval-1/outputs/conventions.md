# Discovered Conventions

## From CONVENTIONS.md Lookup

The repository root contains a `CONVENTIONS.md` file at `./CONVENTIONS.md`. This would be read during Step 4 for explicit project-level conventions and CI verification commands. Since we cannot access the actual file in this eval, we note its existence and would follow whatever conventions it specifies.

## Discovered Conventions (from sibling analysis)

Based on analysis of the repository structure described in `repo-backend.md` and the patterns referenced in the task's Implementation Notes:

### Production Code Conventions

- **Framework:** Axum for HTTP routing, SeaORM for database ORM
- **Module structure:** Each domain module follows the `model/ + service/ + endpoints/` triad pattern (observed in `sbom/`, `advisory/`, `package/`)
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping for error enrichment (pattern from `common/src/error.rs`)
- **Endpoint registration:** Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern; `server/main.rs` mounts all modules
- **Response types:** Single-entity endpoints return the struct directly via Axum's `Json` extractor; list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Service method signatures:** Service methods take `&self`, entity-specific parameters, and `tx: &Transactional<'_>` (observed in `AdvisoryService::fetch`, `AdvisoryService::list`)
- **Path parameter extraction:** Endpoints use `Path<Id>` extractor from Axum (observed in `get.rs` endpoint handlers)
- **Query helpers:** Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Caching:** Uses `tower-http` caching middleware configured in endpoint route builders
- **Model module registration:** Each `model/mod.rs` re-exports sub-modules with `pub mod <name>;` declarations (observed in `advisory/model/mod.rs` with `summary` and `details` sub-modules)
- **Naming:** Model structs follow `<Entity>Summary` and `<Entity>Details` naming (e.g., `AdvisorySummary`, `SbomDetails`)
- **File naming:** Model files are named after the struct purpose in lowercase (e.g., `summary.rs`, `details.rs`)

### Test Conventions

- **Test location:** Integration tests live in `tests/api/` directory, one file per domain entity
- **Test naming:** Files follow the entity name pattern (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- **Test database:** Tests hit a real PostgreSQL test database (not mocked)
- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code verification, followed by body deserialization
- **Error case coverage:** Based on acceptance criteria patterns, 404 tests should use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` consistent with existing SBOM endpoints

### Import Organization

- Standard library imports first, then external crates, then internal modules (standard Rust convention)

### No Convention Conflicts Detected

The task description and Implementation Notes are consistent with all discovered conventions. No conflicts to flag.
