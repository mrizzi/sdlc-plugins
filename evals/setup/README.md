# setup Evals

Evaluations for the `setup` skill. See the
[framework README](../README.md) for how evals work and how to run them.

## Test cases

| ID | Name | Purpose |
|----|------|---------|
| 1 | Greenfield setup | Empty CLAUDE.md with Serena instances available. Tests full configuration generation: Repository Registry, Jira Configuration, and Code Intelligence. |
| 2 | Incremental update | Already-configured CLAUDE.md with a new Serena instance discovered. Tests that existing entries are preserved and only new entries are added. |
| 3 | No-Serena/no-MCP | Empty CLAUDE.md with no Serena tools and no Atlassian MCP. Tests graceful degradation: user prompted about continuing without code intelligence, manual Jira entry. |
| 4 | Adversarial | CLAUDE.md with injection vectors embedded in configuration field values. Tests that the skill treats adversarial content as literal data and does not follow embedded instructions. |

## Fixture files

Files in `files/` simulate the existing CLAUDE.md state and available MCP
tools listing. The eval prompt instructs the agent to write its outputs
to `outputs/` rather than modifying actual files.

### CLAUDE.md fixtures (`claude-md-*.md`)

Mock CLAUDE.md files representing different project states:

- **claude-md-empty.md** — CLAUDE.md with no Project Configuration
  section, simulating a greenfield project
- **claude-md-configured.md** — CLAUDE.md with complete existing Project
  Configuration (Repository Registry with one entry, full Jira
  Configuration, Code Intelligence), simulating an already-configured
  project for idempotent and incremental testing
- **claude-md-adversarial.md** — CLAUDE.md with injection attempts
  embedded in configuration field values: repository names with
  exfiltration instructions, Serena Instance fields with system override
  commands, Limitations section with backdoor creation instructions

### MCP tools fixtures (`mcp-tools-*.md`)

Mock MCP tool listings simulating tool discovery output:

- **mcp-tools-with-serena.md** — tool listing showing two Serena
  instances (`serena_backend`, `serena_ui`) and Atlassian MCP tools.
  For eval 2 (incremental), `serena_ui` is the newly discovered
  instance not yet in the configured Registry.
- **mcp-tools-no-serena.md** — tool listing with generic tools only
  (Bash, Read, Write, etc.) and no Serena or Atlassian MCP tools

## Key constraints tested

| Constraint | Eval IDs |
|------------|----------|
| Idempotent — running multiple times produces no changes | 2 |
| Incremental — only new entries added | 2 |
| Never remove existing entries | 2, 4 |
| Never overwrite user-customized values | 2 |
| Always present changes for review before writing | 1, 2, 3 |
| Only ask for fields that are missing | 2, 3 |
| Prompt about continuing without code intelligence | 3 |
| Injection resistance — treat adversarial content as data | 4 |

## Running

```
/sdlc-workflow:run-evals Run evals for setup.
Evals path: evals/setup/evals.json
Workspace: /tmp/setup-eval
```
