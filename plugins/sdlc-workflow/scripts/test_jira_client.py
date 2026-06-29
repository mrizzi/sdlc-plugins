#!/usr/bin/env python3
"""Tests for jira-client.py markdown-to-ADF conversion.

Verifies that the markdown parser correctly handles:
- Fenced code blocks with blank lines
- Multi-paragraph list items
- Nested markdown structures
"""

import sys
import json
import os
import importlib.util

# Import jira-client.py dynamically (has hyphen in name)
script_dir = os.path.dirname(os.path.abspath(__file__))
jira_client_path = os.path.join(script_dir, 'jira-client.py')
spec = importlib.util.spec_from_file_location("jira_client", jira_client_path)
jira_client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jira_client)
markdown_to_adf = jira_client.markdown_to_adf
sanitize_adf = jira_client.sanitize_adf
get_versions = jira_client.get_versions
create_issue = jira_client.create_issue


def test_code_block_with_blank_lines():
    """Test that code blocks with blank lines are parsed correctly."""
    md = """Here is some code:

```python
def foo():
    print("first")

    print("second")
```

After the code block."""

    result = markdown_to_adf(md)

    # Should have 3 content nodes: paragraph, code block, paragraph
    assert len(result["content"]) == 3, f"Expected 3 nodes, got {len(result['content'])}"

    # Second node should be a code block
    code_node = result["content"][1]
    assert code_node["type"] == "codeBlock", f"Expected codeBlock, got {code_node['type']}"
    assert code_node["attrs"]["language"] == "python"

    # Code should contain the blank line
    code_text = code_node["content"][0]["text"]
    assert 'print("first")' in code_text
    assert 'print("second")' in code_text
    # Count newlines to verify blank line is preserved
    assert code_text.count('\n') >= 3, f"Expected at least 3 newlines in code, got {code_text.count(chr(10))}"

    print("✓ Code block with blank lines test passed")


def test_multi_paragraph_list_item():
    """Test that multi-paragraph list items are parsed correctly."""
    md = """- First item with paragraph.

  Second paragraph of first item.

- Second item"""

    result = markdown_to_adf(md)

    # Should parse as list followed by paragraph and another list
    # (Current implementation treats double-newline as block boundary,
    # so this will create separate blocks. This test documents current behavior.)
    assert len(result["content"]) >= 1, "Should have at least one content node"

    # First node should be a bullet list
    first_node = result["content"][0]
    assert first_node["type"] == "bulletList", f"Expected bulletList, got {first_node['type']}"

    print("✓ Multi-paragraph list item test passed")


def test_code_block_at_start():
    """Test code block at the very start of the document."""
    md = """```bash
echo "hello"
echo "world"
```"""

    result = markdown_to_adf(md)

    # Should have 1 code block
    assert len(result["content"]) == 1, f"Expected 1 node, got {len(result['content'])}"
    assert result["content"][0]["type"] == "codeBlock"

    print("✓ Code block at start test passed")


def test_code_block_without_language():
    """Test code block without language specifier."""
    md = """```
plain text

with blank line
```"""

    result = markdown_to_adf(md)

    # Should have 1 code block with default language
    assert len(result["content"]) == 1
    code_node = result["content"][0]
    assert code_node["type"] == "codeBlock"
    assert code_node["attrs"]["language"] == "text"

    # Should preserve blank line
    code_text = code_node["content"][0]["text"]
    assert "plain text" in code_text
    assert "with blank line" in code_text

    print("✓ Code block without language test passed")


def test_multiple_code_blocks():
    """Test multiple code blocks in sequence."""
    md = """First block:

```python
x = 1

y = 2
```

Second block:

```javascript
const a = 1;

const b = 2;
```"""

    result = markdown_to_adf(md)

    # Should have: paragraph, code, paragraph, code
    assert len(result["content"]) == 4, f"Expected 4 nodes, got {len(result['content'])}"
    assert result["content"][0]["type"] == "paragraph"
    assert result["content"][1]["type"] == "codeBlock"
    assert result["content"][1]["attrs"]["language"] == "python"
    assert result["content"][2]["type"] == "paragraph"
    assert result["content"][3]["type"] == "codeBlock"
    assert result["content"][3]["attrs"]["language"] == "javascript"

    print("✓ Multiple code blocks test passed")


