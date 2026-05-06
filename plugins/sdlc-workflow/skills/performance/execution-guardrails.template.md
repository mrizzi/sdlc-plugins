# Execution Guardrails Template

Shared execution integrity instructions for all performance skills.
Each skill references this file and adds its own inline skill-specific sections.

---

### Execution Order — MANDATORY

**Every step in this skill MUST be executed in the exact sequence defined in this document.
No step may be reordered, merged with another step, or silently omitted.**

- Steps are numbered to enforce a strict linear order.
- Sub-steps must be completed in their defined sub-order before the parent step is
  considered done.
- Conditional paths are the **only permitted deviations** from sequential order, and they
  are explicitly stated in the step text. Any step not applicable to the current execution
  path must still be **acknowledged** with a brief output note before moving on.

### Step-Skip Policy

- A step may be **conditionally skipped** only when the step itself contains an explicit
  conditional instruction (e.g., "This step runs ONLY if …", "skip if … = true").
- When a step is skipped due to a condition, output **must** include:
  `⏭ Step X skipped — <reason>` before proceeding to the next step.
- A step may **never** be skipped to save time, reduce verbosity, or because the result
  seems obvious.

**Never proceed silently.** If a step produces no data (e.g., no routes found), output must
explicitly state that fact rather than moving on without comment.

### Blocking Steps — CANNOT BE BYPASSED

Steps that require user confirmation or user input are **hard blocking**. The skill must
pause and wait for explicit user response before executing the next step. These steps may
not be auto-answered, assumed, or skipped. Skill-specific blocking steps are listed below.

> Note: Blocking step instructions are enforced in interactive sessions. Unattended
> pipeline runs do not have a mechanical enforcement mechanism.

### Completeness Enforcement

- All outputs defined for a step (tables, summaries, file writes, console messages) must
  be produced **in full** before the step is marked complete.
- Partial output (e.g., truncating a table, showing a subset of discovered endpoints) is
  not permitted.
- If a step's output would exceed reasonable length, summarise with counts and highlight
  key items — but the full artifact (file) must still be written completely.

### Error Handling

- If any mandatory step fails (e.g., config missing, report missing, script error), the
  skill must halt at that step, output a clear error message with the step number, and
  provide actionable remediation instructions. It must not silently skip to a later step.

### Step Execution Format

- **Always announce each step** before executing it using the format: `▶ Step X – <name>`
- **Always confirm step completion** after executing it with a brief summary of what was
  produced and what step comes next, using the format: `✓ Step X complete — <summary>`

### In-Context Processing Rule

Shell and MCP tools are for **reading source code only** (grep, find_symbol, Read, Glob).

**All collection, counting, grouping, and validation MUST be performed in-context:**
- Output discovered items (endpoints, routes, modules) as a **markdown table in your response**
- Count by counting rows in that table — do NOT run `wc -l` or `echo ${#array[@]}`
- Group by reasoning over the table — do NOT write grouping logic to a shell script
- Validate by comparing table totals — do NOT write results to `/tmp` or any file

**Never write intermediate results to `/tmp`, shell arrays, or temporary files.**
Shell is a read-only tool in this skill. Any shell command that writes or counts is a violation.

