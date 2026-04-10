#!/usr/bin/env python3
"""JIRA REST API v3 client with markdown-to-ADF conversion.

This client provides a fallback mechanism for sdlc-workflow skills when
Atlassian MCP is unavailable due to organizational policies.

Uses only Python stdlib - no external dependencies required.
"""

import json
import os
import re
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from base64 import b64encode
from typing import Dict, List, Optional, Any


def get_credentials() -> tuple[str, str, str]:
    """Read credentials from environment variables.

    Returns:
        Tuple of (server_url, email, api_token)

    Raises:
        SystemExit: If any credentials are missing
    """
    server_url = os.getenv('JIRA_SERVER_URL')
    email = os.getenv('JIRA_EMAIL')
    api_token = os.getenv('JIRA_API_TOKEN')

    if not all([server_url, email, api_token]):
        missing = []
        if not server_url:
            missing.append('JIRA_SERVER_URL')
        if not email:
            missing.append('JIRA_EMAIL')
        if not api_token:
            missing.append('JIRA_API_TOKEN')

        print(f"❌ Missing credentials: {', '.join(missing)}", file=sys.stderr)
        print("Set these environment variables before running this command.", file=sys.stderr)
        sys.exit(1)

    return server_url.rstrip('/'), email, api_token


def mask_token(token: str) -> str:
    """Mask API token for safe logging.

    Args:
        token: The API token to mask

    Returns:
        Masked token showing first 8 and last 4 characters
    """
    if len(token) <= 12:
        return "***"
    return f"{token[:8]}...{token[-4:]}"


