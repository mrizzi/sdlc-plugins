# Description Digests — TC-9004

Each digest below corresponds to a task description file. The digest is computed
using SHA-256 over the file content (markdown format, stripped of leading/trailing
whitespace), tagged with the format prefix `sha256-md:`.

## Digests

| Task | File | Digest |
|---|---|---|
| Task 1 — License report model | `task-1-license-report-model.md` | `sha256-md:2c7bdc2cbad94b2707ccf5e7d57c1e42283796230b88dd47dee9de3b8d37355b` |
| Task 2 — License report service | `task-2-license-report-service.md` | `sha256-md:0833c48889a402fd278adfebb3bddb4073a27782a540b6036102c4b45cec71a3` |
| Task 3 — License report endpoint | `task-3-license-report-endpoint.md` | `sha256-md:127c48bc058e3cca330726656410c0642eee7c025a1cae550c06b55e601a4a54` |
| Task 4 — Integration tests | `task-4-integration-tests.md` | `sha256-md:bb1a7cb684536d406d8e7532d0d7fd6bf5b670220210b907f507cbaa252ebc99` |

## Digest Comment Format

For each task, a Jira comment would be posted with the following format:

```
[sdlc-workflow] Description digest: <tagged-digest>
```

Where `<tagged-digest>` is the value from the Digest column above.
