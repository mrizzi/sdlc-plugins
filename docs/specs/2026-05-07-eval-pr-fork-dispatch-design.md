# Eval PR Fork Dispatch

**Date**: 2026-05-07
**Scope**: Secure eval execution for fork PRs via `workflow_run` dispatch
**Relates to**: [Eval Skills CI Workflow](2026-04-21-eval-skills-ci-workflow-design.md)

## Problem

The `eval-pr.yml` workflow requires repository secrets (`GCP_SA_KEY`, `CLOUD_ML_REGION`) to authenticate to Google Cloud for running Claude Code via Vertex AI. GitHub does not pass secrets to workflows triggered from forked repositories:

> "With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered from a forked repository."
> — [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

This means fork PRs that modify skills or evals cannot produce eval results.

## Solution

Split `eval-pr.yml` into two workflows using the `workflow_run` event, which runs in the base repository context with full secret access:

> "The workflow started by the `workflow_run` event is able to access secrets and write tokens, even if the previous workflow was not."
> — [Events that trigger workflows: workflow_run](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run)

A trust check auto-approves eval runs for repository collaborators with write access, while external contributors require manual approval via a GitHub protected environment.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Dispatch mechanism | `workflow_run` | Only mechanism that works for fork PRs — `workflow_dispatch`/`repository_dispatch` require write tokens that fork PR `GITHUB_TOKEN` lacks |
| Trust signal | Collaborator permission API | `GET /repos/{owner}/{repo}/collaborators/{username}/permission` — uses GitHub's actual permission model, handles teams automatically, no file parsing |
| Trust threshold | `admin` or `write` | Collaborators with write access can already push to the repo directly — granting them secret access in CI adds no new attack surface |
| Untrusted gate | Protected environment | GitHub's built-in approval mechanism — reviewers click "Approve" in the Actions UI |
| PR coverage | All PRs (fork and non-fork) | Single code path avoids duplicate logic and ensures consistent behavior |
| Artifact naming | `eval-pr-metadata` (fixed name) | Artifacts are scoped to workflow runs — concurrent PRs each get their own run ID, no collision |

## Architecture

```
Fork PR opened
    │
    ▼
┌──────────────────────────────┐
│  eval-pr.yml (pull_request)  │  No secrets needed
│  1. Checkout                 │
│  2. Discover changed skills  │
│  3. Upload artifact          │
│     (skills, PR#, SHA, author)│
└──────────────┬───────────────┘
               │ workflow_run (completed)
               ▼
┌──────────────────────────────────────┐
│  eval-pr-run.yml (workflow_run)      │  Base repo context — secrets available
│                                      │
│  Job 1: discover                     │
│  - Download artifact                 │
│  - Check collaborator permission     │
│  - Output: trusted, skills, PR#, SHA │
│                                      │
│  Job 2: gate                         │
│  - Runs ONLY if trusted != true      │
│  - environment: eval-protected       │
│  - Blocks until reviewer approves    │
│                                      │
│  Job 3: run-evals                    │
│  - Checkout PR merge commit          │
│  - Authenticate GCP                  │
│  - Run evals                         │
│  - Post PR review                    │
└──────────────────────────────────────┘
```

## Workflow 1: eval-pr.yml (modified)

### Changes from Current

The workflow is stripped to discovery and artifact upload only. All secret-dependent steps are removed: GCP authentication, Claude Code installation, eval execution, and review posting.

### Trigger

Unchanged:

```yaml
on:
  pull_request:
    branches: [main]
    paths:
      - 'plugins/sdlc-workflow/skills/**/*.md'
      - 'evals/**/evals.json'
      - '.github/workflows/eval-pr.yml'
```

### Permissions

```yaml
permissions:
  contents: read
```

Reduced from `contents: read` + `pull-requests: write` — this workflow no longer posts reviews.

### Steps

1. **Checkout** — `actions/checkout@v4` with `fetch-depth: 0`
2. **Discover changed skills** — existing logic, unchanged (git diff against PR base, map to eval suites)
3. **Write metadata file** — write `eval-pr-metadata.json` with PR context:

```json
{
  "skills": "skill1,skill2",
  "pr_number": 90,
  "head_sha": "abc123def",
  "author": "username"
}
```

4. **Upload artifact** — `actions/upload-artifact@v4` with name `eval-pr-metadata`, containing the `eval-pr-metadata.json` file.

The artifact is uploaded even when `skills` is empty so Stage 2 can detect the no-op cleanly.

## Workflow 2: eval-pr-run.yml (new)

### Trigger

```yaml
on:
  workflow_run:
    workflows: ["Eval PR"]
    types: [completed]
```

No path filtering — `workflow_run` does not support it. The `completed` type fires on both success and failure, so the `discover` job checks `github.event.workflow_run.conclusion == 'success'` before proceeding. If the triggering workflow found no changed skills, the `run-evals` job skips via its `if` condition.

### Permissions

```yaml
permissions:
  contents: read
  pull-requests: write
  actions: read
```

`actions: read` is needed to download artifacts from the triggering run.

### Job 1: discover

Downloads the artifact and determines trust level. Skips early if the triggering workflow failed.

**Steps:**

1. **Check triggering workflow conclusion** — exit early if `github.event.workflow_run.conclusion != 'success'`

2. **Download artifact** from triggering run:

```yaml
- uses: actions/download-artifact@v4
  with:
    name: eval-pr-metadata
    run-id: ${{ github.event.workflow_run.id }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

3. **Parse metadata and check trust** via `actions/github-script@v7`:

```javascript
const metadata = JSON.parse(fs.readFileSync('eval-pr-metadata.json', 'utf8'));

let trusted = false;
try {
  const { data } = await github.rest.repos.getCollaboratorPermissionLevel({
    owner: context.repo.owner,
    repo: context.repo.repo,
    username: metadata.author
  });
  trusted = ['admin', 'write'].includes(data.permission);
} catch (e) {
  // Non-collaborators may 404 — treat as untrusted
  trusted = false;
}
```

4. **Set outputs**: `skills`, `pr_number`, `head_sha`, `author`, `trusted`

### Job 2: gate

```yaml
gate:
  needs: discover
  if: needs.discover.outputs.trusted != 'true' && needs.discover.outputs.skills != ''
  runs-on: ubuntu-latest
  environment: eval-protected
  steps:
    - run: echo "Approved by reviewer"
```

Skipped entirely for trusted authors and when there are no skills to evaluate. For untrusted authors, the job is created but paused until a designated reviewer approves it in the Actions UI.

### Job 3: run-evals

```yaml
run-evals:
  needs: [discover, gate]
  if: >-
    !cancelled() &&
    needs.discover.outputs.skills != '' &&
    (needs.discover.outputs.trusted == 'true' || needs.gate.result == 'success')
  runs-on: ubuntu-latest
```

**Steps:**

1. **Checkout PR merge commit**:

```yaml
- uses: actions/checkout@v4
  with:
    ref: refs/pull/${{ needs.discover.outputs.pr_number }}/merge
    fetch-depth: 0
```

2. **Authenticate to Google Cloud** — existing step, moved from `eval-pr.yml`:

```yaml
- uses: google-github-actions/auth@v3
  with:
    credentials_json: ${{ secrets.GCP_SA_KEY }}
```

3. **Install Claude Code** — existing step, moved from `eval-pr.yml`

4. **Run PR evals** — existing step, moved from `eval-pr.yml`. Uses `needs.discover.outputs.skills` instead of the inline discovery output.

5. **Post eval results review** — existing step, moved from `eval-pr.yml`. Uses `needs.discover.outputs.pr_number` instead of `context.issue.number` (which is unavailable in `workflow_run` context).

## Trust Model

### Trusted Authors (auto-approve)

Repository collaborators with `write` or `admin` permission. Determined by the GitHub REST API:

```
GET /repos/{owner}/{repo}/collaborators/{username}/permission
```

This returns the highest permission level across all grant sources (direct, teams, org, enterprise). Collaborators with write access can already push directly to the repository, so granting them secret access in CI adds no new attack surface.

### Untrusted Authors (manual approval)

All other PR authors. Their eval runs require a reviewer to click "Approve" in the GitHub Actions UI. The protected environment `eval-protected` enforces this gate.

### Security Properties

- The `workflow_run` workflow executes on the base repository's default branch — a fork PR cannot modify the workflow definition or trust logic
- The collaborator permission check uses GitHub's API, not a file in the repo — it cannot be manipulated by a PR
- Once approved, the workflow does execute skill files from the PR with access to secrets via environment variables — this is inherent to the use case (evaluating skills requires running them)
- The `dontAsk` permission mode with explicit `--allowedTools` limits Claude Code's capabilities, but a malicious skill could still read environment variables via the Bash tool

### Why Not Other Approaches

| Approach | Why not |
|----------|---------|
| `workflow_dispatch` / `repository_dispatch` | Cannot be triggered from fork PR workflows — `GITHUB_TOKEN` is read-only for fork PRs |
| `pull_request_target` | Runs in base repo context with secrets, but GitHub warns: "Avoid using this event if you need to build or run code from the pull request" |
| CODEOWNERS parsing | Text file parsing is fragile (teams, globs, multiple entries); collaborator API is authoritative |
| Skip evals for fork PRs | Fork contributors would never see eval results |

## Setup Requirements

### GitHub Environment

Create a protected environment in the repository:

1. Settings > Environments > New environment: `eval-protected`
2. Add required reviewers (at minimum, repository maintainers)
3. No environment-specific secrets needed — existing repository-level secrets (`GCP_SA_KEY`, `CLOUD_ML_REGION`) are available to all `workflow_run` jobs

### No Other Infrastructure

- No CODEOWNERS file needed
- No GitHub App or PAT required
- No changes to `eval-baseline.yml` (runs on push to main, secrets always available)

## File Changes

| File | Change |
|------|--------|
| `.github/workflows/eval-pr.yml` | Strip to discovery + artifact upload only |
| `.github/workflows/eval-pr-run.yml` | New workflow: trust check, gate, eval execution, review posting |
| `docs/specs/2026-04-21-eval-skills-ci-workflow-design.md` | Add reference to this spec |

## References

- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) — fork PR secret restriction
- [Events that trigger workflows: workflow_run](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run) — secret access in `workflow_run`
- [GitHub Security Lab: Preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/) — two-stage pattern for fork PR processing
- [Repository collaborators API](https://docs.github.com/en/rest/collaborators/collaborators) — permission check endpoint
