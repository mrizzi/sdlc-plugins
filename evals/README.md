# Skill Evaluation Framework

Structured evaluations for sdlc-workflow skills. Each skill's evals live
in `evals/<skill-name>/` with test cases, fixture files, and committed
baselines.

For architectural decisions and known limitations, see the
[design spec](../docs/specs/2026-04-16-skill-eval-framework-design.md).

## Why a custom eval skill

Anthropic's `skill-creator` includes eval capabilities, but it is designed
for interactive skill development — running both with-skill and
without-skill configurations, launching a browser-based eval viewer, and
iterating through improvement cycles with human review.

CI evaluation has different requirements: deterministic output paths,
single-configuration runs, no browser, and a summary that can be posted
as a PR comment or displayed in a terminal. Rather than fighting
skill-creator's interactive assumptions, `run-evals`
(`/sdlc-workflow:run-evals`) is a purpose-built skill that:

- Produces results in a fixed directory layout — no variation between runs
- Runs only the current skill version (baselines are stored separately)
- Grades assertions and aggregates metrics into `benchmark.json`
- Renders a Markdown summary via `render_summary.py`, comparing against
  stored baselines when available
- Works identically in interactive and headless (`claude -p`) modes

## Directory structure

```
evals/
├── README.md                  # This file
├── <skill-name>/
│   ├── evals.json             # Test case definitions and assertions
│   ├── README.md              # Skill-specific eval documentation
│   ├── files/                 # Input fixtures (mock data for eval prompts)
│   │   └── ...
│   └── baselines/             # Committed baseline results
│       ├── latest -> <hash>/  # Symlink to most recent baseline
│       └── <commit-hash>/
│           ├── benchmark.json
│           ├── feedback.json
│           ├── eval-1/
│           │   ├── grading.json
│           │   ├── timing.json
│           │   └── outputs/
│           ├── eval-2/
│           │   └── ...
│           └── ...
└── ...
```

## evals.json schema

Each skill defines its test cases in `evals.json`:

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
        "Each task file contains all required template sections",
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
| `evals[].files` | string[] | Paths to fixture files (relative to the evals.json directory) |
| `evals[].assertions` | string[] | Assertions graded by the LLM judge after each run |

## Running evals locally

Start a Claude Code session in the repo root and invoke the `run-evals`
skill:

```
/sdlc-workflow:run-evals Run evals for plan-feature.
Evals path: evals/plan-feature/evals.json
Workspace: /tmp/plan-feature-eval
```

The skill:
1. Reads `evals.json` and spawns a subagent per test case
2. Grades each run's outputs against the assertions
3. Aggregates results into `benchmark.json`
4. Compares against the stored baseline at `evals/plan-feature/baselines/latest/`
5. Renders `summary.md` and displays it

### Output structure

Every run produces this exact layout:

```
<workspace>/
├── benchmark.json       # Aggregate metrics (pass rate, tokens, duration)
├── feedback.json        # Human review placeholder (empty strings)
├── summary.md           # Rendered Markdown with results and baseline delta
├── eval-1/
│   ├── grading.json     # Per-assertion pass/fail with evidence
│   ├── timing.json      # Tokens and duration for the run
│   └── outputs/         # Raw skill outputs
├── eval-2/
│   └── ...
└── ...
```

### benchmark.json schema

```json
{
  "run_summary": {
    "pass_rate": { "mean": 1.0, "stddev": 0.0 },
    "time_seconds": { "mean": 191.62, "stddev": 47.5 },
    "tokens": { "mean": 41571, "stddev": 4316 }
  }
}
```

| Field | What to look for |
|-------|-----------------|
| `pass_rate.mean` | 1.0 = all assertions passed. Below 1.0 = regressions. |
| `time_seconds` | Large increases may indicate the skill is doing unnecessary work. |
| `tokens` | Token usage proxy for cost. Compare across runs. |

## CI workflows

Two GitHub Actions workflows automate eval execution. Neither gates
merges — they report results only.

### eval-pr.yml (pull request)

Triggers when a PR modifies `plugins/sdlc-workflow/skills/**/*.md` or
`evals/**/evals.json`.

1. **Discover changed skills** — `git diff` maps changed files to eval suites
2. **Run evals** — invokes `run-evals` via `claude -p` for each changed skill
3. **Post PR comment** — reads `summary.md` from the workspace and posts it

The skill's `render_summary.py` script handles baseline comparison. If
`evals/<skill>/baselines/latest/` exists, the summary includes a delta
line. If not, it shows raw results only.

### eval-baseline.yml (push to main)

Triggers when skill or eval files are merged to main.

1. **Discover all eval suites** — runs all skills, not just changed ones
2. **Run evals** — invokes `run-evals` via `claude -p` for each skill
3. **Store baselines** — commits results to `evals/<skill>/baselines/<hash>/`
4. **Update `latest` symlink** — points to the new baseline

This ensures every merge to main has a complete baseline that subsequent
PRs can compare against.

## Baseline strategy

Baselines are committed to `evals/<skill>/baselines/<commit-hash>/` and
the `latest` symlink always points to the most recent one. PRs resolve
the baseline via the symlink — they don't need to know the exact commit
hash.

If main receives commits that don't touch skill or eval files, the
`eval-baseline` workflow doesn't trigger, but `latest` still points to
the most recent valid baseline.

## Adding evals for a new skill

1. Create the directory structure:

   ```
   evals/<skill-name>/
   ├── evals.json
   ├── README.md        # Skill-specific documentation
   └── files/           # Fixture files
       └── ...
   ```

2. Define test cases in `evals.json` (see schema above).

3. Create fixture files in `files/` that simulate what external tools
   would return. Each skill mocks different inputs — see existing skills
   for examples.

4. Run the evals locally to verify they work.

5. The `baselines/` directory is created after the first successful run
   on main.

## Fixture file conventions

Fixture files simulate external tool responses so evals run without
network dependencies:

- **Adversarial fixtures**: include `<!-- ADVERSARIAL TEST FIXTURE — <purpose> -->`
- **Synthetic data fixtures**: include `<!-- SYNTHETIC TEST DATA — <purpose> -->`

## Iteration workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Run evals  │────▶│    Grade    │────▶│   Review    │────▶│   Improve   │
│             │     │             │     │  (human)    │     │  SKILL.md   │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
       ▲                                                           │
       └───────────────────────────────────────────────────────────┘
```

1. **Run** — invoke `/sdlc-workflow:run-evals`
2. **Grade** — the skill grades assertions and produces `grading.json`
3. **Review** — inspect outputs and record feedback in `feedback.json`
4. **Improve** — edit the skill's `SKILL.md` based on failures and feedback
5. **Repeat** — re-run evals, compare against baseline, stop when pass
   rate plateaus

### Committing baselines

After a successful iteration, commit results to
`baselines/<commit-hash>/` and update the `latest` symlink. The commit
hash identifies which version of the skill produced the baseline.
