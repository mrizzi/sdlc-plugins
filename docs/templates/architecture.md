# Architecture Documentation Template

<!-- TODO: Copy this template into your project and fill in the sections below.
     This document helps the AI assistant understand your project's architecture
     so it can make better planning and implementation decisions. -->

## System Overview

<!-- TODO: Provide a high-level description of your system.
     What does it do? Who are the users? What are the main components? -->

## Repositories

<!-- TODO: List each repository in your project with its purpose.
     Example:
     - **my-backend** — Go API server, handles business logic and data persistence
     - **my-frontend** — React SPA, user-facing dashboard
     - **my-infra** — Terraform modules and Helm charts for deployment -->

## Key Modules

<!-- TODO: For each repository, list the major modules/packages and their responsibilities.
     Example:
     ### my-backend
     - `cmd/server` — application entrypoint and CLI
     - `internal/api` — HTTP handlers and routing
     - `internal/domain` — core business logic
     - `internal/storage` — database access layer -->

## API Surface

<!-- TODO: Document the main APIs (REST, gRPC, GraphQL, etc.).
     Example:
     - `GET /api/v1/items` — list items with pagination
     - `POST /api/v1/items` — create a new item
     - `GET /api/v1/items/{id}` — get item details -->

## Data Model

<!-- TODO: Describe the main entities and their relationships.
     Example:
     - **Item** — core entity, has many Tags, belongs to a Project
     - **Project** — grouping entity, has many Items and Members -->

## External Dependencies

<!-- TODO: List external services, databases, and message queues your system depends on.
     Example:
     - PostgreSQL 15 — primary data store
     - Redis — caching and session storage
     - S3-compatible storage — file uploads -->

## Testing Strategy

<!-- TODO: Describe how tests are organized and run.
     Example:
     - Unit tests: `cargo test` / `npm test`
     - Integration tests: `cargo test --features integration`
     - E2E tests: Cypress in `my-frontend/cypress/` -->
