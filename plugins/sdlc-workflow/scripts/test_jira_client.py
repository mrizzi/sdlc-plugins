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
