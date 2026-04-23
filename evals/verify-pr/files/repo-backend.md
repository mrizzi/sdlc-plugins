<!-- SYNTHETIC TEST DATA — representative repository structure for eval testing; names, URLs, and identifiers are fictional -->

# Repository Structure: trustify-backend

A Rust backend service for the Trusted Profile Analyzer platform. Manages SBOMs,
vulnerability advisories, and risk assessments via a REST API backed by PostgreSQL.

## Directory Tree

```
trustify-backend/
├── Cargo.toml
├── Cargo.lock
├── README.md
├── CONVENTIONS.md
├── migration/
│   ├── src/
│   │   ├── lib.rs
│   │   └── m0001_initial/
│   │       └── mod.rs
│   └── Cargo.toml
├── common/
│   ├── src/
│   │   ├── lib.rs
│   │   ├── db/
│   │   │   ├── mod.rs
│   │   │   ├── query.rs          # Shared query builder helpers (filtering, pagination, sorting)
│   │   │   └── limiter.rs        # Connection pool limiter
│   │   ├── model/
│   │   │   ├── mod.rs
│   │   │   └── paginated.rs      # PaginatedResults<T> response wrapper
│   │   └── error.rs              # AppError enum, implements IntoResponse
│   └── Cargo.toml
├── modules/
│   ├── fundamental/
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── sbom/
│   │   │   │   ├── mod.rs
│   │   │   │   ├── model/
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── summary.rs       # SbomSummary struct
│   │   │   │   │   └── details.rs       # SbomDetails struct
│   │   │   │   ├── service/
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   └── sbom.rs          # SbomService: fetch, list, ingest
│   │   │   │   └── endpoints/
│   │   │   │       ├── mod.rs           # Route registration: /api/v2/sbom
│   │   │   │       ├── list.rs          # GET /api/v2/sbom — list SBOMs
│   │   │   │       └── get.rs           # GET /api/v2/sbom/{id} — get SBOM details
│   │   │   ├── advisory/
│   │   │   │   ├── mod.rs
│   │   │   │   ├── model/
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   ├── summary.rs       # AdvisorySummary struct (includes severity field)
│   │   │   │   │   └── details.rs       # AdvisoryDetails struct
│   │   │   │   ├── service/
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   └── advisory.rs      # AdvisoryService: fetch, list, search
│   │   │   │   └── endpoints/
│   │   │   │       ├── mod.rs           # Route registration: /api/v2/advisory
│   │   │   │       ├── list.rs          # GET /api/v2/advisory
│   │   │   │       └── get.rs           # GET /api/v2/advisory/{id}
│   │   │   └── package/
│   │   │       ├── mod.rs
│   │   │       ├── model/
│   │   │       │   ├── mod.rs
│   │   │       │   └── summary.rs       # PackageSummary struct (includes license field)
│   │   │       ├── service/
│   │   │       │   └── mod.rs           # PackageService: fetch, list
│   │   │       └── endpoints/
│   │   │           ├── mod.rs           # Route registration: /api/v2/package
│   │   │           └── list.rs          # GET /api/v2/package
│   │   └── Cargo.toml
│   ├── ingestor/
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── graph/
│   │   │   │   ├── mod.rs
│   │   │   │   ├── sbom/
│   │   │   │   │   └── mod.rs           # SBOM ingestion: parse, store, link packages
│   │   │   │   └── advisory/
│   │   │   │       └── mod.rs           # Advisory ingestion: parse, store, correlate
│   │   │   └── service/
│   │   │       └── mod.rs               # IngestorService
│   │   └── Cargo.toml
│   └── search/
│       ├── src/
│       │   ├── lib.rs
│       │   ├── service/
│       │   │   └── mod.rs               # SearchService: full-text search across entities
│       │   └── endpoints/
│       │       └── mod.rs               # GET /api/v2/search
│       └── Cargo.toml
├── entity/
│   ├── src/
│   │   ├── lib.rs
│   │   ├── sbom.rs                      # SBOM entity (SeaORM)
│   │   ├── advisory.rs                  # Advisory entity
│   │   ├── sbom_advisory.rs             # SBOM-Advisory join table
│   │   ├── package.rs                   # Package entity
│   │   ├── sbom_package.rs              # SBOM-Package join table
│   │   └── package_license.rs           # Package-License mapping
│   └── Cargo.toml
├── server/
│   ├── src/
│   │   └── main.rs                      # Axum server setup, route mounting
│   └── Cargo.toml
└── tests/
    ├── api/
    │   ├── sbom.rs                      # SBOM endpoint integration tests
    │   ├── advisory.rs                  # Advisory endpoint integration tests
    │   └── search.rs                    # Search endpoint integration tests
    └── Cargo.toml
```

## Key Conventions

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders
