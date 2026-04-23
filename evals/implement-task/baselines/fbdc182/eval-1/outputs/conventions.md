# Discovered Conventions — trustify-backend

Derived from sibling analysis of `modules/fundamental/src/advisory/` and `modules/fundamental/src/sbom/` patterns, plus the repository's documented Key Conventions.

## Framework and Tooling

- **HTTP framework**: Axum (path extractors, `Json` response, route builders)
- **ORM**: SeaORM (entity relations, join tables, query builder)
- **Language**: Rust (2021 edition implied by project structure)

## Module Structure

- Every domain follows a strict `model/ + service/ + endpoints/` three-layer layout
- Each layer has its own `mod.rs` that pub-re-exports sub-modules
- New sub-modules are declared with `pub mod <name>;` in the parent `mod.rs`
- Files to create always mirror the naming of their sibling: `severity_summary.rs` sits alongside `summary.rs` and `details.rs`

## Naming Conventions

- Struct names: `PascalCase` (e.g., `AdvisorySummary`, `SbomDetails`, `PaginatedResults`)
- Service method names: `verb_noun` snake_case (e.g., `fetch`, `list`, `search`) — new method follows `severity_summary`
- Handler function names: match the file name in snake_case (e.g., handler file `severity_summary.rs` → function `severity_summary`)
- Route path segments: kebab-case (e.g., `/advisory-summary`)

## Error Handling

- All service methods and handlers return `Result<T, AppError>`
- Errors are wrapped with `.context()` from `common/src/error.rs`
- `AppError` implements `IntoResponse` — handlers simply propagate `?`
- 404 responses: return `AppError::not_found()` (or equivalent variant) when entity does not exist

## Endpoint Pattern (from `endpoints/get.rs` sibling)

```rust
// Path parameters extracted via `Path<Id>`
// Service called with `(&self, id: Id, tx: &Transactional<'_>)`
// Response returned directly as `Json(result)` — Axum serializes automatically
// Handler signature: `async fn <name>(State(service): State<Arc<AdvisoryService>>, Path(id): Path<Id>) -> Result<Json<T>, AppError>`
```

## Route Registration (from `endpoints/mod.rs` sibling)

```rust
Router::new().route("/path", get(handler_fn))
// Mounted at the module level; `server/main.rs` composes all module routers
```

## Service Method Pattern (from `advisory.rs` sibling)

```rust
pub async fn method_name(&self, param: Type, tx: &Transactional<'_>) -> Result<ReturnType, AppError>
```

## Response Types

- Single-item endpoints: return the struct directly wrapped in `Json<T>`
- List endpoints: return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- New endpoint (`severity_summary`) returns a plain struct — NOT paginated

## Database / Query Pattern

- Use SeaORM entity definitions from `entity/src/`
- Join table `entity/src/sbom_advisory.rs` links SBOMs to advisories
- `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` has a `severity` field used for per-advisory severity
- Deduplication: use `.distinct()` or group-by on advisory ID before counting

## Testing Conventions (from `tests/api/sbom.rs` and `tests/api/advisory.rs` siblings)

- Integration tests hit a real PostgreSQL test database
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` for HTTP status
- Body deserialization: deserialize into the response struct and assert on specific field values (not just counts)
- Error case coverage: each endpoint test includes at least one 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- Test naming: `test_<endpoint>_<scenario>` snake_case (e.g., `test_advisory_summary_valid_sbom`)
- Documentation: every `#[test]` / `#[tokio::test]` function preceded by a `///` doc comment
- Given-When-Then: non-trivial tests use `// Given`, `// When`, `// Then` inline comments

## Documentation

- `CONVENTIONS.md` exists at repository root (referenced in repo-backend.md) — read it for CI check commands
- Every new public struct, method, and function gets a `///` doc comment (one line minimum)
- API docs in `docs/api.md` should be updated when new public endpoints are added
