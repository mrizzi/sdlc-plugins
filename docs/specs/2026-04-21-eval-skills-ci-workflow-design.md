# Eval Skills CI Workflow

**Date**: 2026-04-21
**Scope**: GitHub Actions workflows for running skill evals in CI and storing baselines
**Jira**: TC-4149 (part of TC-4144 — Skill evaluation framework for sdlc-workflow)

## Overview

Two independent GitHub Actions workflows that automate skill eval execution:

1. **eval-baseline.yml** — on push to main, runs all evals and commits baseline results
2. **eval-pr.yml** — on PR, runs evals for changed skills and posts a benchmark delta comment

Together they prove that skill-creator with subagent spawning works in headless CI and establish the foundation for an automated regression gate.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Workflow count | 2 separate files | Independent triggers, permissions, and behaviors; easier to enable/disable independently |
| Eval invocation | Single `claude -p` per skill | Mirrors the README's validated pattern; skill-creator handles subagent orchestration internally |
| Push-to-main scope | Run all evals | Ensures every baseline is complete across all skills |
| PR scope | Changed skills only | Token-efficient; uses `git diff` to map changed skill/eval files to eval suites |
| Baseline lookup | `latest` symlink | Avoids exact-hash misses when main HEAD has no baseline (unrelated commits between eval-triggering pushes) |
| Permission mode | `--dangerously-skip-permissions` | Simplest for initial proof; ephemeral CI runner limits blast radius; tighten later |
| Install method | `curl` (native installer) | Matches existing `validate-plugins.yml`; Anthropic's recommendation |
| Missing baseline | Skip with warning | Non-blocking; reports raw PR results without delta |
| Eval failure | Log warning, continue | Never blocks the workflow; feasibility proof, not a merge gate |

## Workflow 1: eval-baseline.yml (push to main)

### Trigger

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'plugins/sdlc-workflow/skills/**/*.md'
      - 'evals/**/evals.json'
```

### Permissions

`contents: write` — needs to commit baselines back to main.

### Steps

1. **Checkout** — `actions/checkout@v4`
2. **Install Claude Code** — `curl -fsSL https://claude.ai/install.sh | bash`
3. **Discover all eval suites** — find every `evals/*/evals.json`, extract skill names. No filtering — run all skills to ensure complete baselines.
4. **Run evals** — for each skill, one `claude -p` invocation:
   - Prompt references skill-creator and the skill's `evals.json`
   - `--dangerously-skip-permissions` for full autonomous access
   - Workspace via `mktemp -d /tmp/<skill>-eval-<hash>-XXXXXX`
   - On failure: log `::warning::`, continue to next skill
5. **Collect results** — copy workspace outputs into `evals/<skill>/baselines/<commit-hash>/`:
   - `eval-N/grading.json`, `eval-N/timing.json`, `eval-N/outputs/`
   - `benchmark.json`, `feedback.json`
   - Handle both `iteration-N/` and flat workspace layouts from skill-creator
   - Create `feedback.json` placeholder if skill-creator didn't produce one
6. **Update `latest` symlink** — for each skill, create or update `evals/<skill>/baselines/latest` as a relative symlink pointing to `<hash>/`
7. **Commit and push** — `github-actions[bot]` commits baselines and symlinks

### No infinite loop risk

Baseline commits write to `evals/<skill>/baselines/<hash>/{benchmark.json, grading.json, ...}`. The trigger glob `evals/**/evals.json` matches only `evals.json` filenames, not these result files. The other trigger `plugins/sdlc-workflow/skills/**/*.md` is unrelated. So baseline commits cannot re-trigger the workflow.

## Workflow 2: eval-pr.yml (pull request)

### Trigger

```yaml
on:
  pull_request:
    branches: [main]
    paths:
      - 'plugins/sdlc-workflow/skills/**/*.md'
      - 'evals/**/evals.json'
```

### Permissions

