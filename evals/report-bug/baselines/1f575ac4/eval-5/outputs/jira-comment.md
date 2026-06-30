# Jira Comment: Bug Creation Metadata

## API Call: Add Comment

**Endpoint**: `POST /rest/api/3/issue/{issueKey}/comment`

**Request Body**:

```json
{
  "body": {
    "version": 1,
    "type": "doc",
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "This bug was reported using the "
          },
          {
            "type": "text",
            "text": "sdlc-workflow/report-bug",
            "marks": [{ "type": "code" }]
          },
          {
            "type": "text",
            "text": " skill (v0.11.0) from "
          },
          {
            "type": "text",
            "text": "https://github.com/mrizzi/sdlc-plugins",
            "marks": [{ "type": "link", "attrs": { "href": "https://github.com/mrizzi/sdlc-plugins" } }]
          },
          {
            "type": "text",
            "text": "."
          }
        ]
      }
    ]
  }
}
```
