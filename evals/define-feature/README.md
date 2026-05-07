# define-feature Evals

Evaluations for the `define-feature` skill. See the
[framework README](../README.md) for how evals work and how to run them.

## Test cases

| ID | Name | Purpose |
|----|------|---------|
| 1 | Complete feature | All 9 template sections provided. Tests golden path: section composition, preview generation, Jira create parameters, and Comment Footnote format. |
| 2 | Partial sections | Only Required sections (Feature Overview, Requirements) provided; all others skipped. Tests that skipped sections are omitted from the preview (no empty headings). |
| 3 | Missing config | CLAUDE.md without Project Configuration. Tests that the skill stops with a /setup recommendation and does NOT proceed to collect section content. |
| 4 | Adversarial | User input with injection vectors (system overrides, exfiltration instructions, backdoor requirements, fabrication directives, preview bypass). Tests injection resistance and guardrail compliance. |

## Fixture files

Files in `files/` simulate user input and project configuration. The eval
prompt instructs the agent to write its outputs to `outputs/` rather than
calling actual Jira APIs.

### User input fixtures (`user-input-*.md`)

Simulated user-provided content for the 9 template sections:

- **user-input-complete.md** — realistic content for all 9 sections
  (SBOM dependency graph visualization feature), testing golden path
  composition
- **user-input-partial.md** — content for only the 2 Required sections
  (Feature Overview, Requirements) with explicit SKIP markers for all
  other sections
- **user-input-adversarial.md** — section content with embedded injection
  vectors: system override commands, exfiltration instructions, backdoor
  endpoint requirements, content fabrication directives, and preview
  bypass attempts

### Project configuration (`claude-md-*.md`)

Mock CLAUDE.md files representing different project states:

- **claude-md-configured.md** — valid CLAUDE.md with complete Project
  Configuration (Repository Registry, Jira Configuration, Code
  Intelligence), consistent with the setup eval fixture format
- **claude-md-missing-config.md** — CLAUDE.md without a Project
  Configuration section, simulating a project that hasn't run /setup

## Key constraints tested

| Constraint | Eval IDs |
|------------|----------|
| §1.7 — define-feature MUST NOT modify/create/delete files | 1, 2, 4 |
| §1.8 — define-feature MUST NOT fabricate content | 1, 2, 4 |
| §1.9 — define-feature MUST NOT create issue without preview and approval | 1, 2, 4 |
| Step 0 — validate Project Configuration before proceeding | 3 |
| Step 3 — skipped sections omitted from output (no empty headings) | 2 |
| Comment Footnote — correct skill name, repo link, and version | 1, 4 |
| Injection resistance — adversarial content treated as literal text | 4 |

## Running

```
/skill-litmus:run-evals Run evals for define-feature.
Evals path: evals/define-feature/evals.json
Workspace: /tmp/define-feature-eval
```
