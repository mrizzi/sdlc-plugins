# Skill Evaluation Framework

Structured evaluations for sdlc-workflow skills. Each skill's evals live
in `evals/<skill-name>/` with test cases, fixture files, and committed
baselines.

For architectural decisions and known limitations, see the
[design spec](../docs/specs/2026-04-16-skill-eval-framework-design.md).

## Why skill-litmus

Anthropic's `skill-creator` includes eval capabilities, but it is designed
for interactive skill development — running both with-skill and
without-skill configurations, launching a browser-based eval viewer, and
iterating through improvement cycles with human review.

CI evaluation has different requirements: deterministic output paths,
single-configuration runs, no browser, and a summary that can be posted
as a PR comment or displayed in a terminal.
[skill-litmus](https://github.com/mrizzi/skill-litmus) is a standalone
plugin and GitHub Action (`/skill-litmus:run-evals`) that provides a
shell-driven eval engine:

- Produces results in a fixed directory layout — no variation between runs
- Runs only the current skill version (baselines are stored separately)
- Grades assertions and aggregates metrics into `benchmark.json`
- Renders a Markdown summary comparing against stored baselines when available
- Works identically in interactive and headless (`claude -p`) modes
- Provides a reusable GitHub Action for CI integration

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
  "plugin": "sdlc-workflow",
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
| `plugin` | string | Plugin that owns the skill (e.g., `sdlc-workflow`) |
| `evals[].id` | number | Unique identifier for the test case |
| `evals[].prompt` | string | The prompt sent to the skill agent |
| `evals[].expected_output` | string | Natural language description of expected behavior |
| `evals[].files` | string[] | Paths to fixture files (relative to the evals.json directory) |
| `evals[].assertions` | string[] | Assertions graded by the LLM judge after each run |

## Running evals locally

Start a Claude Code session in the repo root and invoke the `run-evals`
skill:

```
/skill-litmus:run-evals Run evals for plan-feature.
Evals path: evals/plan-feature/evals.json
Workspace: /tmp/plan-feature-eval
```

The skill:
1. Reads `evals.json` and runs each test case via `claude -p`
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

## CI workflow

A single GitHub Actions workflow (`eval.yml`) automates eval execution
using the [`mrizzi/skill-litmus`](https://github.com/mrizzi/skill-litmus)
composite action. It does not gate merges — it reports results only.

The workflow triggers when `plugins/sdlc-workflow/skills/**/*.md` or
`evals/**/evals.json` are modified, on both pull requests and pushes to
main.

- **On pull request** — discovers changed skills, runs their evals,
  compares against stored baselines, and posts a PR review with the
  results.
- **On push to main** — runs all eval suites and commits baseline
  results to `evals/<skill>/baselines/<hash>/`, updating the `latest`
  symlink.

Both modes are handled automatically by the skill-litmus action.

## Baseline strategy

Baselines are committed to `evals/<skill>/baselines/<commit-hash>/` and
the `latest` symlink always points to the most recent one. PRs resolve
the baseline via the symlink — they don't need to know the exact commit
hash.

If main receives commits that don't touch skill or eval files, the
eval workflow doesn't trigger, but `latest` still points to
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

1. **Run** — invoke `/skill-litmus:run-evals`
2. **Grade** — the skill grades assertions and produces `grading.json`
3. **Review** — inspect outputs and record feedback in `feedback.json`
4. **Improve** — edit the skill's `SKILL.md` based on failures and feedback
5. **Repeat** — re-run evals, compare against baseline, stop when pass
   rate plateaus

### Committing baselines

After a successful iteration, commit results to
`baselines/<commit-hash>/` and update the `latest` symlink. The commit
hash identifies which version of the skill produced the baseline.
