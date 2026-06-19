# Running sdlc-workflow skills with fullsend

Run sdlc-workflow skills inside secure sandboxes via [fullsend](https://github.com/fullsend-ai/fullsend). Each skill runs in an isolated container with least-privilege network and filesystem policies.

## Prerequisites

- [fullsend](https://github.com/fullsend-ai/fullsend) CLI installed
- [OpenShell](https://github.com/NVIDIA/OpenShell) gateway running — fullsend uses OpenShell as its sandbox runtime; the gateway manages container lifecycle
- GCP credentials for Vertex AI (or Anthropic API key) — Claude Code needs LLM API access from inside the sandbox
- Jira API token — skills read/write Jira issues via REST API (MCP is not available inside the sandbox)
- GitHub token — skills read PRs and post comments via `gh` CLI
- Python `jsonschema` package on the runner — the `validation_loop` validates agent output against the JSON schema before the post_script runs (`pip install jsonschema`)

## Quick start (local mode)

```bash
fullsend run verify-pr \
  --fullsend-dir plugins/sdlc-workflow \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env
```

This assumes sdlc-plugins is cloned locally. For target repos without the
clone, see [Deployment modes](#deployment-modes) below.

The `--fullsend-dir` points to the plugin directory itself — it doubles as the
fullsend config directory, so the same skill files serve both Claude Code plugin
users and fullsend users with zero duplication.

The `--target-repo` must be a disposable clone, not your working directory —
fullsend deletes and re-creates this directory after each run
([fullsend#2075](https://github.com/fullsend-ai/fullsend/issues/2075)).

The post_script handles all Jira/GitHub write operations (sub-task creation,
PR comment replies, verification report posting) after the sandbox agent
completes and output validation passes.

## Secrets env file

Create a secrets file (never commit this). The `--env-file` flag is repeatable —
use a separate file for per-run variables like `JIRA_ISSUE_ID`:

```bash
# secrets.env — long-lived credentials
# GCP (tier 4 — file-based auth, must be on sandbox filesystem)
ANTHROPIC_VERTEX_PROJECT_ID=my-project
GOOGLE_CLOUD_PROJECT=my-project
CLOUD_ML_REGION=global
GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa-key.json
# Issue tracker (tier 2 — provider proxies credentials via gateway)
JIRA_SERVER_URL=https://myorg.atlassian.net
JIRA_EMAIL=me@example.com
JIRA_API_TOKEN=my-jira-token
JIRA_PROJECT_KEY=TC
# GitHub (tier 2 — provider proxies credentials via gateway)
GH_TOKEN=my-github-token
```

Jira and GitHub credentials are read by the providers and post_script on the
trusted runner — they never enter the sandbox. GCP credentials must be on the
sandbox filesystem (tier 4) because Vertex AI auth requires local JWT signing.

```bash
# task.env — per-run variables
JIRA_ISSUE_ID=PROJ-123
```

```bash
fullsend run verify-pr \
  --fullsend-dir plugins/sdlc-workflow \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env \
  --env-file task.env
```

Later env files override earlier ones, so `task.env` can override any value
from `secrets.env`.

## Building the image

Fullsend runs agents inside sandboxed containers. Claude Code discovers plugins
through a marketplace cache structure under `$CLAUDE_CONFIG_DIR/plugins/`. The
Dockerfile extends fullsend's base image and bakes the sdlc-workflow plugin into
this cache so Claude Code auto-discovers the skills — no `--plugin-dir` flag needed
at runtime.

**CI pipeline:** The image is automatically built and pushed to GHCR on every
push to `run-in-fullsend` that changes plugin files. The pipeline builds
multi-arch (`linux/amd64` + `linux/arm64`) images using Red Hat actions
(`buildah-build`, `podman-login`, `push-to-registry`). PR builds validate
without pushing.

See `.github/workflows/build-sandbox-image.yml`.

**Local build** (for development/testing):

```bash
podman build -f plugins/sdlc-workflow/sandboxes/base/Dockerfile \
  -t ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest .
```

## File inventory

All paths are relative to `plugins/sdlc-workflow/`.

| File | Purpose | Why |
|---|---|---|
| `sandboxes/base/Dockerfile` | Container image extending `fullsend-code` with the sdlc-workflow plugin baked into Claude Code's marketplace cache | Extends fullsend's own image to inherit TLS proxy CA workaround, security tooling (gitleaks, tirith), and all system dependencies. We only add the plugin. |
| `sandboxes/base/Dockerfile.hummingbird` | Alternative image based on Red Hat Hummingbird (near-zero CVE) | For environments that require RPM-based images. Self-contained — installs all tools via `dnf` from official repos (Anthropic, GitHub, Hummingbird). |
| `sandboxes/base/bootstrap-plugin-cache.sh` | Generates Claude Code marketplace cache structure at build time | Claude Code auto-discovers plugins from `$CLAUDE_CONFIG_DIR/plugins/` only if the marketplace cache JSON files exist. This script replicates the structure that fullsend's `bootstrapPlugins()` Go function creates at runtime, but baked into the image so no host-side plugin upload is needed. |
| `sandboxes/base/claude-code.repo` | Anthropic's official RPM repo definition for Claude Code | Only used by `Dockerfile.hummingbird`. The default Dockerfile inherits Claude Code from the fullsend base image. |
| `providers/jira.yaml` | OpenShell provider for Jira credentials | The gateway proxy swaps opaque placeholder tokens for real `JIRA_EMAIL` and `JIRA_API_TOKEN` at the HTTP layer. Credentials never enter the sandbox ([ADR-0025](https://github.com/fullsend-ai/fullsend/blob/main/docs/ADRs/0025-provider-credential-delivery-for-sandboxed-agents.md), tier 2). |
| `providers/github.yaml` | OpenShell provider for GitHub token | Uses the built-in `github` provider type. The gateway injects `GH_TOKEN` as an opaque placeholder, swapped transparently when `gh` CLI makes API calls. |
| `harness/verify-pr.yaml` | Fullsend harness config for the verify-pr skill | Declares the image, policy, providers, env file mounts, and timeout. Fullsend reads this to know how to create the sandbox, what credentials to inject, and how long the agent can run. |
| `agents/verify-pr.md` | Agent prompt with YAML frontmatter | Fullsend launches Claude Code with `--agent verify-pr` which loads this file as the system prompt. The YAML frontmatter is required — without it Claude Code treats the file as a generic prompt and ignores the instructions. The agent reads `JIRA_ISSUE_ID` from the environment and invokes the skill. |
| `policies/verify-pr.yaml` | Sandbox network/filesystem policy | Controls which endpoints the sandbox can reach and whether the filesystem is read-only or read-write. Each network policy entry requires a `name:` field (OpenShell supervisor crashes without it), prefix wildcards only (`*.googleapis.com`, not `*-pattern.domain`), and `**/binary` double-star globs for binary paths. These constraints were discovered by testing against OpenShell and verified against fullsend's production policies. |
| `env/gcp-vertex.env` | Vertex AI env var template | Expanded at runtime from the secrets file via fullsend's `host_files` with `expand: true`. Sets `CLAUDE_CODE_USE_VERTEX=1` and points `GOOGLE_APPLICATION_CREDENTIALS` to the uploaded credential file at `/tmp/.gcp-credentials.json`. |
| `env/jira.env` | Jira non-credential config | Carries `JIRA_SERVER_URL` (for URL construction) and `JIRA_ISSUE_ID` (task identifier). Credentials (`JIRA_EMAIL`, `JIRA_API_TOKEN`) are injected by the Jira provider, not this file. |
| `schemas/verify-pr-result.schema.json` | JSON Schema for verify-pr structured output | Defines the action types, cross-reference format, and report structure. Validated by fullsend's `validation_loop` before the post_script runs. |
| `scripts/pre-verify-pr.sh` | Pre_script for verify-pr | Validates inputs before sandbox creation: checks required env vars, JIRA_ISSUE_ID format, issue existence, and PR linkage. Fails fast to avoid wasting sandbox compute time. Delegates Python logic to `pre_verify_pr.py`. |
| `scripts/pre_verify_pr.py` | Pre-script Python module | Extracts PR URL from Jira custom fields (ADF or string) and transforms Jira issue JSON into the tracker-agnostic input schema. Called by `pre-verify-pr.sh` via stdin pipe. |
| `scripts/post-verify-pr.sh` | Post_script for verify-pr | Shell wrapper that finds `agent-result.json` and delegates to `execute-actions.py`. Runs on the trusted runner after sandbox is destroyed. |
| `scripts/execute-actions.py` | Action executor | Processes the ordered actions array, resolves `{{ref.key}}` placeholders as Jira entities are created, calls `jira-client.py` and `gh` CLI for all write operations. |
| `scripts/validate-output-schema.sh` | Output schema validator | Strips extra properties then validates JSON against the schema using Python's `jsonschema`. The stripping is schema-driven (not hardcoded) via `strip_extra_properties.py`. Used by `validation_loop`. |
| `scripts/strip_extra_properties.py` | Schema-driven property stripper | Recursively walks the JSON Schema tree and removes properties not declared at nodes with `additionalProperties: false`. Handles `$ref`, `allOf/if/then` discriminated unions, and nested objects/arrays. The agent can add arbitrary metadata fields without breaking validation or burning retry iterations. |

## Adding a new skill

Each skill needs up to 7 files. Some are shared across skills (providers,
executor, image), others are skill-specific. The checklist below covers
everything needed for a tier-2 skill with structured output.

### Shared files (reuse as-is)

These already exist and apply to all skills — do not create copies:

| File | Shared because |
|---|---|
| `providers/jira.yaml` | Same Jira credentials for all skills |
| `providers/github.yaml` | Same GitHub token for all skills |
| `scripts/execute-actions.py` | Generic action executor — extend if new action types needed |
| `scripts/validate-output-schema.sh` | Schema validator with property stripping via `strip_extra_properties.py` |
| `scripts/strip_extra_properties.py` | Generic recursive property stripper — works with any schema |
| `scripts/jira-client.py` | Jira REST API client used by pre/post scripts |
| `scripts/pre_verify_pr.py` | Pre-script Python module for Jira data extraction |
| `env/gcp-vertex.env` | Vertex AI config — same for all skills |
| `env/jira.env` | Non-credential Jira config (`JIRA_SERVER_URL`, `JIRA_ISSUE_ID`) |
| Image (`sdlc-base:latest`) | All skills share the same image |

### Skill-specific files (create for each new skill)

#### 1. Agent prompt — `agents/<skill>.md`

YAML frontmatter is required. The agent receives "Run the agent task" from
fullsend and must read env vars to determine what to do. After the skill
completes, it verifies the structured output file exists.

```markdown
---
name: <skill>
description: >-
  One-line description of what this agent does.
model: opus
---

# <Skill> Agent

You are running inside an OpenShell sandbox with the sdlc-workflow plugin
pre-installed.

## Startup procedure

1. Read the `JIRA_ISSUE_ID` environment variable:
   ```bash
   echo $JIRA_ISSUE_ID
   ```

2. Invoke the skill:
   ```
   /sdlc-workflow:<skill> <issue-id>
   ```

3. After the skill completes, verify the output file exists:
   ```bash
   ls -la $FULLSEND_OUTPUT_DIR/agent-result.json
   ```

## Constraints

- Do not call issue tracker write APIs directly — the skill writes
  structured JSON output for the post_script to process.
- Do not post GitHub comments directly — the post_script handles this.
- <list additional constraints specific to this skill>
```

#### 2. Harness — `harness/<skill>.yaml`

Declares the full execution pipeline: providers for credential isolation,
pre_script for input validation, validation_loop for output checking, and
post_script for executing write operations on the trusted runner.

```yaml
agent: agents/<skill>.md
model: opus
image: ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest
policy: policies/<skill>.yaml

providers:
  - jira
  - github

security:
  enabled: true

host_files:
  - src: env/gcp-vertex.env
    dest: /sandbox/workspace/.env.d/gcp-vertex.env
    expand: true
  - src: env/jira.env
    dest: /sandbox/workspace/.env.d/jira.env
    expand: true
  - src: ${GOOGLE_APPLICATION_CREDENTIALS}
    dest: /tmp/.gcp-credentials.json
  - src: ${GCP_OIDC_TOKEN_FILE}
    dest: /sandbox/workspace/.gcp-oidc-token
    optional: true
  - src: /tmp/fullsend-pre-output/<skill>-input.json
    dest: /sandbox/workspace/.pre-script/<skill>-input.json
    optional: true

validation_loop:
  script: scripts/validate-output-schema.sh
  max_iterations: 2

pre_script: scripts/pre-<skill>.sh
post_script: scripts/post-<skill>.sh

runner_env:
  JIRA_SERVER_URL: "${JIRA_SERVER_URL}"
  JIRA_EMAIL: "${JIRA_EMAIL}"
  JIRA_API_TOKEN: "${JIRA_API_TOKEN}"
  JIRA_PROJECT_KEY: "${JIRA_PROJECT_KEY}"
  GH_TOKEN: "${GH_TOKEN}"
  FULLSEND_OUTPUT_SCHEMA: "${FULLSEND_DIR}/schemas/<skill>-result.schema.json"
  FULLSEND_OUTPUT_FILE: "agent-result.json"

timeout_minutes: 30
```

Key points:
- `providers:` references shared provider names — credentials never enter
  the sandbox (tier 2, [ADR-0025](https://github.com/fullsend-ai/fullsend/blob/main/docs/ADRs/0025-provider-credential-delivery-for-sandboxed-agents.md))
- `host_files` mounts pre-fetched task data from the pre_script (optional
  — the skill falls back to API calls if the file is missing)
- `runner_env` credentials are for the post_script on the trusted runner,
  not injected into the sandbox
- `FULLSEND_OUTPUT_SCHEMA` uses `${FULLSEND_DIR}` to resolve relative to
  `--fullsend-dir`

#### 3. Policy — `policies/<skill>.yaml`

Start from the verify-pr policy and adjust. The policy controls per-skill
network and filesystem access — the image is shared across all skills.

**Filesystem:**
- **Read-only skills** (plan-feature, verify-pr, define-feature): set
  `include_workdir: false`. The sandbox enforces this via Landlock LSM.
- **Read-write skills** (implement-task): set `include_workdir: true`.

**Network — adjust these entries per skill:**
- `claude_code` — always required (LLM API access)
- `jira_read` — for skills that read issues at runtime (e.g., root-cause
  investigation). Remove if the skill only uses pre-fetched data.
- `github_read` — for skills that read PR data via `gh` CLI
- `github_git` — add for skills that push commits (port 22, SSH)
- `figma` — add for skills that read Figma designs (`api.figma.com`)
- `npm_registry`, `crates_io`, `pypi` — add for skills that install
  packages during builds

**Format constraints (OpenShell-specific):**
- Every entry requires a `name:` field (supervisor crashes without it)
- Prefix wildcards only (`*.googleapis.com`, not `*-pattern.domain`)
- Binary paths use `**/binary` double-star globs
- `landlock: compatibility: best_effort` is required

```yaml
version: 1

filesystem_policy:
  include_workdir: false
  read_only:
    - /var/log
    - /usr
    - /lib
    - /lib64
    - /proc
    - /dev/urandom
    - /etc
    - /opt
  read_write:
    - /sandbox
    - /tmp
    - /dev/null

landlock:
  compatibility: best_effort

process:
  run_as_user: sandbox
  run_as_group: sandbox

network_policies:
  claude_code:
    name: claude-code
    endpoints:
      - { host: api.anthropic.com, port: 443 }
      - { host: "*.googleapis.com", port: 443 }
      - { host: "*.amazonaws.com", port: 443 }
      - { host: statsig.anthropic.com, port: 443 }
      - { host: sentry.io, port: 443 }
      - { host: raw.githubusercontent.com, port: 443 }
      - { host: platform.claude.com, port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/node" }
  jira_read:
    name: jira-read
    endpoints:
      - { host: "*.atlassian.net", port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/python3" }
  github_read:
    name: github-read
    endpoints:
      - { host: api.github.com, port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/gh" }
```

#### 4. Output schema — `schemas/<skill>-result.schema.json`

Defines the structured JSON output the agent produces. The `validation_loop`
validates against this schema before the post_script runs. Use the same
action types as verify-pr (`create_subtask`, `create_link`, `post_pr_reply`,
`post_pr_comment`, `create_root_cause_task`, `post_comment`, `post_report`). If the skill needs
new action types, add them to the schema and extend `execute-actions.py`.

See `schemas/verify-pr-result.schema.json` as the reference.

#### 5. Input schema — `schemas/<skill>-input.schema.json`

Defines the tracker-agnostic pre-fetched data the pre_script writes into the
sandbox. The schema normalizes tracker-specific data (Jira, GitHub Issues,
etc.) into a common format:

- `task_id` — issue key (e.g., `TC-4741`, `#42`)
- `task.summary`, `task.description`, `task.status`, `task.labels`,
  `task.issue_links`, `task.custom_fields` — normalized fields
- `pr_url` — PR URL from the task's custom field
- `source.tracker` — tracker type (`jira`, `github`)
- `source.raw` — full original API response

See `schemas/verify-pr-input.schema.json` as the reference. Most skills
can reuse the same input schema since the task data structure is shared.

#### 6. Pre_script — `scripts/pre-<skill>.sh`

Runs on the trusted runner before sandbox creation. Responsibilities:

1. **Validate inputs** — check required env vars, issue ID format
2. **Verify issue exists** — fail fast before burning sandbox compute
3. **Pre-fetch task data** — fetch the full issue and write a
   tracker-agnostic JSON file to `/tmp/fullsend-pre-output/<skill>-input.json`
4. **Extract PR/branch URL** — from the task's custom fields

The pre_script uses `runner_env` credentials (expanded from `--env-file`).
These credentials are for the pre_script and post_script only — they never
enter the sandbox.

See `scripts/pre-verify-pr.sh` as the reference. Most skills can share the
same pre_script logic since the input validation and pre-fetching are
identical — only the output filename differs.

#### 7. Post_script — `scripts/post-<skill>.sh`

Runs on the trusted runner after sandbox cleanup. Reads the agent's
`agent-result.json`, delegates to `execute-actions.py` for action processing.

See `scripts/post-verify-pr.sh` as the reference. Most skills can share the
same post_script since the action executor is generic — it processes any
action types defined in the output schema.

### Testing a new skill

1. **Build the image** (only if skill files changed):
   ```bash
   podman build -f plugins/sdlc-workflow/sandboxes/base/Dockerfile \
     -t ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest .
   ```

2. **Clean up stale providers** (if a previous run left them):
   ```bash
   openshell provider delete jira github 2>/dev/null || true
   ```

3. **Create a disposable clone** of the target repo:
   ```bash
   rm -rf /tmp/my-repo-clone && git clone <repo-url> /tmp/my-repo-clone
   ```

4. **Run fullsend**:
   ```bash
   fullsend run <skill> \
     --fullsend-dir plugins/sdlc-workflow \
     --target-repo /tmp/my-repo-clone \
     --env-file secrets.env \
     --env-file <(echo "JIRA_ISSUE_ID=<issue-id>")
   ```

5. **Verify the pipeline**:
   - Pre_script: "Input validation passed"
   - Providers: "Provider ready: jira" and "Provider ready: github"
   - Agent: exits with code 0
   - Validation: "PASS: output validated against schema"
   - Post_script: actions executed successfully

## Deployment modes

There are three ways to run sdlc-workflow skills via fullsend.

### Local mode — for sdlc-plugins developers

When sdlc-plugins is cloned locally, point `--fullsend-dir` at the plugin
directory. All files (harness, agents, policies, env) are resolved locally.
Updates arrive via `git pull`.

```bash
fullsend run verify-pr \
  --fullsend-dir plugins/sdlc-workflow \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env
```

The post_script handles all Jira/GitHub write operations (sub-task creation,
PR comment replies, verification report posting) after the sandbox agent
completes and output validation passes.

### Remote mode — for target repos without sdlc-plugins

Target repos that consume sdlc-workflow skills without cloning sdlc-plugins
use URL-referenced resources in their own `.fullsend/` directory. The agent
prompt and policy are fetched from GitHub at runtime; the plugin is baked
into the custom image.

```
my-repo/
├── .fullsend/
│   ├── harness/
│   │   └── verify-pr.yaml      # URL refs to agent/policy + image tag
│   └── env/
│       ├── gcp-vertex.env       # ${VAR} templates (identical across repos)
│       ├── jira.env
│       └── github.env
├── AGENTS.md → CLAUDE.md        # symlink (recommended)
└── ...
```

The harness references the agent and policy via URLs with mandatory SHA-256
integrity hashes ([ADR-0038](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0038-universal-harness-access.md)).
The plugin comes from the custom image — `plugins:` does not support URL
references today ([fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113)).

```yaml
# .fullsend/harness/verify-pr.yaml
agent: https://raw.githubusercontent.com/mrizzi/sdlc-plugins/<commit>/plugins/sdlc-workflow/agents/verify-pr.md#sha256=<hash>
model: opus
image: ghcr.io/mrizzi/sdlc-plugins/sdlc-base:<version>
policy: https://raw.githubusercontent.com/mrizzi/sdlc-plugins/<commit>/plugins/sdlc-workflow/policies/verify-pr.yaml#sha256=<hash>

security:
  enabled: true

host_files:
  - src: env/gcp-vertex.env
    dest: /sandbox/workspace/.env.d/gcp-vertex.env
    expand: true
  - src: env/jira.env
    dest: /sandbox/workspace/.env.d/jira.env
    expand: true
  - src: env/github.env
    dest: /sandbox/workspace/.env.d/github.env
    expand: true
  - src: ${GOOGLE_APPLICATION_CREDENTIALS}
    dest: /tmp/.gcp-credentials.json
  - src: ${GCP_OIDC_TOKEN_FILE}
    dest: /sandbox/workspace/.gcp-oidc-token
    optional: true

allowed_remote_resources:
  - https://raw.githubusercontent.com/mrizzi/sdlc-plugins/

timeout_minutes: 30
```

```bash
fullsend run verify-pr \
  --fullsend-dir .fullsend \
  --target-repo . \
  --env-file secrets.env
```

### CI mode — GitHub Actions via reusable workflow

Run verify-pr in CI using a reusable workflow + thin shim pattern, matching
fullsend's own `reusable-triage.yml` architecture. This follows
[rhdh-fullsend](https://github.com/redhat-developer/rhdh-fullsend/blob/main/docs/repo-onboarding.md)
Method 2.

**Architecture:**

```
sdlc-plugins/.github/workflows/
├── reusable-verify-pr.yml    # workflow_call — full pipeline
└── fullsend-verify-pr.yml    # workflow_dispatch — thin shim
```

The **reusable workflow** (`reusable-verify-pr.yml`) handles the full
pipeline: checkout fullsend upstream defaults at a pinned tag (v0.17.0),
checkout sdlc-plugins skill files as an overlay layer, prepare the
workspace, authenticate via fullsend's `setup-gcp` action (WIF +
`prepare-sandbox-credentials.sh` for OIDC token rewriting), set up agent
env vars via `setup-agent-env.sh` (strips `VERIFY_PR_` prefix), checkout
the target repo into `target-repo/`, and run the agent via fullsend's
composite action.

The **thin shim** (`fullsend-verify-pr.yml`) is a `workflow_dispatch`
trigger that calls the reusable workflow, mapping repo secrets to the
expected input/secret names.

Other repos adopt verify-pr by creating just the thin shim pointing to
the reusable workflow. No file duplication, no custom GCP auth.

**Prerequisites — GitHub repo secrets:**

GCP secrets must already exist (`GCP_WIF_PROVIDER`, `GCP_PROJECT_ID`,
`GCP_CLOUD_ML_REGION`). Create the Jira and GitHub secrets:

```bash
gh secret set JIRA_SERVER_URL --repo <owner/repo>
gh secret set JIRA_EMAIL --repo <owner/repo>
gh secret set JIRA_API_TOKEN --repo <owner/repo>
gh secret set JIRA_PROJECT_KEY --repo <owner/repo>
gh secret set GH_TOKEN --repo <owner/repo>
```

`GH_TOKEN` is a fine-grained PAT with **Pull requests: Read and write**
on the target repos where PRs will be verified. Required when the mint
is not configured, because `github.token` is scoped to the workflow's
repo and cannot comment on PRs in other repos. When the mint is adopted,
this secret can be removed (the minted token provides cross-repo access).

**Trigger:**

```bash
gh workflow run fullsend-verify-pr.yml \
  --repo <owner/repo> \
  --field jira_issue_id=<issue-id>
```

Note: `--ref` is only needed when the workflow file is not on the default
branch (e.g., `--ref run-in-fullsend` for sdlc-plugins during the spike).
Target repos with the workflow merged to `main` do not need `--ref`.

**Updating skill files:** the `sdlc_plugins_ref` input on the reusable
workflow defaults to `run-in-fullsend`. Target repos can override it to
pin to a specific commit SHA for reproducibility. The `fullsend_ai_ref`
input pins the fullsend upstream version (default `v0.17.0`).

See `.github/workflows/reusable-verify-pr.yml` and
`.github/workflows/fullsend-verify-pr.yml`.

### Keeping target repos up to date

When sdlc-plugins publishes a new version, target repos need to bump three
values in their harness YAML: the two SHA-256 hashes (agent, policy) and the
image tag.

Use [Renovate](https://docs.renovatebot.com/) or
[Dependabot](https://docs.github.com/en/code-security/dependabot) to automate
this. On each sdlc-plugins release, the bot computes new hashes, opens a PR
to bump them, and the maintainer merges when ready. This is the same model
used for GitHub Actions SHA pinning.

The env template files (`gcp-vertex.env`, `jira.env`, `github.env`) are pure
`${VAR}` placeholders and rarely change — they do not need version tracking.

When [fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113) is
resolved, the custom image is eliminated: the plugin is also URL-referenced,
and the image becomes the standard `fullsend-code:latest`. This reduces the
bump to two hashes + one plugin hash — still automated by Renovate.

## Design decisions

### Why the plugin directory is the fullsend dir

Fullsend's `--fullsend-dir` requires all referenced files (harness, agents,
policies, env, skills) to be inside that directory — paths that resolve outside
are rejected for security. By placing the fullsend config files alongside the
existing plugin files, both Claude Code users and fullsend users consume the
same skill definitions with zero duplication.

### Why one image for all skills

The policy (not the image) controls what each skill can access. All skills need
the same tools (Claude Code, Git, GH CLI, Python) and the same plugin. Building
per-skill images would multiply build time and storage with no security benefit —
the sandbox policy is the enforcement layer.

### Why `--dangerously-skip-permissions`

Fullsend launches Claude Code with `--dangerously-skip-permissions` because the
sandbox policy is the permission layer. Claude Code's built-in permission prompts
are designed for interactive use; inside a headless sandbox, the OpenShell network
and filesystem policies enforce the same boundaries without user interaction.

### Why Jira REST API instead of MCP

MCP servers are not available inside the sandbox — they run as separate processes
that require localhost network access and configuration that doesn't transfer
into the container. Skills detect MCP unavailability and fall back to the Jira
REST API v3 using env vars (`JIRA_SERVER_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`).

### Credential delivery tiers

Per [ADR-0025](https://github.com/fullsend-ai/fullsend/blob/main/docs/ADRs/0025-provider-credential-delivery-for-sandboxed-agents.md),
credentials use the highest isolation tier possible:

| Service | Tier | Model | Credentials in sandbox? |
|---|---|---|---|
| Jira | 2 | OpenShell provider (`providers/jira.yaml`) | No — gateway proxy swaps placeholder tokens |
| GitHub | 2 | OpenShell provider (`providers/github.yaml`) | No — gateway proxy swaps placeholder tokens |
| GCP Vertex AI | 4 | Host file (`${GOOGLE_APPLICATION_CREDENTIALS}`) | Yes — file-based auth requires local JWT signing |

Tier 1 (prefetch + post-process with zero credential access) is partially
achieved: the pre_script pre-fetches the Jira issue, and the post_script
handles all writes. The sandbox still needs runtime GitHub API access for
PR diff, reviews, and CI status.

## Comparison with fullsend canonical patterns

Full comparison of our approach against fullsend's conventions. References are
permalinked to fullsend commit `58cc443`.

| Aspect | Fullsend canonical | Our approach | Aligned? | Justification or convergence plan | References |
|---|---|---|---|---|---|
| Harness YAML location | `harness/<agent>.yaml` | `harness/verify-pr.yaml` | ✓ | — | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md) |
| Agent prompts | `agents/<agent>.md` with YAML frontmatter | `agents/verify-pr.md` with frontmatter | ✓ | — | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md) |
| Policies | `policies/<agent>.yaml` | `policies/verify-pr.yaml` | ✓ | — | [ADR-0020](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0020-composable-single-responsibility-agents-with-individual-sandboxes.md) |
| Env templates | `env/*.env` with `${VAR}` + `expand: true` | Same pattern | ✓ | — | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md) |
| GCP creds via host_files | `${GOOGLE_APPLICATION_CREDENTIALS}` mounted | Same | ✓ | — | [running-agents-locally.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/running-agents-locally.md) |
| Security scanning | `security: enabled: true` (default) | Same | ✓ | — | [runtimes.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/runtimes.md) |
| Skills loading | `skills:` field — uploaded from host at runtime | Baked into image via marketplace cache | Diverges | **Interim**: custom image bakes plugin into marketplace cache. `plugins:` field is for Claude Code marketplace plugins (not just LSP). **Target**: plugin referenced via URL in harness once fullsend adds URL support for `plugins:` field in `ResolveHarness()`. Tracked in [fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113). | [customizing-with-skills.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-with-skills.md), [runtimes.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/runtimes.md), [ADR-0038](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0038-universal-harness-access.md) |
| Plugin loading | `plugins:` field — marketplace cache created at runtime | Baked into image at build time | Diverges | **Interim**: same root cause as skills loading — `plugins:` field does not support URL references today, so build-time baking is the only option without duplication. **Target**: converges with skills loading when [fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113) is resolved. | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md), [ADR-0038](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0038-universal-harness-access.md) |
| Pre/post scripts | `pre_script` + `post_script` for split-trust | `post_script` executes structured JSON actions from sandbox output | ✓ | **Converged**: sandbox produces `agent-result.json` with ordered actions. `post_script` resolves `{{ref.key}}` placeholders and executes writes (Jira sub-tasks, PR replies, report posting). `validation_loop` validates output against JSON schema before post_script runs. | [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md), [security-threat-model.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/problems/security-threat-model.md) |
| Validation loop | `validation_loop:` with script + `max_iterations` | Strip extra properties then validate against schema | ✓ | **Converged**: `strip_extra_properties.py` recursively removes properties not declared in the schema (using `additionalProperties: false` nodes) before `jsonschema` validates. This avoids burning retry iterations on benign metadata the agent adds (e.g., `is_review_body`). The schema stays strict (documents the contract), the stripping makes it forgiving. Fullsend's agents handle this via prompt instructions listing rejected field names; our approach is deterministic and schema-driven. | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md), [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md) |
| CI reusable workflow | `reusable-<role>.yml` + thin shim | `reusable-verify-pr.yml` + `fullsend-verify-pr.yml` | ✓ | **Converged**: follows `reusable-triage.yml` pattern. Uses `setup-gcp` action for WIF + `prepare-sandbox-credentials.sh`, `setup-agent-env.sh` for env prefix stripping, `target-repo/` checkout. Other repos adopt by creating the thin shim only. | [reusable-triage.yml](https://github.com/fullsend-ai/fullsend/blob/v0.17.0/.github/workflows/reusable-triage.yml) |
| Config directory | Dedicated `.fullsend` repo per org | Three modes: local (`--fullsend-dir`), remote (URL refs), CI (reusable workflow) | Diverges | **Local mode**: plugin dir as `--fullsend-dir`. **Remote mode**: per-repo `.fullsend/` with URL-referenced agent/policy. **CI mode**: reusable workflow fetches skill files at runtime. **Target**: standard `fullsend-code` image + plugin via URL when [fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113) is resolved. | [ADR-0003](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0003-org-config-repo-convention.md), [ADR-0035](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0035-layered-content-resolution.md), [ADR-0038](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0038-universal-harness-access.md) |
| Layered resolution | Three-tier: upstream < org < per-repo | Single layer — no overrides | Diverges | **Keep**: per-repo `.fullsend/` with URL refs is the correct tier for external skills consumed across multiple orgs. Org-level `.fullsend` repo with `customized/` is possible but requires copying files on each release — Renovate on per-repo URL refs is lower maintenance. | [ADR-0035](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0035-layered-content-resolution.md) |
| AGENTS.md | Auto-loaded from target repo | Not shipped | Diverges | **Converge now**: recommend target repos create symlink `AGENTS.md → CLAUDE.md`. Verified that fullsend preserves symlinks through upload/download cycle (`UploadDir` uses `tar` without `--dereference`, `sanitizeDownload` allows relative in-repo symlinks, `hasAgentsMD` detects symlink as existing file). Document in fullsend.md. | [customizing-with-agents-md.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-with-agents-md.md), [ADR-0020](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0020-composable-single-responsibility-agents-with-individual-sandboxes.md) |
| `.agents/skills/` convention | Skills in `.agents/skills/` + symlink to `.claude/skills/` | Skills in `skills/` (Claude Code plugin format) | Different convention | **Keep**: Claude Code plugin format (`plugin.json` + `skills/`) predates `.agents/skills/`. Both are valid for different discovery mechanisms. No benefit converting — Claude Code discovers plugins via marketplace cache, not `.agents/skills/`. | [customizing-with-skills.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-with-skills.md) |
| Output schemas | `schemas/` directory for JSON validation | `schemas/verify-pr-result.schema.json` | ✓ | **Converged**: JSON Schema defines action types, cross-reference format, and report structure. Validated by `validation_loop` before post_script runs. | [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md) |

## Known issues

- **fullsend deletes the target repo directory** after each run
  ([#2075](https://github.com/fullsend-ai/fullsend/issues/2075)). Always use
  a disposable clone as `--target-repo`, never your working directory.
- **macOS AppleDouble file corruption** in `.git/objects/pack/` after fullsend
  runs ([#2032](https://github.com/fullsend-ai/fullsend/issues/2032)). Fixed
  in fullsend by adding `COPYFILE_DISABLE=1` to the tar command.

## Available skills

| Skill | Harness | Status |
|---|---|---|
| verify-pr | `harness/verify-pr.yaml` | Working |
| implement-task | — | Not yet added |
| plan-feature | — | Not yet added |
| define-feature | — | Not yet added |
