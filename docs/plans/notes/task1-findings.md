# Task 1 findings — Environment + delivery/resolution confirmation

**Jira:** [TC-5805](https://redhat.atlassian.net/browse/TC-5805) (Epic A: Delivery foundation, parent TC-5800)
**Date:** 2026-08-27
**fullsend CLI:** v0.37.0 (built from `github.com/fullsend-ai/fullsend` tag `v0.37.0`)

## IMAGE digest

```
IMAGE=ghcr.io/fullsend-ai/fullsend-code@sha256:9743bc7b6e451e0bcea25ae4a67e0c040c296f1fee04c08988ae80c53fafcfe6
```

Source: `image:` in `/Users/mrizzi/git/cloned/agents/harness/review.yaml`.

## 1. Toolchain — fullsend v0.37.0

Built with the version ldflag (plain `go build` stamps `version dev`):

```bash
go build -C /Users/mrizzi/git/cloned/fullsend \
  -ldflags "-X github.com/fullsend-ai/fullsend/internal/cli.version=v0.37.0" \
  -o /Users/mrizzi/.local/bin/fullsend ./cmd/fullsend
fullsend --version   # -> fullsend version v0.37.0
```

**Confirmed:** `fullsend --version` reports `v0.37.0`.

## 2. Stock image binaries

`podman run --rm --entrypoint "" "$IMAGE" bash -lc 'command -v <bin> ...'`:

| binary  | path                        |
|---------|-----------------------------|
| claude  | /usr/local/bin/claude       |
| node    | /usr/bin/node               |
| python3 | /sandbox/.venv/bin/python3  |
| gh      | /usr/bin/gh                 |
| git     | /usr/bin/git                |
| jq      | /usr/bin/jq                 |
| curl    | /usr/bin/curl               |

**Confirmed:** all required binaries present, none MISSING. `claude`/`node`/`python3`/`gh`/`git`
all resolve (python3 = `/sandbox/.venv/bin/python3`, required for ADR-0090 python sandbox hooks).

➡️ **TC-5806 (sandbox image extension) is a NO-OP** — no required binary is missing.

## 3. Root-level harness resolution

Validated against a throwaway probe (`role: verify-pr`, `plugins: [plugins/sdlc-workflow]`,
`image: $IMAGE`) run from the repo root; probe never committed (working tree clean afterwards).

**Confirmed:** a root-level harness bases its relative children at the repo root, so
`plugins/sdlc-workflow` resolves in place and the `sdlc-workflow:verify-pr` skill is present
with its sibling `shared/` intact:

- `plugin.json` name = `sdlc-workflow`; `skills/` and `shared/` are siblings at the plugin root.
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` exists; the skill's `../../shared/*.md`
  links resolve to `plugins/sdlc-workflow/shared/` (comment-footnote.md, jira-rest-fallback.md, …).
- Skill id therefore = `sdlc-workflow:verify-pr`.

Evidence chain (resolution-only, no dispatch):

- `fullsend agent add harness/probe-verify-pr.yaml --name probe-verify-pr --fullsend-dir .`
  → `✓ Added agent "probe-verify-pr"` (the root-level harness path resolves at the repo root).
- `fullsend lock probe-verify-pr --fullsend-dir . --offline --max-depth 0`
  → loads + validates the harness and runs `ResolveRelativeTo(absFullsendDir)` with **no**
  "resolves outside fullsend directory" error → `plugins/sdlc-workflow` resolves cleanly
  inside the repo root; "no remote dependencies" confirms it is treated as a local, in-place path.
- Source confirmation (fullsend v0.37.0):
  - `internal/cli/run.go:464` and `internal/cli/lock.go:248` call
    `Harness.ResolveRelativeTo(absFullsendDir)` — relative local paths resolve against the
    **fullsend-dir**, which must be the repo root.
  - `internal/cli/run.go:670` calls `Harness.ValidateFilesExist()`, which `os.Stat`s every
    plugin path (`internal/harness/harness.go:798`).

### ⚠️ Deviations from the task's literal commands (important for TC-5807)

These are real constraints the delivery model must account for; the task's example commands
do **not** work verbatim on fullsend v0.37.0:

1. **`--fullsend-dir` must be the repo root**, not a scratch `/tmp` dir. fullsend resolves the
   harness source path *and* the harness's relative children (`plugins/…`) against
   `absFullsendDir` = the `--fullsend-dir` value (`ResolveRelativeTo`, `validateLocalPath`).
   With `--fullsend-dir /tmp/probe-fs` the probe fails
   (`local path does not exist: /tmp/probe-fs/harness/probe-verify-pr.yaml`) and
   `plugins/sdlc-workflow` would resolve under `/tmp`, not the repo. The probe here used
   `--fullsend-dir .` at the repo root and a scratch `config.yaml`/`harness/` (both removed).

2. **`verify-pr` is NOT a valid `config.yaml` role.** `config.yaml` `roles:` are validated
   against a fixed enum — `fullsend, triage, coder, review, fix, retro, prioritize, e2e`
   (`internal/config/config.go:196`); `verify-pr` is rejected
   (`invalid role "verify-pr": must be one of …`). The **harness** `role:` field is only
   regex-validated (`internal/harness/harness.go:474`), so `role: verify-pr` is accepted in the
   harness YAML. The scratch `config.yaml` therefore declared a valid enum role (`review`) while
   the harness kept `role: verify-pr`, and `agent add` succeeded. TC-5807 must reconcile this:
   the installation `config.yaml` cannot list `verify-pr` as a role in v0.37.0.

3. **`fullsend agent add` does not stage plugins.** It only validates the harness source path
   exists and records the source string in `config.yaml` (`internal/cli/agent.go:174-205`).
   Plugin resolution/staging and existence checks happen at `fullsend run` time. The
   `fullsend run … --offline --max-depth 0` "secondary gate" was **not** executed here because
   `fullsend run` sets up the sandbox and dispatches a real agent (not resolution-only);
   resolution was confirmed via `agent add` + `lock` + source review instead.

## Acceptance

- [x] `fullsend --version` reports v0.37.0; IMAGE digest recorded.
- [x] Required binaries present (none MISSING) → TC-5806 no-op.
- [x] Throwaway probe: `agent add` resolves the in-place plugin at the repo root;
      `sdlc-workflow:verify-pr` present with `skills/verify-pr/SKILL.md` + sibling `shared/`;
      probe removed (working tree clean).
- [x] Findings committed (trailers required).
