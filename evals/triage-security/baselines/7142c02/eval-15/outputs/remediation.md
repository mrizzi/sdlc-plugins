# Step 7 -- Post-Triage Summary: TC-8001

## Triage Outcome

**Case A + Case B**: The 2.2.x stream (scoped stream) has affected versions (2.2.0, 2.2.1, 2.2.2). Cross-stream impact detected: the 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9).

### Actions Taken

1. **Affects Versions corrected**: removed RHTPA 2.0.0, set to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. **Remediation tasks created** for 2.2.x stream (source dependency -- Cargo ecosystem):
   - Upstream backport task: bump quinn-proto to >= 0.11.14 on branch `release/0.4.z` in rhtpa-backend
   - Downstream propagation subtask: update rhtpa-backend reference in rhtpa-release.0.4.z
3. **Cross-stream impact comment**: 2.1.x stream also affected (quinn-proto 0.11.9 in versions 2.1.0, 2.1.1)
4. **Preemptive remediation tasks created** for 2.1.x stream (no CVE Jira exists for that stream):
   - Upstream backport task: bump quinn-proto to >= 0.11.14 on branch `release/0.3.z` in rhtpa-backend (label: security-preemptive)
   - Downstream propagation subtask: update rhtpa-backend reference in rhtpa-release.0.3.z (label: security-preemptive)
5. **Label added**: `ai-cve-triaged`

## Post-Triage Summary Comment (ADF format)

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "heading",
      "attrs": {"level": 3},
      "content": [
        {
          "type": "text",
          "text": "Triage Summary -- CVE-2026-31812"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "CVE-2026-31812: quinn-proto panic on large stream counts (DoS). CVSS 7.5 (High). Fixed in quinn-proto 0.11.14."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 4},
      "content": [
        {
          "type": "text",
          "text": "Version Impact"
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
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Stream"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "quinn-proto"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Affected?"}]}]},
            {"type": "tableHeader", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Notes"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.1.0"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.1.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.9"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": ""}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.1.1"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.1.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.9"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": ""}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.0"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.9"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": ""}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.1"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.12"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": ""}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.2"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "--"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "YES"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "retag of 2.2.1"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.3"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.14"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "NO"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "fixed version"}]}]}
          ]
        },
        {
          "type": "tableRow",
          "content": [
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.4"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "2.2.x"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "0.11.14"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "NO"}]}]},
            {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "fixed version"}]}]}
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 4},
      "content": [
        {
          "type": "text",
          "text": "Affects Versions Correction"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Corrected from RHTPA 2.0.0 to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 based on lock file evidence."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 4},
      "content": [
        {
          "type": "text",
          "text": "Triage Outcome"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affected",
          "marks": [{"type": "strong"}]
        },
        {
          "type": "text",
          "text": " -- remediation tasks created for the scoped 2.2.x stream. Cross-stream impact detected on 2.1.x."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 4},
      "content": [
        {
          "type": "text",
          "text": "Remediation Tasks (2.2.x stream)"
        }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Upstream backport: ",
                  "marks": [{"type": "strong"}]
                },
                {
                  "type": "text",
                  "text": "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x) -- bump quinn-proto to >= 0.11.14 on branch release/0.4.z in rhtpa-backend"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Downstream propagation: ",
                  "marks": [{"type": "strong"}]
                },
                {
                  "type": "text",
                  "text": "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x) -- blocked by upstream task"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 4},
      "content": [
        {
          "type": "text",
          "text": "Cross-Stream Impact"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (versions 2.1.0, 2.1.1 ship quinn-proto 0.11.9). Preemptive remediation tasks created for the 2.1.x stream with label security-preemptive and Related link type."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": {"level": 4},
      "content": [
        {
          "type": "text",
          "text": "Preemptive Remediation Tasks (2.1.x stream)"
        }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Upstream backport (preemptive): ",
                  "marks": [{"type": "strong"}]
                },
                {
                  "type": "text",
                  "text": "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x) -- bump on branch release/0.3.z in rhtpa-backend (security-preemptive)"
                }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "Downstream propagation (preemptive): ",
                  "marks": [{"type": "strong"}]
                },
                {
                  "type": "text",
                  "text": "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x) (security-preemptive)"
                }
              ]
            }
          ]
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
            "id": "557058:psirt-analyst-mock-id",
            "text": "@psirt-analyst"
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

## Jira Mutations Summary

1. **Affects Versions updated**: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. **Label added**: `ai-cve-triaged`
3. **Remediation tasks created** (2.2.x -- scoped stream):
   - Upstream backport task (labels: ai-generated-jira, Security, CVE-2026-31812) linked via "Depend"
   - Downstream propagation subtask (labels: ai-generated-jira, Security, CVE-2026-31812) linked via "Depend" to CVE, "Blocks" from upstream
4. **Preemptive remediation tasks created** (2.1.x -- cross-stream):
   - Upstream backport task (labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive) linked via "Related"
   - Downstream propagation subtask (labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive) linked via "Related" to CVE, "Blocks" from upstream
5. **Post-triage summary comment** posted with version impact table, Affects Versions correction, remediation task links, cross-stream impact notice, and @mention of reporter (psirt-analyst)
6. **Transition**: Vulnerability issue transitioned to In Progress
7. **Assignment**: Vulnerability issue assigned to current user
