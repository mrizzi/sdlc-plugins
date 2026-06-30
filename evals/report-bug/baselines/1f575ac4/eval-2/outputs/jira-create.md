## Jira Create Issue Call

**Tool:** `mcp__jira__create_issue`

**Parameters:**

- **project_key:** `TC`
- **issue_type_id:** `10300`
- **summary:** `Search results pagination returns duplicate entries`
- **description:**

```
### **Issue Description**

When paginating through search results on the SBOM list page, some
entries appear on both the current and next page. This happens
consistently when sorting by creation date descending. Approximately
10-15% of entries are duplicated across page boundaries.

### **Steps to Reproduce**

1. Ingest at least 50 SBOMs into the system
2. Navigate to the SBOM list page
3. Set sort order to "Created Date (Newest First)"
4. Scroll through pages using the pagination controls
5. Compare entries on page 2 with entries on page 1

### **Expected Result**

Each SBOM appears exactly once across all pages. No duplicates when
paginating through the full result set.

### **Actual Result**

Several SBOMs that appeared at the bottom of page 1 also appear at
the top of page 2. The total count shown in the pagination footer
is correct, but the actual displayed items exceed this count due to
duplicates.

### **Attachments**

None — the issue is reproducible with any dataset of 50+ SBOMs.
```

- **labels:** `["ai-generated-jira"]`
