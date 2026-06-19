# Fullsend Integration for sdlc-workflow

Run sdlc-workflow skills inside OpenShell sandboxes via fullsend's harness
system. Skills are baked into container images at build time with zero
duplication — the same skill files serve both Claude Code plugin users and
fullsend users.

## Context

Direct OpenShell integration (TC-4713) produced working sandboxes but
required 7 manual steps per session: building images, uploading GCP
credentials, setting env vars, configuring `CLAUDE_CONFIG_DIR`,
`NODE_EXTRA_CA_CERTS`, and more. Fullsend solves all of this with a
declarative harness YAML and a single `fullsend run` command.

This spec defines the integration approach: pre-built container images
with the plugin baked in, consumed by thin fullsend harness configs that
only inject runtime secrets.

## Architecture

```
┌───────────────────────────────────────────────────────┐
│  Git repo: mrizzi/sdlc-plugins                        │
│                                                       │
│  plugins/sdlc-workflow/                               │
│    skills/          ← SINGLE SOURCE OF TRUTH          │
│    shared/                                            │
│    .claude-plugin/                                    │
│    sandboxes/base/  ← Dockerfile                      │
└─────────────┬─────────────────────────────────────────┘
              │ CI builds
              ▼
┌───────────────────────────────────────────────────────┐
│  GHCR: ghcr.io/mrizzi/sdlc-plugins/                   │
│                                                       │
│  Single image for all skills:                         │
│    sdlc-base:latest                                   │
│                                                       │
│  Image extends fullsend-code:latest and adds:         │
│    - sdlc-workflow plugin in marketplace cache format │
│                                                       │
│  Policy (not image) controls per-skill access         │
└─────────────┬─────────────────────────────────────────┘
              │
              ▼
┌───────────────────────────────────────────────────────┐
│  Fullsend config (in plugins/sdlc-workflow/)          │
│                                                       │
│  harness/verify-pr.yaml     ← image + policy + env   │
│  agents/verify-pr.md        ← thin agent prompt       │
│  policies/verify-pr.yaml    ← OpenShell policy        │
│  schemas/verify-pr-result.schema.json ← output schema │
│  scripts/pre-verify-pr.sh   ← input validation        │
│  scripts/post-verify-pr.sh  ← action execution        │
│  scripts/execute-actions.py ← ref resolution + writes │
│  env/gcp-vertex.env         ← Vertex AI config        │
│  env/jira.env               ← Jira REST API config    │
│  env/github.env             ← GitHub token config      │
│                                                       │
│  NO skills/ — they're in the image                    │
│  NO plugins/ — they're in the image                   │
└───────────────────────────────────────────────────────┘
```

### Split-Trust Execution Model

Fullsend's security architecture separates trusted (runner) from untrusted
(sandbox) execution. The verify-pr skill converges with this model:

```
Runner (trusted)                    Sandbox (untrusted)
─────────────────                   ───────────────────
1. pre_script                       3. Agent runs skill
   - Validate JIRA_ISSUE_ID            - Reads Jira issue
   - Verify issue has PR               - Reads PR diff/reviews
   - Verify PR is open                 - Dispatches sub-agents
   - Fail fast on bad inputs           - Produces agent-result.json
                                        (structured JSON output)
2. Create sandbox + run agent
                                    4. validation_loop
                                       - Validates JSON against schema
                                       - Up to 2 iterations on failure

5. post_script
   - Reads agent-result.json
   - Creates Jira sub-tasks
   - Creates issue links
   - Posts PR comment replies
   - Posts verification report
   - Resolves {{ref.key}} placeholders
```

Write operations never happen inside the sandbox. The sandbox policy allows
read-only access to Jira and GitHub APIs. All writes are executed by the
post_script on the trusted runner using credentials from `runner_env`.

## Zero-Duplication Model

Skills live in one place: `plugins/sdlc-workflow/skills/` in the Git repo.

| Consumer | How skills are loaded |
|---|---|
| Claude Code plugin users | Install via marketplace (`mrizzi/sdlc-plugins`). Claude Code discovers `plugin.json` and loads skills from the installed plugin directory. |
| Fullsend users | `fullsend run verify-pr`. The pre-built image has the plugin baked into the Claude Code marketplace cache at `$CLAUDE_CONFIG_DIR/plugins/`. Claude Code auto-discovers it — no `--plugin-dir`, no host-side files. |
| Direct OpenShell users | `openshell sandbox create --from <image>`. Same image, manual env var setup. |

## Image Build

### Marketplace cache structure

The Dockerfile bakes the plugin into the Claude Code marketplace cache
format so it's auto-discovered when `CLAUDE_CONFIG_DIR` is set:

