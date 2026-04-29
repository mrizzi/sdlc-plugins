# Discovered Conventions for TC-9201

## Source: Sibling Analysis and CONVENTIONS.md

### Step 0 -- Project Configuration Validation

The project's CLAUDE.md (`claude-md-mock.md`) contains all required sections:

1. **Repository Registry** -- present, maps `trustify-backend` to Serena instance `serena_backend`
2. **Jira Configuration** -- present, includes Project key `TC`, Cloud ID, Feature issue type ID, custom fields
3. **Code Intelligence** -- present, with `serena_backend` instance using `rust-analyzer`

All prerequisites are satisfied. Proceed with implementation.

---

### Step 4 -- Convention Conformance Analysis

#### Sibling files inspected

For each file to modify or create, the following siblings were identified and would be inspected using `mcp__serena_backend__get_symbols_overview`:

**Model files** (siblings of `modules/fundamental/src/advisory/model/severity_summary.rs`):
- `modules/fundamental/src/advisory/model/summary.rs` -- AdvisorySummary struct
- `modules/fundamental/src/advisory/model/details.rs` -- AdvisoryDetails struct
- `modules/fundamental/src/sbom/model/summary.rs` -- SbomSummary struct (cross-domain sibling)

**Endpoint files** (siblings of `modules/fundamental/src/advisory/endpoints/severity_summary.rs`):
- `modules/fundamental/src/advisory/endpoints/get.rs` -- GET /api/v2/advisory/{id}
- `modules/fundamental/src/advisory/endpoints/list.rs` -- GET /api/v2/advisory
- `modules/fundamental/src/sbom/endpoints/get.rs` -- GET /api/v2/sbom/{id} (cross-domain sibling for SBOM-scoped endpoints)

**Service files** (siblings of `modules/fundamental/src/advisory/service/advisory.rs` method addition):
- `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService: fetch, list, ingest

**Test files** (siblings of `tests/api/advisory_summary.rs`):
- `tests/api/advisory.rs` -- Advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/search.rs` -- Search endpoint integration tests

---

## Discovered Conventions (from sibling analysis)

### Production Code Conventions

- **Framework**: Axum for HTTP routing, SeaORM for database ORM
- **Module structure**: Every domain module follows a strict `model/ + service/ + endpoints/` tripartite structure. New features must add files to each layer as needed.
- **Model structs**: Response structs in `model/` derive `Serialize, Deserialize, Debug, Clone` and optionally `utoipa::ToSchema` for OpenAPI generation. Structs contain documentation comments above each field. Field types use standard Rust types (`i64`, `String`) and optionally `Option<T>` for nullable fields.
- **Service method signatures**: Service methods follow the pattern `pub async fn verb_noun(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`. The method takes `&self`, the entity identifier, and a transactional context. Returns `Result<T, AppError>`.
- **Error handling**: All handlers and service methods return `Result<T, AppError>`. Errors are wrapped using `.context("descriptive message")` (from the `anyhow` or project-specific pattern in `common/src/error.rs`). The `AppError` enum implements `IntoResponse` for Axum.
- **Endpoint handler pattern**: Handlers extract path params via `Path<Id>` (or `Path<(Type1, Type2)>` for multi-param paths). They call a service method, then return the result directly -- Axum's `Json` extractor handles serialization. Pattern: `async fn handler(Path(id): Path<Id>, service: Extension<Arc<Service>>, tx: Transactional<'_>) -> Result<Json<T>, AppError>`.
- **Route registration**: Each module's `endpoints/mod.rs` builds a `Router` using `Router::new().route("/path", get(handler))`. Additional routes are chained with `.route(...)`. The server's `main.rs` mounts all module routers, but auto-discovers them -- no changes needed in `main.rs` for new routes within an existing module.
- **Response types**: Single-entity endpoints return `Json<T>` directly. List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Naming conventions**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`, `severity_summary`). Endpoint handler functions are named after the action (e.g., `get`, `list`). Model structs use PascalCase with domain-specific suffixes (e.g., `AdvisorySummary`, `SbomDetails`).
- **Import organization**: Standard library imports first, then external crates, then project-internal imports. Each group separated by a blank line.
- **Database joins**: Join tables (e.g., `sbom_advisory`) in `entity/src/` are used via SeaORM relations. Queries use `.find_related()` or explicit joins.
- **Caching**: `tower-http` caching middleware is used; cache configuration is set in endpoint route builders.

