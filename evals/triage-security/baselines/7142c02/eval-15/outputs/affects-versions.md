# Step 3 -- Affects Versions Correction: TC-8001

## Current vs Corrected Affects Versions

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Corrected (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).

The current Affects Versions "RHTPA 2.0.0" is incorrect:
- There is no 2.0.x version stream in the Security Configuration
- Lock file analysis shows quinn-proto < 0.11.14 is present in versions 2.2.0, 2.2.1, and 2.2.2
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected

## Proposed Jira Comment (ADF format)

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions corrected",
          "marks": [{"type": "strong"}]
        },
        {
          "type": "text",
          "text": " based on lock file analysis of quinn-proto versions across the 2.2.x stream."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Previous: ",
          "marks": [{"type": "strong"}]
        },
        {
          "type": "text",
          "text": "RHTPA 2.0.0"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Corrected: ",
          "marks": [{"type": "strong"}]
        },
        {
          "type": "text",
          "text": "RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Evidence: quinn-proto versions from Cargo.lock at pinned source commits:"
        }
      ]
    },
    {
      "type": "table",
      "attrs": {"isNumberColumnEnabled": false, "layout": "default"},
      "content": [
        {
          "type": "tableRow",
          "content": [
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Version"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "quinn-proto"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Affected?"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.0"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.9"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.1"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.12"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.2 (retag of 2.2.1)"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "--"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.3"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.14"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "NO"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.4"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.14"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "NO"}]}]}
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "RHTPA 2.0.0 does not correspond to any configured version stream. The 2.2.x stream versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are affected. Versions 2.2.3+ ship the fixed version 0.11.14."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "cc "
        },
        {
          "type": "mention",
          "attrs": {
            "id": "557058:prodsec-mock-account-id",
            "text": "@ProdSec"
          }
        }
      ]
    },
    {
      "type": "rule"
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This comment was AI-generated by "
        },
        {
          "type": "text",
          "text": "sdlc-workflow/triage-security",
          "marks": [
            {
              "type": "link",
              "attrs": {
                "href": "https://github.com/mrizzi/sdlc-plugins"
              }
            }
          ]
        },
        {
          "type": "text",
          "text": " v0.11.0."
        }
      ]
    }
  ]
}
```

## Jira Field Update

Remove `RHTPA 2.0.0` and set Affects Versions to: `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`.

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`.
