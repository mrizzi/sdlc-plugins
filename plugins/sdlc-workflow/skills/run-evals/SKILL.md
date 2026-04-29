---
name: run-evals
description: Run skill evals with deterministic output layout and CI-compatible results. Grades assertions, aggregates benchmark.json, and renders summary.md via Python scripts. NOT skill-creator — this skill produces fixed output paths for automated pipelines. Triggers on "run evals", "eval <skill-name>", "benchmark", or "grade evals".
---

# Run Evals

Run eval cases for a skill, grade each against assertions, and produce
structured results in a deterministic directory layout.

## Inputs

The user provides:
- **Skill name** — the slash-command name of the skill to test (e.g., `plan-feature`)
- **Evals path** — path to the `evals.json` file (e.g., `evals/plan-feature/evals.json`)
- **Workspace** — directory where results are written

## Output Structure

Every run produces this exact layout — no variation:

```
<workspace>/
├── benchmark.json
├── feedback.json
├── summary.md
├── eval-1/
│   ├── grading.json
│   ├── timing.json
│   └── outputs/
│       └── (skill outputs)
├── eval-2/
│   └── ...
└── eval-N/
    └── ...
```

## Process

### Step 1 — Read evals.json

Read the evals file and extract:
- `skill_name` — the skill being evaluated
- `evals[]` — array of test cases, each with `id`, `prompt`, `expected_output`,
  `files` (optional), and `assertions`

### Step 2 — Execute each eval case

For each eval in `evals[]`, spawn a subagent with this prompt:

```
You are executing an eval for the /sdlc-workflow:<skill-name> skill.

Task: <eval.prompt>

<if eval.files>
Input files (read these before starting):
<for each file in eval.files>
- <evals_dir>/<file>
</for>
</if>

Write all outputs to: <workspace>/eval-<eval.id>/outputs/

Important:
- Invoke the /sdlc-workflow:<skill-name> skill via the Skill tool to process this task
- Write every output file to the outputs/ directory
- Do not interact with external services (Jira, Figma, etc.) — write to files instead
```

**Parallelism:** Spawn all eval subagents in a single turn so they run
concurrently. Do not wait for one eval to complete before starting the
next — the eval cases are independent.

When each subagent completes, capture `total_tokens` and `duration_ms`
from the task completion notification immediately. Write to
`<workspace>/eval-<eval.id>/timing.json`:

```json
{
  "total_tokens": <value>,
  "duration_ms": <value>
}
```

### Step 3 — Grade each eval case

As each eval completes, spawn a grader subagent. Grading can overlap
with execution — grade each eval as it finishes rather than waiting for
all to complete.

Grader prompt:

```
Grade the outputs of an eval run against these assertions.

Assertions:
<for each assertion in eval.assertions>
- <assertion>
</for>

Outputs directory: <workspace>/eval-<eval.id>/outputs/

## Grading rules

1. Read every file in the outputs directory. Open and read file
   contents — do not judge based on filenames alone.
2. Burden of proof is on PASS. Default to FAIL. Only mark PASS when
   you find specific, concrete evidence in the output files that
   satisfies the assertion.
3. No partial credit. Each assertion is binary: PASS or FAIL.
   "Mostly correct" or "partially addressed" is FAIL.
4. Cite specific evidence. The evidence field must quote or reference
   exact content from output files — file paths, line excerpts, counts.
   Never write vague evidence like "the output generally addresses this."
5. Check structure AND content. Verify both that expected sections/files
   exist AND that their content satisfies the assertion.
6. Contradictory evidence means FAIL. If some outputs support the
   assertion but others contradict it, the assertion fails.

Write results to: <workspace>/eval-<eval.id>/grading.json

Use this exact JSON structure:
{
  "assertion_results": [
    {
      "text": "<assertion text>",
      "passed": true/false,
      "evidence": "<specific evidence from output files>"
    }
  ],
  "summary": {
    "passed": <count>,
    "failed": <count>,
    "total": <count>,
    "pass_rate": <0.0 to 1.0>
  }
}
```

### Step 4 — Aggregate into benchmark.json

After all evals are graded, run the aggregation script:

```bash
python3 <skill-dir>/scripts/aggregate_benchmark.py --results <workspace>
```

The script reads all `eval-N/grading.json` and `eval-N/timing.json`
files, computes mean and stddev for pass rate, duration, and token usage,
and writes `<workspace>/benchmark.json`.

### Step 5 — Create feedback.json placeholder

Write `<workspace>/feedback.json` with empty strings for each eval:

```json
{
  "eval-1": "",
  "eval-2": "",
  ...
}
```

### Step 6 — Render summary

Determine the baseline path: `evals/<skill-name>/baselines/latest/`.

Run the render script, passing the skill name so the heading identifies
which skill the results belong to:

```bash
python3 <skill-dir>/scripts/render_summary.py \
  --results <workspace> \
  --baseline <baseline-path> \
  --skill <skill-name>
```

If the baseline path does not exist, omit `--baseline` — the script
renders results without a comparison.

The script writes `<workspace>/summary.md`. Display its contents to the
user.

## Rules

- Write all outputs to the exact paths specified. No intermediate directories,
  no configuration-named subdirectories.
- Every eval case gets its own `eval-<id>/` directory using the `id` from evals.json.
- `grading.json` uses `assertion_results` (not `expectations`) with fields
  `text`, `passed`, `evidence`.
- Timing data must be captured from the task completion notification — it cannot
  be recovered after the fact.
- Do not launch an eval viewer or browser.
- Do not run baseline comparisons — only run the current skill version.
  Baseline comparison is handled by the render script in Step 6.
- `<skill-dir>` is the directory containing this SKILL.md — resolve it from
  the absolute path shown in the skill invocation header.