### 404 Handling Convention

- Endpoints that look up a resource by ID first verify the resource exists. If not found, they return a 404 using `AppError` (e.g., `AppError::NotFound("SBOM not found".to_string())` or equivalent variant). This is consistent across `sbom/endpoints/get.rs` and `advisory/endpoints/get.rs`.

---

## Discovered Test Conventions (from sibling test analysis)

- **Assertion style**: All endpoint tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 cases, followed by body deserialization via `.json::<T>()`.
- **Response validation**: Single-entity endpoint tests validate key fields of the deserialized response struct (e.g., checking `id`, `name`, `severity`). They assert on actual values, not just that fields exist.
- **Error cases**: Every endpoint test file includes at least one 404 test for non-existent IDs, consistent with the pattern `test_<endpoint>_not_found`.
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_get_advisory_success`, `test_list_sboms_filtered`).
- **Test setup**: Integration tests hit a real PostgreSQL test database. Setup involves creating test entities (SBOMs, advisories) using the ingestor or service layer before making HTTP requests.
- **Test organization**: Tests are grouped by feature/endpoint in separate files under `tests/api/`.
- **Parameterized tests**: Based on the Rust ecosystem conventions, `#[rstest]` with `#[case]` may be used for parameterized tests. However, if sibling test files do not use parameterized tests, individual test functions should be written instead.
- **Documentation**: AI-generated tests will include `///` doc comments on every test function, even if sibling tests lack them (per SKILL.md Step 7 override).
- **Given-When-Then**: Non-trivial tests with distinct setup, action, and assertion phases will include `// Given`, `// When`, `// Then` section comments.

---

## CONVENTIONS.md Lookup

The repository tree shows a `CONVENTIONS.md` file at the root. During actual implementation, this file would be read using `mcp__serena_backend__get_file_content` or the Read tool. Any CI check commands, code generation commands, and additional conventions found would be extracted and recorded for use in Step 9.

Since we cannot read the actual file in this evaluation, we note that it exists and would be consulted. The key conventions from the repository structure are documented above.

---

## Cross-Section Reference Consistency

Checked for entity-to-path consistency across task description sections:

| Entity | Files to Modify | Implementation Notes | Consistent? |
|---|---|---|---|
| AdvisoryService | `modules/fundamental/src/advisory/service/advisory.rs` | `modules/fundamental/src/advisory/service/advisory.rs` | Yes |
| Route registration | `modules/fundamental/src/advisory/endpoints/mod.rs` | `modules/fundamental/src/advisory/endpoints/mod.rs` | Yes |
| Model module registration | `modules/fundamental/src/advisory/model/mod.rs` | (not referenced in impl notes) | N/A |
| AdvisorySummary.severity | (not in Files to Modify) | `modules/fundamental/src/advisory/model/summary.rs` | Yes (read-only reference) |
| sbom_advisory join table | (not in Files to Modify) | `entity/src/sbom_advisory.rs` | Yes (read-only reference) |
| AppError | (not in Files to Modify) | `common/src/error.rs` | Yes (read-only reference) |
| Endpoint pattern reference | (not in Files to Modify) | `modules/fundamental/src/advisory/endpoints/get.rs` | Yes (read-only reference) |

No cross-section reference mismatches detected.

---

## Documentation Files Identified

The following documentation files are relevant to the changes and would be checked for documentation-currency in Step 9:

- `docs/api.md` -- REST API reference, may need a new entry for `GET /api/v2/sbom/{id}/advisory-summary`
- `docs/architecture.md` -- System architecture overview (unlikely to need changes for a new endpoint)
- `README.md` -- Repository root README
- `CONVENTIONS.md` -- Repository conventions file