```
/tmp/claude-config/
  settings.json
  plugins/
    marketplaces/claude-plugins-official/
      .claude-plugin/marketplace.json
      plugins/sdlc-workflow/README.md
    cache/claude-plugins-official/sdlc-workflow/1.0.0/
      README.md
    installed_plugins.json
    known_marketplaces.json
    sdlc-workflow/
      .claude-plugin/plugin.json
      skills/verify-pr/SKILL.md
      shared/task-description-template.md
      ...
```

This replicates what fullsend's `bootstrapPlugins()` function creates at
runtime, but baked into the image at build time. The structure was verified
by reading `internal/runtime/claude.go:bootstrapPlugins` and
`buildPluginConfigs` in the fullsend codebase.

### Base image

Hummingbird `core-runtime:latest-builder` with OpenShell compatibility:

- `claude-code` (official RPM repo)
- `gh` (GitHub official RPM repo)
- `git`, `openssh-server`, `openssh-clients`, `python3`, `jq`, `iproute`,
  `procps-ng`, `tar`, `gzip`
- `supervisor` + `sandbox` users
- `WORKDIR /sandbox`

### Per-skill images

Two-line Dockerfiles extending the base:

```dockerfile
FROM ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest
COPY policy.yaml /etc/openshell/policy.yaml
```

## Fullsend Harness

### Harness YAML (per skill)

```yaml
# harness/verify-pr.yaml
agent: agents/verify-pr.md
model: opus
image: ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest
policy: policies/verify-pr.yaml

security:
  enabled: true

host_files:
  - src: env/gcp-vertex.env
    dest: /tmp/workspace/.env.d/gcp-vertex.env
    expand: true
  - src: env/jira.env
    dest: /tmp/workspace/.env.d/jira.env
    expand: true
  - src: env/github.env
    dest: /tmp/workspace/.env.d/github.env
    expand: true
  - src: ${GOOGLE_APPLICATION_CREDENTIALS}
    dest: /tmp/gcp-creds.json
  - src: ${GCP_OIDC_TOKEN_FILE}
    dest: /tmp/gcp-oidc-token
    optional: true

validation_loop:
  script: scripts/validate-output-schema.sh
  max_iterations: 2

pre_script: scripts/pre-verify-pr.sh
post_script: scripts/post-verify-pr.sh

runner_env:
  JIRA_SERVER_URL: "${JIRA_SERVER_URL}"
  JIRA_EMAIL: "${JIRA_EMAIL}"
  JIRA_API_TOKEN: "${JIRA_API_TOKEN}"
  JIRA_PROJECT_KEY: "${JIRA_PROJECT_KEY}"
  GH_TOKEN: "${GH_TOKEN}"
  FULLSEND_OUTPUT_SCHEMA: "${FULLSEND_DIR}/schemas/verify-pr-result.schema.json"
  FULLSEND_OUTPUT_FILE: "agent-result.json"

timeout_minutes: 30
```

No `skills:` or `plugins:` fields — the image has everything. Security is
enabled so fullsend runs pre-agent scans (context injection detection, secret
scanning). The `pre_script` validates inputs before sandbox creation. The
`validation_loop` validates structured output against the JSON schema. The
`post_script` executes all write operations on the trusted runner.

### Agent prompt (per skill)

```markdown
# agents/verify-pr.md

You are running inside an OpenShell sandbox with the sdlc-workflow plugin
pre-installed. The plugin provides skills for AI-assisted SDLC workflow.

Execute the verify-pr skill: /sdlc-workflow:verify-pr

Read the Jira task ID from the GITHUB_ISSUE_URL or ISSUE_NUMBER environment
variable, or from the agent input.
```

Agent prompts are thin wrappers (~5 lines) that tell Claude which skill to
invoke. The actual skill logic is in the image.

### Environment files

```bash
# env/gcp-vertex.env
export CLAUDE_CODE_USE_VERTEX=1
export ANTHROPIC_VERTEX_PROJECT_ID=${ANTHROPIC_VERTEX_PROJECT_ID}
export CLOUD_ML_REGION=${CLOUD_ML_REGION}
export GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-creds.json
export GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
export NODE_EXTRA_CA_CERTS=/etc/openshell-tls/ca-bundle.pem
```

```bash
# env/jira.env
export JIRA_SERVER_URL=${JIRA_SERVER_URL}
export JIRA_EMAIL=${JIRA_EMAIL}
export JIRA_API_TOKEN=${JIRA_API_TOKEN}
```

### User-provided secrets

```bash
# secrets.env (user creates, never committed)
ANTHROPIC_VERTEX_PROJECT_ID=my-project
CLOUD_ML_REGION=global
GOOGLE_CLOUD_PROJECT=my-project
GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa-key.json
JIRA_SERVER_URL=https://myorg.atlassian.net
JIRA_EMAIL=me@example.com
JIRA_API_TOKEN=my-token
GH_TOKEN=ghp_xxx
```

