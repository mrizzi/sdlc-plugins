---
name: run-evals
description: Run skill evals and produce structured grading results. Use when the user wants to run evals for a skill, grade assertions, and produce benchmark.json. Triggers on "run evals", "eval plan-feature", "grade evals", or similar.
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
You are executing an eval for the /<skill-name> skill.

Task: <eval.prompt>

<if eval.files>
Input files (read these before starting):
<for each file in eval.files>
- <evals_dir>/<file>
</for>
</if>

Write all outputs to: <workspace>/eval-<eval.id>/outputs/

Important:
- Invoke the /<skill-name> skill via the Skill tool to process this task
- Write every output file to the outputs/ directory
- Do not interact with external services (Jira, Figma, etc.) — write to files instead
```

When the subagent completes, capture `total_tokens` and `duration_ms` from
the task completion notification. Write immediately to
`<workspace>/eval-<eval.id>/timing.json`:

```json
{
  "total_tokens": <value>,
  "duration_ms": <value>
}
```

### Step 3 — Grade each eval case

After each eval completes, spawn a grader subagent with this prompt:

```
Grade the outputs of an eval run against these assertions.

Assertions:
<for each assertion in eval.assertions>
- <assertion>
</for>

Outputs directory: <workspace>/eval-<eval.id>/outputs/

For each assertion:
1. Search the output files for evidence
2. PASS if clear evidence supports the assertion
3. FAIL if no evidence, or evidence contradicts
4. Cite specific evidence for every verdict

Write results to: <workspace>/eval-<eval.id>/grading.json

Use this exact JSON structure:
{
  "assertion_results": [
    {
      "text": "<assertion text>",
      "passed": true/false,
      "evidence": "<specific evidence>"
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

After all evals are graded, read every `eval-N/grading.json` and
`eval-N/timing.json` and produce `<workspace>/benchmark.json`:

```json
{
  "run_summary": {
    "pass_rate": {
      "mean": <mean across evals>,
      "stddev": <stddev across evals>
    },
    "time_seconds": {
      "mean": <mean duration_ms / 1000>,
      "stddev": <stddev>
    },
    "tokens": {
      "mean": <mean total_tokens>,
      "stddev": <stddev>
    }
  }
}
```

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

Run the render script from the skill's scripts/ directory:

```bash
python3 <skill-dir>/scripts/render_summary.py \
  --results <workspace> \
  --baseline <baseline-path>
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