def make_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Make authenticated JIRA API request.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint relative to /rest/api/3/
        data: Optional request body (will be JSON-encoded)

    Returns:
        Parsed JSON response

    Raises:
        SystemExit: On HTTP errors or connection failures
    """
    server_url, email, api_token = get_credentials()

    # Build request
    url = f"{server_url}/rest/api/3/{endpoint}"
    auth_string = f"{email}:{api_token}"
    auth_bytes = auth_string.encode('utf-8')
    auth_b64 = b64encode(auth_bytes).decode('ascii')

    headers = {
        'Authorization': f"Basic {auth_b64}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    request = Request(url, headers=headers, method=method)
    if data:
        request.data = json.dumps(data).encode('utf-8')

    # Execute with error handling
    try:
        with urlopen(request) as response:
            response_data = response.read().decode('utf-8')
            if response_data:
                return json.loads(response_data)
            return {}
    except HTTPError as e:
        handle_http_error(e)
        sys.exit(1)
    except URLError as e:
        print(f"❌ Connection error: {e.reason}", file=sys.stderr)
        print(f"Check that {server_url} is accessible.", file=sys.stderr)
        sys.exit(1)


def handle_http_error(error: HTTPError) -> None:
    """Map HTTP errors to user-friendly messages.

    Args:
        error: The HTTP error to handle
    """
    status = error.code

    if status == 401:
        print("❌ Authentication failed (401 Unauthorized)", file=sys.stderr)
        print("Check your email and API token. Run /setup to update credentials.", file=sys.stderr)
    elif status == 403:
        print("❌ Permission denied (403 Forbidden)", file=sys.stderr)
        print("Contact your JIRA admin to grant project access.", file=sys.stderr)
    elif status == 404:
        print("❌ Resource not found (404 Not Found)", file=sys.stderr)
        print("Verify the issue key or endpoint path.", file=sys.stderr)
    elif status == 400:
        try:
            error_body = error.read().decode('utf-8')
            error_detail = json.loads(error_body)
            messages = error_detail.get('errorMessages', [])
            errors = error_detail.get('errors', {})

            print("❌ Invalid request (400 Bad Request)", file=sys.stderr)
            if messages:
                for msg in messages:
                    print(f"  • {msg}", file=sys.stderr)
            if errors:
                for field, msg in errors.items():
                    print(f"  • {field}: {msg}", file=sys.stderr)
        except:
            print("❌ Invalid request format (400 Bad Request)", file=sys.stderr)
    else:
        print(f"❌ HTTP {status}: {error.reason}", file=sys.stderr)


def markdown_to_adf(md_text: str) -> Dict[str, Any]:
    """Convert markdown to Atlassian Document Format.

    Supports:
    - Headings (# and ##)
    - Paragraphs
    - Bullet lists (-)
    - Ordered lists (1. 2. etc.)
    - Bold (**text**)
    - Italic (*text*)
    - Inline code (`code`)
    - Code blocks (```language)
    - Links ([text](url))
    - Horizontal rules (---)

    Args:
        md_text: Markdown text to convert

    Returns:
        ADF document structure
    """
    doc = {"type": "doc", "version": 1, "content": []}

    # Split by double newlines to get blocks
    blocks = md_text.split('\n\n')

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Horizontal rule
        if re.match(r'^-{3,}$', block):
            doc["content"].append({"type": "rule"})
            continue

        # Code block
        code_block_match = re.match(r'^```(\w+)?\n(.*?)\n```$', block, re.DOTALL)
        if code_block_match:
            language = code_block_match.group(1) or 'text'
            code = code_block_match.group(2)
            doc["content"].append({
                "type": "codeBlock",
                "attrs": {"language": language},
                "content": [{"type": "text", "text": code}]
            })
            continue

        # Heading level 1
        if block.startswith('# ') and not block.startswith('## '):
            doc["content"].append({
                "type": "heading",
                "attrs": {"level": 1},
                "content": parse_inline_formatting(block[2:])
            })
            continue

        # Heading level 2
        if block.startswith('## '):
            doc["content"].append({
                "type": "heading",
                "attrs": {"level": 2},
                "content": parse_inline_formatting(block[3:])
            })
            continue

        # Bullet list
        if re.match(r'^[-*]\s', block):
            items = []
            for line in block.split('\n'):
                if re.match(r'^[-*]\s', line):
                    text = re.sub(r'^[-*]\s+', '', line)
                    items.append({
                        "type": "listItem",
                        "content": [{
                            "type": "paragraph",
                            "content": parse_inline_formatting(text)
                        }]
                    })
            doc["content"].append({"type": "bulletList", "content": items})
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', block):
            items = []
            for line in block.split('\n'):
                if re.match(r'^\d+\.\s', line):
                    text = re.sub(r'^\d+\.\s+', '', line)
                    items.append({
                        "type": "listItem",
                        "content": [{
                            "type": "paragraph",
                            "content": parse_inline_formatting(text)
                        }]
                    })
            doc["content"].append({"type": "orderedList", "content": items})
            continue

        # Regular paragraph
        doc["content"].append({
            "type": "paragraph",
            "content": parse_inline_formatting(block)
        })

    return doc


def parse_inline_formatting(text: str) -> List[Dict[str, Any]]:
    """Parse inline formatting (bold, italic, code, links) into ADF nodes.

    Args:
        text: Text with inline markdown formatting

    Returns:
        List of ADF text nodes with marks
    """
    nodes = []

    # Simple implementation: handle bold, italic, code, links
    # Pattern: **bold** or *italic* or `code` or [text](url)
    pos = 0

    while pos < len(text):
        # Try to match formatting patterns

        # Bold: **text**
        bold_match = re.match(r'\*\*(.+?)\*\*', text[pos:])
        if bold_match:
            nodes.append({
                "type": "text",
                "text": bold_match.group(1),
                "marks": [{"type": "strong"}]
            })
            pos += len(bold_match.group(0))
            continue

        # Italic: *text*
        italic_match = re.match(r'\*(.+?)\*', text[pos:])
        if italic_match:
            nodes.append({
                "type": "text",
                "text": italic_match.group(1),
                "marks": [{"type": "em"}]
            })
            pos += len(italic_match.group(0))
            continue

        # Inline code: `code`
        code_match = re.match(r'`(.+?)`', text[pos:])
        if code_match:
            nodes.append({
                "type": "text",
                "text": code_match.group(1),
                "marks": [{"type": "code"}]
            })
            pos += len(code_match.group(0))
            continue

        # Link: [text](url)
        link_match = re.match(r'\[(.+?)\]\((.+?)\)', text[pos:])
        if link_match:
            nodes.append({
                "type": "text",
                "text": link_match.group(1),
                "marks": [{"type": "link", "attrs": {"href": link_match.group(2)}}]
            })
            pos += len(link_match.group(0))
            continue

        # Plain text: accumulate until next formatting char
        plain_match = re.match(r'[^\*`\[]+', text[pos:])
        if plain_match:
            nodes.append({
                "type": "text",
                "text": plain_match.group(0)
            })
            pos += len(plain_match.group(0))
            continue

        # Single character that didn't match (edge case)
        nodes.append({"type": "text", "text": text[pos]})
        pos += 1

    return nodes if nodes else [{"type": "text", "text": text}]


# =============================================================================
# JIRA API Operations
# =============================================================================

def get_issue(issue_key: str, fields: str = "*all") -> Dict[str, Any]:
    """Get JIRA issue by key.

    Args:
        issue_key: Issue key (e.g., TC-123)
        fields: Comma-separated field names or "*all" for all fields

    Returns:
        Issue object with requested fields
    """
    return make_request('GET', f"issue/{issue_key}?fields={fields}")


def create_issue(
    project_key: str,
    summary: str,
    description_md: str,
    issue_type: str,
    labels: Optional[List[str]] = None,
    assignee_id: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create JIRA issue with markdown description.

    Args:
        project_key: Project key (e.g., TC)
        summary: Issue summary/title
        description_md: Issue description in markdown (auto-converted to ADF)
        issue_type: Issue type ID or name
        labels: Optional list of labels
        assignee_id: Optional assignee account ID
        custom_fields: Optional custom field values (field_id: value)

    Returns:
        Created issue object with key and ID
    """
    data = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": markdown_to_adf(description_md),
            "issuetype": {"id": issue_type} if issue_type.isdigit() else {"name": issue_type},
        }
    }

    if labels:
        data["fields"]["labels"] = labels

    if assignee_id:
        data["fields"]["assignee"] = {"id": assignee_id}

    if custom_fields:
        data["fields"].update(custom_fields)

    return make_request('POST', 'issue', data)


def update_issue(
    issue_key: str,
    fields: Dict[str, Any]
) -> None:
    """Update JIRA issue fields.

    Args:
        issue_key: Issue key (e.g., TC-123)
        fields: Field updates as dict (field_name: value)
    """
    data = {"fields": fields}
    make_request('PUT', f"issue/{issue_key}", data)


def add_comment(issue_key: str, comment_md: str) -> Dict[str, Any]:
    """Add comment to JIRA issue.

    Args:
        issue_key: Issue key (e.g., TC-123)
        comment_md: Comment text in markdown (auto-converted to ADF)

    Returns:
        Created comment object
    """
    data = {"body": markdown_to_adf(comment_md)}
    return make_request('POST', f"issue/{issue_key}/comment", data)


def transition_issue(issue_key: str, transition_id: str) -> None:
    """Transition JIRA issue to a new status.

    Args:
        issue_key: Issue key (e.g., TC-123)
        transition_id: Transition ID from get_transitions()
    """
    data = {"transition": {"id": transition_id}}
    make_request('POST', f"issue/{issue_key}/transitions", data)


def get_transitions(issue_key: str) -> List[Dict[str, Any]]:
    """Get available transitions for an issue.

    Args:
        issue_key: Issue key (e.g., TC-123)

    Returns:
        List of available transitions with IDs and names
    """
    result = make_request('GET', f"issue/{issue_key}/transitions")
    return result.get('transitions', [])


def search_jql(
    jql: str,
    fields: Optional[str] = None,
    max_results: int = 50,
    start_at: int = 0
) -> Dict[str, Any]:
    """Search JIRA issues using JQL.

    Args:
        jql: JQL query string
        fields: Comma-separated field names (default: summary,status,assignee)
        max_results: Maximum results per page (max 50)
        start_at: Pagination offset

    Returns:
        Search results with issues array and total count
    """
    if fields is None:
        fields = "summary,status,assignee,priority,issuetype,labels"

    from urllib.parse import quote
    jql_encoded = quote(jql)
    endpoint = f"search?jql={jql_encoded}&fields={fields}&maxResults={max_results}&startAt={start_at}"
    return make_request('GET', endpoint)


def create_link(
    inward_issue: str,
    outward_issue: str,
    link_type: str
) -> None:
    """Create link between two JIRA issues.

    Args:
        inward_issue: Inward issue key (e.g., TC-123)
        outward_issue: Outward issue key (e.g., TC-456)
        link_type: Link type name (e.g., "Blocks", "Relates", "Depend", "Incorporates")
    """
    data = {
        "type": {"name": link_type},
        "inwardIssue": {"key": inward_issue},
        "outwardIssue": {"key": outward_issue}
    }
    make_request('POST', 'issueLink', data)


def get_user_info() -> Dict[str, Any]:
    """Get current user information.

    Returns:
        User object with accountId, displayName, emailAddress
    """
    return make_request('GET', 'myself')


def get_project_metadata(project_key: str) -> Dict[str, Any]:
    """Get project metadata including issue types and fields.

    Args:
        project_key: Project key (e.g., TC)

    Returns:
        Project object with issueTypes, components, versions
    """
    return make_request('GET', f"project/{project_key}")


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """CLI entry point with subcommand dispatch."""
    import argparse

    parser = argparse.ArgumentParser(
        description='JIRA REST API v3 client for sdlc-workflow skills',
        epilog='Set JIRA_SERVER_URL, JIRA_EMAIL, JIRA_API_TOKEN environment variables before use.'
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # get_issue
    get_issue_parser = subparsers.add_parser('get_issue', help='Get issue by key')
    get_issue_parser.add_argument('issue_key', help='Issue key (e.g., TC-123)')
    get_issue_parser.add_argument('--fields', default='*all', help='Comma-separated fields or *all')

    # create_issue
    create_issue_parser = subparsers.add_parser('create_issue', help='Create new issue')
    create_issue_parser.add_argument('--project', required=True, help='Project key')
    create_issue_parser.add_argument('--summary', required=True, help='Issue summary')
    create_issue_parser.add_argument('--description-md', required=True, help='Description in markdown')
    create_issue_parser.add_argument('--issue-type', required=True, help='Issue type ID or name')
    create_issue_parser.add_argument('--labels', help='Comma-separated labels')
    create_issue_parser.add_argument('--assignee-id', help='Assignee account ID')

    # update_issue
    update_issue_parser = subparsers.add_parser('update_issue', help='Update issue fields')
    update_issue_parser.add_argument('issue_key', help='Issue key')
    update_issue_parser.add_argument('--fields-json', required=True, help='Fields as JSON object')

    # add_comment
    add_comment_parser = subparsers.add_parser('add_comment', help='Add comment to issue')
    add_comment_parser.add_argument('issue_key', help='Issue key')
    add_comment_parser.add_argument('--comment-md', required=True, help='Comment in markdown')

    # transition_issue
    transition_parser = subparsers.add_parser('transition_issue', help='Transition issue status')
    transition_parser.add_argument('issue_key', help='Issue key')
    transition_parser.add_argument('--transition-id', required=True, help='Transition ID')

    # get_transitions
    get_transitions_parser = subparsers.add_parser('get_transitions', help='Get available transitions')
    get_transitions_parser.add_argument('issue_key', help='Issue key')

    # search_jql
    search_parser = subparsers.add_parser('search_jql', help='Search issues with JQL')
    search_parser.add_argument('--jql', required=True, help='JQL query string')
    search_parser.add_argument('--fields', help='Comma-separated fields')
    search_parser.add_argument('--max-results', type=int, default=50, help='Max results (default: 50)')
    search_parser.add_argument('--start-at', type=int, default=0, help='Pagination offset')

    # create_link
    link_parser = subparsers.add_parser('create_link', help='Create issue link')
    link_parser.add_argument('--inward', required=True, help='Inward issue key')
    link_parser.add_argument('--outward', required=True, help='Outward issue key')
    link_parser.add_argument('--link-type', required=True, help='Link type name')

    # get_user_info
    subparsers.add_parser('get_user_info', help='Get current user info')

    # get_project_metadata
    project_parser = subparsers.add_parser('get_project_metadata', help='Get project metadata')
    project_parser.add_argument('project_key', help='Project key')

    # Parse and execute
    args = parser.parse_args()

    result = None

    if args.command == 'get_issue':
        result = get_issue(args.issue_key, args.fields)

    elif args.command == 'create_issue':
        labels = args.labels.split(',') if args.labels else None
        result = create_issue(
            args.project,
            args.summary,
            args.description_md,
            args.issue_type,
            labels=labels,
            assignee_id=args.assignee_id
        )

    elif args.command == 'update_issue':
        fields = json.loads(args.fields_json)
        update_issue(args.issue_key, fields)
        result = {"updated": True}

    elif args.command == 'add_comment':
        result = add_comment(args.issue_key, args.comment_md)

    elif args.command == 'transition_issue':
        transition_issue(args.issue_key, args.transition_id)
        result = {"transitioned": True}

    elif args.command == 'get_transitions':
        result = get_transitions(args.issue_key)

    elif args.command == 'search_jql':
        result = search_jql(args.jql, args.fields, args.max_results, args.start_at)

    elif args.command == 'create_link':
        create_link(args.inward, args.outward, args.link_type)
        result = {"linked": True}

    elif args.command == 'get_user_info':
        result = get_user_info()

    elif args.command == 'get_project_metadata':
        result = get_project_metadata(args.project_key)

    # Print result as JSON
    if result:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