## User Experience

### Fullsend users

```bash
fullsend run verify-pr \
  --fullsend-dir /path/to/.fullsend \
  --target-repo /path/to/my-repo \
  --env-file secrets.env
```

One command. Fullsend handles: sandbox creation, image pull, GCP credential
upload, env var injection, Claude Code launch with `--agent`, sandbox
cleanup.

### Claude Code plugin users (unchanged)

Install via marketplace. No change to the existing experience.

### Direct OpenShell users

Use the same images with manual setup (documented in sandboxes/README.md).

## Policy Files

Policies live in the `.fullsend` config directory under `policies/`. They
are the same files currently under `sandboxes/*/policy.yaml`, moved (or
symlinked) to `policies/`.

Each policy follows the verified OpenShell format:
- `name:` field on each network policy entry
- `*.googleapis.com` prefix wildcards (not mid-string)
- `**/claude` double-star binary globs
- `landlock: compatibility: best_effort`
- `/var/log` in `read_only`, `/sandbox` as appropriate

## Scope

### Phase 1 — PoC (done)

- Base Dockerfile extending `fullsend-code:latest` with plugin in marketplace cache
- Harness, agent prompt, policy, env files for verify-pr
- Manual `fullsend run` with `--no-post-script` (side effects inside sandbox)

### Phase 2 — Structured output convergence (done)

- JSON Schema for verify-pr structured output (`schemas/verify-pr-result.schema.json`)
- Action executor with `{{ref.key}}` placeholder resolution (`scripts/execute-actions.py`)
- Post_script for deterministic action execution (`scripts/post-verify-pr.sh`)
- Validation loop integration (`scripts/validate-output-schema.sh`)
- Skill sandbox mode detection (`FULLSEND_OUTPUT_DIR`)
- Sandbox policy renamed to reflect read-only intent
- `jira-client.py` extended with `--description-adf` and `--comment-adf` flags

### Phase 3 — Input validation (next)

- Pre_script for input validation (`scripts/pre-verify-pr.sh`)
- Validate `JIRA_ISSUE_ID` exists and issue has a linked PR before sandbox creation
- Fail fast on invalid inputs to avoid wasting sandbox compute time

### Phase 4 (future)

- Remaining skills: implement-task, plan-feature, define-feature
- CI pipeline for building and publishing images to GHCR
- GitHub Actions workflow for running skills via fullsend in CI
- Remote deployment mode with URL-referenced resources and Renovate-based updates

## Verified Assumptions

All assumptions were verified by reading fullsend source code via Serena:

| Assumption | Verified in |
|---|---|
| Fullsend sets `CLAUDE_CONFIG_DIR` automatically | `ClaudeRuntime.EnvExports()` in `internal/runtime/claude.go:28` |
| Skills are uploaded from `h.Skills[]` paths | `Bootstrap()` in `internal/runtime/claude.go:52` |
| Plugins get marketplace cache structure | `bootstrapPlugins()` in `internal/runtime/claude.go:295` |
| Claude runs with `--agent --print --dangerously-skip-permissions` | `buildRunCommand()` in `internal/runtime/claude.go:182` |
| Skill paths must be inside `--fullsend-dir` | `ResolveRelativeTo()` in `internal/harness/harness.go:327` |
| URL-referenced skills need SHA-256 hash | `resolveURL()` in `internal/resolve/resolve.go:69` |
| `host_files` with `expand: true` handles env var injection | `bootstrapEnv()` in `internal/cli/run.go` |
| Image can be any custom image | `sandbox.Create()` passes `--from <image>` directly |

## Lessons Learned (from direct OpenShell integration)

| Issue | Root cause | How fullsend solves it |
|---|---|---|
| Sandbox supervisor exit code 1 | Missing `iproute`, `openssh-server`, `supervisor` user | Community base or our fixed Hummingbird image handles this |
| Policy YAML format errors | Missing `name:` field, mid-string wildcards, glob binaries | Verified format against fullsend's production policies |
| Claude Code hangs in interactive mode | TUI doesn't work in sandbox SSH | Fullsend uses `--print` mode exclusively |
| Claude Code hangs silently | `CLAUDE_CONFIG_DIR` not writable (Landlock) | Fullsend sets `CLAUDE_CONFIG_DIR=/tmp/claude-config` (writable) |
| Claude Code exits with no output | Missing `NODE_EXTRA_CA_CERTS` for TLS proxy | Fullsend's image bakes the CA symlink; our env sets it |
| 7 manual steps per session | No automation layer | Fullsend: one command |