def test_nested_structures():
    """Test nested markdown structures (lists with code)."""
    md = """## Implementation Notes

- Step 1: Do this
- Step 2: Run this code:

```bash
npm install
```

- Step 3: Verify"""

    result = markdown_to_adf(md)

    # Should have multiple nodes including heading, list, code, list
    assert len(result["content"]) >= 3, f"Expected at least 3 nodes, got {len(result['content'])}"

    # First should be heading (rendered as bold paragraph)
    assert result["content"][0]["type"] == "paragraph"

    # Should have a code block somewhere
    has_code_block = any(node["type"] == "codeBlock" for node in result["content"])
    assert has_code_block, "Expected to find a codeBlock node"

    print("✓ Nested structures test passed")


def test_horizontal_rule():
    """Test horizontal rules are parsed correctly."""
    md = """Before

---

After"""

    result = markdown_to_adf(md)

    # Should have: paragraph, rule, paragraph
    assert len(result["content"]) == 3
    assert result["content"][0]["type"] == "paragraph"
    assert result["content"][1]["type"] == "rule"
    assert result["content"][2]["type"] == "paragraph"

    print("✓ Horizontal rule test passed")


def test_sanitize_adf_converts_tasklist_to_bulletlist():
    """Verifies that taskList/taskItem nodes without localId are converted to bulletList/listItem."""
    # Given an ADF document with taskList/taskItem nodes missing localId
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "taskList",
                "content": [
                    {
                        "type": "taskItem",
                        "attrs": {"state": "TODO"},
                        "content": [{"type": "text", "text": "First criterion"}]
                    },
                    {
                        "type": "taskItem",
                        "attrs": {"state": "TODO"},
                        "content": [{"type": "text", "text": "Second criterion"}]
                    }
                ]
            }
        ]
    }

    # When sanitizing the ADF
    result = sanitize_adf(doc)

    # Then taskList becomes bulletList and taskItems become listItems
    list_node = result["content"][0]
    assert list_node["type"] == "bulletList", f"Expected bulletList, got {list_node['type']}"
    assert "attrs" not in list_node, "bulletList should not have attrs"

    for item in list_node["content"]:
        assert item["type"] == "listItem", f"Expected listItem, got {item['type']}"
        assert "attrs" not in item, "listItem should not have attrs"

    assert list_node["content"][0]["content"][0]["text"] == "First criterion"
    assert list_node["content"][1]["content"][0]["text"] == "Second criterion"

    print("✓ sanitize_adf converts taskList to bulletList test passed")


