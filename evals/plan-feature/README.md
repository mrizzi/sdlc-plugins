# plan-feature Eval Framework

Structured evaluations for the `plan-feature` skill, using Anthropic's
[skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
as the eval engine. This document uses plan-feature as a concrete example,
but the eval pattern applies to any skill — see
[Adapting for other skills](#adapting-for-other-skills).

For architectural decisions and known limitations, see the
[design spec](../../docs/specs/2026-04-16-skill-eval-framework-design.md).

## Why evals live outside the plugin directory

Eval fixtures live at `evals/plan-feature/` (repo root) rather than inside
`plugins/sdlc-workflow/`. Test fixtures should not ship with production
artifacts, following the standard convention of `tests/` as a sibling of
`src/`. This is especially critical for adversarial fixtures containing
prompt injection payloads.

## Directory structure

```
evals/plan-feature/
├── README.md              # This file
├── evals.json             # Test case definitions and assertions
├── files/                 # Input fixtures (mock Jira features, repo manifests)
│   ├── feature-standard.md
│   ├── feature-ambiguous.md
│   ├── feature-multi-repo.md
│   ├── feature-adversarial.md
│   ├── repo-backend.md
│   ├── repo-frontend.md
│   └── figma-context.md
└── baselines/             # Committed baseline results (one dir per git commit)
    └── <commit-hash>/
        ├── benchmark.json
        ├── feedback.json
        ├── eval-1/
        │   ├── grading.json
        │   ├── timing.json
        │   └── outputs/
        │       ├── impact-map.md
        │       ├── task-1-slug.md
        │       └── ...
        ├── eval-2/
        │   └── ...
        ├── eval-3/
        │   └── ...
        └── eval-4/
            └── ...
```

The workspace directory (where skill-creator writes ephemeral run outputs) is
stored in `/tmp/` and is not committed to git.

## evals.json schema

`evals.json` defines the skill under test and an array of test cases:

```json
{
  "skill_name": "plan-feature",
  "evals": [
    {
      "id": 1,
      "prompt": "User prompt that exercises the skill...",
      "expected_output": "Human-readable description of what good output looks like.",
      "files": ["files/feature-standard.md", "files/repo-backend.md"],
      "assertions": [
        "Each task file contains all required template sections: Repository, Description, ...",
        "Task count is between 3 and 10 inclusive"
      ]
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `skill_name` | string | Name of the skill being evaluated |
| `evals[].id` | number | Unique identifier for the test case |
| `evals[].prompt` | string | The prompt sent to the skill agent |
| `evals[].expected_output` | string | Natural language description of expected behavior |
| `evals[].files` | string[] | Paths to fixture files (relative to the directory containing `evals.json`) |
| `evals[].assertions` | string[] | Assertions graded by the LLM judge after each run |

### Current test cases

| ID | Name | Purpose |
|----|------|---------|
| 1 | Standard feature | Well-structured Jira Feature, single backend repo. The golden path. |
| 2 | Ambiguous feature | Vague acceptance criteria, missing details. Tests gap awareness. |
| 3 | Multi-repo feature | Frontend + backend repos with Figma context. Tests cross-repo decomposition. |
| 4 | Adversarial feature | Prompt injection attempts embedded in the Feature description. Tests injection resistance. |

## Fixture file format

Fixture files in `files/` simulate what MCP tools would return during a real
skill invocation. The eval prompt instructs the agent to read these files
instead of calling external tools, and to write outputs to files instead of
making live API calls.

The fixture types below are specific to plan-feature — other skills would
have different mock data (e.g., mock PR diffs for verify-pr, mock task
descriptions for implement-task).

### Feature fixtures (`feature-*.md`)

Mock Jira Feature issues in Markdown. Each contains:

- Issue metadata (key, summary, status, labels)
- Feature description sections matching the Jira Feature template

### Repository manifests (`repo-*.md`)

Directory tree snapshots showing the target repository layout — key files,
module structure, and conventions. The skill uses these to ground file paths
in task descriptions.

### Figma context (`figma-context.md`)

Design context simulating output from Figma MCP tools, used by the
multi-repo test case.

### Annotation headers

Per `CONVENTIONS.md`, fixture files must include annotation headers:

- **Adversarial fixtures**: `<!-- ADVERSARIAL TEST FIXTURE — <purpose> -->`
- **Synthetic data fixtures**: `<!-- SYNTHETIC TEST DATA — <purpose> -->`

## Prerequisites

- **Anthropic's skill-creator** must be installed as a Claude Code plugin
  (see [installation](https://github.com/anthropics/skills/tree/main/skills/skill-creator))
- **The skill under test** must be accessible via its `/skill-name`
  slash-command in the Claude Code session
- **`evals.json`** with at least one test case (see schema above)
- **Fixture files** in `files/` referenced by `evals.json`

## Running evals

The eval pipeline has three stages:

1. **Execute** — for each test case in `evals.json`, run the skill with the
   given prompt and fixture files. The skill writes task descriptions and an
   impact map to an output directory.
2. **Grade** — an LLM judge evaluates each run's outputs against the
   assertions in `evals.json`, producing `grading.json` with pass/fail
   verdicts and evidence.
3. **Aggregate** — `aggregate_benchmark.py` reads all `grading.json` files
   and produces `benchmark.json` with summary statistics.

### Interactive: skill-creator

For iterative skill improvement with human-in-the-loop review, start a
Claude Code session in the repo root and run:

```
/skill-creator I have an existing skill /plan-feature with evals already
defined at @evals/plan-feature/evals.json. Run all 4 eval cases and grade
them against the assertions. For the workspace, run:
mktemp -d /tmp/plan-feature-eval-$(git rev-parse --short HEAD)-XXXXXX
```

`/plan-feature` references the skill under test by its slash-command name.
The `@` prefix on the evals.json path attaches the file to the prompt so
skill-creator can read it directly.

The `mktemp` command generates a unique workspace path per invocation
(e.g., `/tmp/plan-feature-eval-a45017c-xK9mPL`), avoiding collisions
when multiple sessions run concurrently.

### Non-interactive: `claude -p`

For CI or scripted runs without human review:

```bash
claude -p "/skill-creator I have an existing skill /plan-feature with evals \
  already defined at @evals/plan-feature/evals.json. Run all 4 eval cases \
  and grade them against the assertions. Skip the eval viewer. For the \
  workspace, run: \
  mktemp -d /tmp/plan-feature-eval-\$(git rev-parse --short HEAD)-XXXXXX" \
  --dangerously-skip-permissions
```

This runs the full pipeline (execute, grade, aggregate) in a single
command. Results land in the generated workspace directory (e.g.,
`/tmp/plan-feature-eval-bd5c260-yooaFv/iteration-1/`).

"Skip the eval viewer" suppresses skill-creator's built-in browser-based
review tool (`eval-viewer/generate_review.py`), which is designed for
interactive human feedback and has no use in CI or scripted runs.

### Baseline strategy

Baselines are git-based. The `main` branch serves as the reference — no
manual snapshots are needed. This works naturally with feature branches:
edit `SKILL.md` on a branch, and evals automatically compare the branch
version against the committed `main` version.

Committed baselines in `baselines/<commit-hash>/` preserve grading results
for historical comparison. The commit hash identifies which version of the
skill produced the baseline.

### When to run evals

- Before committing changes to any `SKILL.md` under `skills/plan-feature/`.
- After incorporating feedback from real-world usage into the skill.
- When refactoring shared resources (e.g., `task-description-template.md`)
  that plan-feature depends on.

## Reading benchmark.json

`benchmark.json` summarizes pass rates, timing, and token usage across all
test cases for both configurations:

```json
{
  "run_summary": {
    "pr-branch": {
      "pass_rate": { "mean": 1.0, "stddev": 0.0 },
      "time_seconds": { "mean": 191.62, "stddev": 47.5 },
      "tokens": { "mean": 41571, "stddev": 4316 }
    },
    "base-branch": {
      "pass_rate": { "mean": 1.0, "stddev": 0.0 },
      "time_seconds": { "mean": 187.23, "stddev": 49.66 },
      "tokens": { "mean": 40178, "stddev": 3191 }
    },
    "delta": {
      "pass_rate": 0.0,
      "time_seconds": 4.39,
      "tokens": 1393
    }
  }
}
```

| Field | What to look for |
|-------|-----------------|
| `pass_rate.mean` | 1.0 = all assertions passed. Below 1.0 = regressions. |
| `delta.pass_rate` | Positive = branch improved. Negative = branch regressed. Zero = parity. |
| `time_seconds` | Large increases may indicate the skill is doing unnecessary work. |
| `tokens` | Token usage proxy for cost. Compare across iterations. |

Each eval also produces individual results:

- `grading.json` — per-assertion pass/fail with evidence text
- `timing.json` — duration, token count, and tool use count for the run

## Adding new test cases

1. **Create fixture files** in `files/` for any new mock data the test case
   needs (feature description, repo manifest, etc.). Follow the annotation
   header convention from `CONVENTIONS.md`.

2. **Add an entry** to the `evals` array in `evals.json`:

   ```json
   {
     "id": 5,
     "prompt": "Plan the implementation for feature TC-9005...",
     "expected_output": "Description of what good output looks like.",
     "files": ["files/feature-new-scenario.md", "files/repo-backend.md"],
     "assertions": [
       "Assertion 1 — what the grader should check",
       "Assertion 2 — another check"
     ]
   }
   ```

3. **Run the eval** to verify the test case works and produces meaningful
   grading results.

### Writing good assertions

- **Prefer structural assertions** (section presence, task count, path
  validity) over semantic ones — they are more reliable.
- **Use semantic assertions** only for qualities that can't be checked
  mechanically (e.g., "flags ambiguous requirements").
- Assertions are graded by an LLM judge, so write them as clear,
  unambiguous natural language statements.

### When to add test cases

- When real-world usage reveals a failure mode not covered by existing tests.
- When adding new capabilities to the skill.

### When to remove assertions

- When an assertion always passes in both configurations across multiple
  iterations — it no longer measures skill value.

## Iteration workflow

The eval framework supports an iterative improvement cycle:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Run evals  │────▶│    Grade    │────▶│   Review    │────▶│   Improve   │
│             │     │             │     │  (human)    │     │  SKILL.md   │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
       ▲                                                           │
       └───────────────────────────────────────────────────────────┘
```

### 1. Run

Invoke skill-creator to run all test cases against both configurations
(base-branch and pr-branch).

### 2. Grade

skill-creator grades each run against the assertions in `evals.json` and
produces `grading.json` per eval and `benchmark.json` for the overall
summary.

### 3. Review

Review the actual outputs and record specific, actionable feedback in
`feedback.json`:

```json
{
  "eval-1": "",
  "eval-2": "Plan treated vague criteria as precise — generated specific file paths not in the mock repo.",
  "eval-3": ""
}
```

Empty string means the output passed review. Non-empty string is a specific
complaint to address in the next iteration.

### 4. Improve

Feed skill-creator the three signals:
- Failed assertions from `grading.json`
- Human feedback from `feedback.json`
- Execution transcripts from the workspace

skill-creator proposes `SKILL.md` changes. Review and apply them.

### 5. Repeat

Re-run evals. Compare `benchmark.json` against the previous iteration.
Stop when:
- `feedback.json` entries are consistently empty
- `pass_rate` delta plateaus (no further improvement)

### Committing baselines

After a successful iteration, commit the baseline results to
`baselines/<commit-hash>/` where `<commit-hash>` is the short hash of the
skill commit that produced the results. This preserves the grading history
for future comparison.

## Adapting for other skills

To add evals for a different skill, create the following at the repo root:

```
evals/<skill-name>/
├── evals.json             # Test case definitions (see schema above)
└── files/                 # Fixture files simulating external tool responses
    └── ...
```

The `baselines/` directory is created after the first successful run.

In the commands from [Running evals](#running-evals), substitute:

| Placeholder | Example (plan-feature) | Replace with |
|-------------|----------------------|--------------|
| `/plan-feature` | `/plan-feature` | `/<your-skill-name>` |
| `@evals/plan-feature/evals.json` | `@evals/plan-feature/evals.json` | `@evals/<your-skill-name>/evals.json` |
| `plan-feature-eval` (workspace prefix) | `plan-feature-eval` | `<your-skill-name>-eval` |
| `Run all 4 eval cases` | `Run all 4 eval cases` | `Run all N eval cases` (match your evals.json) |

Write fixture files appropriate to your skill's input sources — each skill
mocks different external tools. Start without assertions: run once, inspect
the outputs, then add assertions based on what you observe.