- `contents: read`
- `pull-requests: write` — needs to post/update PR reviews

### Steps

1. **Checkout** — `actions/checkout@v4` with `fetch-depth: 0` (needs full history for `git diff`)
2. **Install Claude Code** — `curl -fsSL https://claude.ai/install.sh | bash`
3. **Discover changed skills** — `git diff --name-only` against PR base:
   - Changed `plugins/sdlc-workflow/skills/<name>/**` maps to `evals/<name>/`
   - Changed `evals/<name>/**` maps to `evals/<name>/`
   - Skip skills that have no `evals/<name>/evals.json`
4. **Resolve baselines** — for each changed skill, read `evals/<skill>/baselines/latest` symlink to get the baseline hash. If `latest` doesn't exist, skip that skill with a warning.
5. **Run pr-branch evals** — one `claude -p` invocation per changed skill:
   - Prompt tells skill-creator to skip base-branch runs (stored baselines serve that role)
   - `--dangerously-skip-permissions`
   - Workspace via `mktemp`
   - On failure: log `::warning::`, continue
6. **Collect PR results** — extract grading/timing from workspace into `/tmp/<skill>-pr-results/`
7. **Compute delta** — compare PR results against stored baseline's `benchmark.json`:
   - Pass rate, token usage, duration
   - If no baseline exists for a skill, report raw results without delta
8. **Post PR review** — `actions/github-script` creates or updates a PR review (`COMMENT` event) with:
   - Per-skill delta table (baseline vs PR vs delta)
   - Fallback to per-eval grading table when no `benchmark.json` is available
   - Warning messages for missing baselines or failed runs

## Changed-Skill Discovery (PR only)

Maps changed files to eval suites via `git diff --name-only`:

| Changed path pattern | Eval suite |
|---------------------|------------|
| `plugins/sdlc-workflow/skills/<name>/**` | `evals/<name>/` |
| `evals/<name>/**` | `evals/<name>/` |

Skills without a corresponding `evals/<name>/evals.json` are skipped silently.

## Baseline Storage Structure

```
evals/<skill>/baselines/
├── latest -> <hash>/          # relative symlink, always points to most recent
├── <hash-1>/
│   ├── benchmark.json
│   ├── feedback.json
│   ├── eval-1/
│   │   ├── grading.json
│   │   ├── timing.json
│   │   └── outputs/
│   ├── eval-2/
│   │   └── ...
│   └── ...
└── <hash-2>/
    └── ...
```

## Claude Code Invocation

Both workflows use the same invocation pattern:

```bash
claude -p "<prompt>" --dangerously-skip-permissions
```

The prompt describes the task in natural language (slash commands are interactive-only in `-p` mode). skill-creator is referenced by name and Claude invokes it via the Skill tool.

### Environment

- `ANTHROPIC_API_KEY` from repository secrets
- Install: `curl -fsSL https://claude.ai/install.sh | bash`

## Error Handling

- `claude -p` failure: log `::warning::`, continue to next skill. Never block the workflow.
- Missing `latest` symlink in PR job: skip delta for that skill, report raw results with a warning.
- No changed skills discovered (PR job): job skips gracefully.
- No eval suites discovered (baseline job): job skips gracefully.

## Security Considerations

- `--dangerously-skip-permissions` gives Claude unrestricted access to the runner filesystem. Acceptable because:
  - Runners are ephemeral (no persistent state at risk)
  - No secrets are exposed beyond `ANTHROPIC_API_KEY`
  - This is a feasibility proof, not a production gate
- Future hardening: migrate to `--permission-mode dontAsk` with `--allowedTools` once tool requirements are known from initial runs.

## Out of Scope

- CI as a hard merge gate (per TC-4144)
- Multi-run statistical evaluation (future: 3-5 runs per config)
- Cross-skill regression detection via shared template change tracking
- Permission mode hardening beyond `--dangerously-skip-permissions`