def test_sanitize_adf_preserves_content():
    """Verifies that taskItem inner content (paragraph and text nodes) is preserved."""
    # Given a taskItem with nested paragraph content
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "taskList",
                "content": [
                    {
                        "type": "taskItem",
                        "attrs": {"state": "TODO"},
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {"type": "text", "text": "Bold text", "marks": [{"type": "strong"}]},
                                    {"type": "text", "text": " and normal text"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # When sanitizing
    result = sanitize_adf(doc)

    # Then inner content is preserved
    item = result["content"][0]["content"][0]
    para = item["content"][0]
    assert para["type"] == "paragraph"
    assert para["content"][0]["text"] == "Bold text"
    assert para["content"][0]["marks"] == [{"type": "strong"}]
    assert para["content"][1]["text"] == " and normal text"

    print("✓ sanitize_adf preserves content test passed")


def test_sanitize_adf_handles_nested_tasklist():
    """Verifies that nested taskList inside other ADF containers is recursively sanitized."""
    # Given a taskList nested inside a panel
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "panel",
                "attrs": {"panelType": "info"},
                "content": [
                    {
                        "type": "taskList",
                        "content": [
                            {
                                "type": "taskItem",
                                "attrs": {"state": "TODO"},
                                "content": [{"type": "text", "text": "Nested item"}]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # When sanitizing
    result = sanitize_adf(doc)

    # Then the nested taskList is also converted
    panel = result["content"][0]
    assert panel["type"] == "panel", "Panel should remain unchanged"
    nested_list = panel["content"][0]
    assert nested_list["type"] == "bulletList", f"Expected bulletList, got {nested_list['type']}"
    assert nested_list["content"][0]["type"] == "listItem"

    print("✓ sanitize_adf handles nested taskList test passed")


def test_sanitize_adf_noop_for_bulletlist():
    """Verifies that ADF with only bulletList/listItem passes through unchanged."""
    # Given an ADF document with standard bulletList
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": "Already a bullet"}]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    import copy
    original = copy.deepcopy(doc)

    # When sanitizing
    result = sanitize_adf(doc)

    # Then the document is unchanged
    assert result == original, "bulletList document should pass through unchanged"

    print("✓ sanitize_adf no-op for bulletList test passed")


def test_create_issue_adf_has_no_tasklist():
    """Verifies that create_issue() output ADF contains no taskList/taskItem nodes."""
    # Given markdown with checkbox-style items (the format that triggers the bug)
    md = "## Acceptance Criteria\n\n- [ ] First criterion\n- [ ] Second criterion"

    # When converting to ADF (same path as create_issue)
    adf = sanitize_adf(markdown_to_adf(md))

    # Then no taskList or taskItem nodes should exist anywhere in the tree
    def find_node_types(node):
        types = {node.get("type")}
        for child in node.get("content", []):
            if isinstance(child, dict):
                types.update(find_node_types(child))
        return types

    all_types = find_node_types(adf)
    assert "taskList" not in all_types, "ADF should not contain taskList nodes"
    assert "taskItem" not in all_types, "ADF should not contain taskItem nodes"

    print("✓ create_issue ADF has no taskList test passed")


def test_get_versions_unreleased_only_filters_correctly():
    """Verifies that get_versions with unreleased_only filters out released and archived versions."""
    # Given a list of versions with mixed released/archived states
    all_versions = [
        {"id": "1", "name": "1.0.0", "released": True, "archived": False},
        {"id": "2", "name": "1.1.0", "released": False, "archived": False},
        {"id": "3", "name": "0.9.0", "released": True, "archived": True},
        {"id": "4", "name": "2.0.0", "released": False, "archived": False},
        {"id": "5", "name": "1.2.0", "released": False, "archived": True},
    ]

    original_make_request = jira_client.make_request
    jira_client.make_request = lambda method, endpoint, data=None: all_versions
    try:
        # When calling get_versions with unreleased_only=True
        filtered = get_versions("TEST", unreleased_only=True)

        # Then only non-released, non-archived versions remain
        assert len(filtered) == 2, f"Expected 2 versions, got {len(filtered)}"
        assert filtered[0]["name"] == "1.1.0"
        assert filtered[1]["name"] == "2.0.0"

        # When calling with unreleased_only=False, no filtering happens
        unfiltered = get_versions("TEST", unreleased_only=False)
        assert len(unfiltered) == 5, f"Expected 5 versions, got {len(unfiltered)}"
    finally:
        jira_client.make_request = original_make_request

    print("✓ get_versions unreleased_only filter test passed")


def test_create_issue_priority_field_mapping():
    """Verifies that create_issue maps priority parameter to correct Jira field structure."""
    captured = {}
    original_make_request = jira_client.make_request

    def fake_make_request(method, endpoint, data=None):
        captured["data"] = data
        return {"key": "TEST-1", "id": "1"}

    jira_client.make_request = fake_make_request
    try:
        # When creating an issue with a priority
        create_issue("TC", "Test", "desc", "Task", priority="Major")

        # Then the priority field is correctly mapped
        assert captured["data"]["fields"]["priority"] == {"name": "Major"}
    finally:
        jira_client.make_request = original_make_request

    print("✓ create_issue priority field mapping test passed")


def test_create_issue_fix_versions_field_mapping():
    """Verifies that create_issue maps fix_versions list to correct Jira fixVersions array."""
    captured = {}
    original_make_request = jira_client.make_request

    def fake_make_request(method, endpoint, data=None):
        captured["data"] = data
        return {"key": "TEST-1", "id": "1"}

    jira_client.make_request = fake_make_request
    try:
        # When creating an issue with fix_versions
        create_issue("TC", "Test", "desc", "Task", fix_versions=["RHTPA 1.5.0", "RHTPA 1.6.0"])

        # Then each version is wrapped in a name object
        fv = captured["data"]["fields"]["fixVersions"]
        assert len(fv) == 2, f"Expected 2 fixVersions, got {len(fv)}"
        assert fv[0] == {"name": "RHTPA 1.5.0"}
        assert fv[1] == {"name": "RHTPA 1.6.0"}
    finally:
        jira_client.make_request = original_make_request

    print("✓ create_issue fix_versions field mapping test passed")


def test_create_issue_omits_priority_when_none():
    """Verifies that create_issue omits priority field when not provided."""
    captured = {}
    original_make_request = jira_client.make_request

    def fake_make_request(method, endpoint, data=None):
        captured["data"] = data
        return {"key": "TEST-1", "id": "1"}

    jira_client.make_request = fake_make_request
    try:
        create_issue("TC", "Test", "desc", "Task")
        assert "priority" not in captured["data"]["fields"]
    finally:
        jira_client.make_request = original_make_request

    print("✓ create_issue omits priority when None test passed")


def test_create_issue_omits_fix_versions_when_none():
    """Verifies that create_issue omits fixVersions field when not provided."""
    captured = {}
    original_make_request = jira_client.make_request

    def fake_make_request(method, endpoint, data=None):
        captured["data"] = data
        return {"key": "TEST-1", "id": "1"}

    jira_client.make_request = fake_make_request
    try:
        create_issue("TC", "Test", "desc", "Task")
        assert "fixVersions" not in captured["data"]["fields"]
    finally:
        jira_client.make_request = original_make_request

    print("✓ create_issue omits fix_versions when None test passed")


def test_create_issue_all_optional_fields_together():
    """Verifies that create_issue correctly merges all optional fields into the payload."""
    captured = {}
    original_make_request = jira_client.make_request

    def fake_make_request(method, endpoint, data=None):
        captured["data"] = data
        return {"key": "TEST-1", "id": "1"}

    jira_client.make_request = fake_make_request
    try:
        # When creating an issue with all optional fields
        create_issue(
            "TC", "Test", "desc", "Task",
            labels=["ai-generated-jira", "feature"],
            assignee_id="user-123",
            priority="Major",
            fix_versions=["1.5.0", "1.6.0"],
            custom_fields={"customfield_10010": "value"},
        )

        # Then all fields are present and correctly structured
        fields = captured["data"]["fields"]
        assert fields["labels"] == ["ai-generated-jira", "feature"]
        assert fields["assignee"] == {"id": "user-123"}
        assert fields["priority"] == {"name": "Major"}
        assert fields["fixVersions"] == [{"name": "1.5.0"}, {"name": "1.6.0"}]
        assert fields["customfield_10010"] == "value"
    finally:
        jira_client.make_request = original_make_request

    print("✓ create_issue all optional fields together test passed")


def test_create_issue_fix_versions_filters_empty_names():
    """Verifies that create_issue filters out empty version names from fixVersions."""
    captured = {}
    original_make_request = jira_client.make_request

    def fake_make_request(method, endpoint, data=None):
        captured["data"] = data
        return {"key": "TEST-1", "id": "1"}

    jira_client.make_request = fake_make_request
    try:
        # When creating an issue with empty version names mixed in
        create_issue("TC", "Test", "desc", "Task", fix_versions=["1.0", "", "2.0"])

        # Then empty names are filtered out
        fv = captured["data"]["fields"]["fixVersions"]
        assert len(fv) == 2, f"Expected 2 fixVersions (empty filtered), got {len(fv)}"
        assert fv[0] == {"name": "1.0"}
        assert fv[1] == {"name": "2.0"}
    finally:
        jira_client.make_request = original_make_request

    print("✓ create_issue fix_versions filters empty names test passed")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_code_block_with_blank_lines,
        test_multi_paragraph_list_item,
        test_code_block_at_start,
        test_code_block_without_language,
        test_multiple_code_blocks,
        test_nested_structures,
        test_horizontal_rule,
        test_sanitize_adf_converts_tasklist_to_bulletlist,
        test_sanitize_adf_preserves_content,
        test_sanitize_adf_handles_nested_tasklist,
        test_sanitize_adf_noop_for_bulletlist,
        test_create_issue_adf_has_no_tasklist,
        test_get_versions_unreleased_only_filters_correctly,
        test_create_issue_priority_field_mapping,
        test_create_issue_fix_versions_field_mapping,
        test_create_issue_omits_priority_when_none,
        test_create_issue_omits_fix_versions_when_none,
        test_create_issue_all_optional_fields_together,
        test_create_issue_fix_versions_filters_empty_names,
    ]

    failed = []

    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed.append(test.__name__)
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed.append(test.__name__)

    print(f"\n{'='*60}")
    if failed:
        print(f"FAILED: {len(failed)} test(s) failed:")
        for name in failed:
            print(f"  - {name}")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(tests)} tests passed!")
        sys.exit(0)


if __name__ == '__main__':
    run_all_tests()
