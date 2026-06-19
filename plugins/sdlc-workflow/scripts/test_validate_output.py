#!/usr/bin/env python3
"""Tests for strip_extra_properties.py and validate-output-schema.sh."""

import json
import os
import shutil
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VALIDATE_SCRIPT = os.path.join(SCRIPT_DIR, "validate-output-schema.sh")
SCHEMA_FILE = os.path.join(SCRIPT_DIR, "..", "schemas", "verify-pr-result.schema.json")

sys.path.insert(0, SCRIPT_DIR)
import strip_extra_properties


def _load_schema():
    with open(SCHEMA_FILE) as f:
        return json.load(f)


def _make_report(**overrides):
    base = {
        "jira_issue_id": "TC-100",
        "pr_repo": "org/repo",
        "pr_number": 1,
        "commit_sha": "abc1234",
        "overall": "PASS",
        "table_md": "| Check | Result |",
        "report_md": "## Report",
        "report_adf": {"type": "doc", "content": []},
        "plugin_version": "0.9.2",
    }
    base.update(overrides)
    return base


# --- Unit tests (strip function directly) ---

def test_strip_top_level_extra():
    schema = _load_schema()
    instance = {"report": _make_report(), "actions": [], "extra": "gone"}
    result = strip_extra_properties.strip(instance, schema, schema)
    assert "extra" not in result
    assert "report" in result
    assert "actions" in result


def test_strip_report_extra():
    schema = _load_schema()
    instance = {"report": _make_report(extra_field="gone"), "actions": []}
    result = strip_extra_properties.strip(instance, schema, schema)
    assert "extra_field" not in result["report"]
    assert result["report"]["jira_issue_id"] == "TC-100"


def test_strip_action_post_pr_reply():
    schema = _load_schema()
    instance = {
        "report": _make_report(),
        "actions": [{
            "type": "post_pr_reply", "repo": "o/r", "pr_number": 1,
            "comment_id": 123, "body": "reply",
            "is_review_body": True, "is_issue_comment": False,
        }],
    }
    result = strip_extra_properties.strip(instance, schema, schema)
    action = result["actions"][0]
    assert "is_review_body" not in action
    assert "is_issue_comment" not in action
    assert action["body"] == "reply"


def test_strip_action_create_subtask():
    schema = _load_schema()
    instance = {
        "report": _make_report(),
        "actions": [{
            "type": "create_subtask", "ref": "s1", "parent": "TC-100",
            "summary": "Fix", "labels": [], "description_adf": {},
            "confidence": 0.95,
        }],
    }
    result = strip_extra_properties.strip(instance, schema, schema)
    assert "confidence" not in result["actions"][0]
    assert result["actions"][0]["summary"] == "Fix"


def test_preserves_valid_fields():
    schema = _load_schema()
    instance = {
        "report": _make_report(),
        "actions": [{
            "type": "create_link", "link_type": "Blocks",
            "inward": "TC-101", "outward": "TC-100",
        }],
    }
    result = strip_extra_properties.strip(instance, schema, schema)
    assert result["actions"][0] == {
        "type": "create_link", "link_type": "Blocks",
        "inward": "TC-101", "outward": "TC-100",
    }


def test_strips_multiple_action_types():
    schema = _load_schema()
    instance = {
        "report": _make_report(),
        "actions": [
            {"type": "create_subtask", "ref": "s1", "parent": "TC-100", "summary": "A", "labels": [], "description_adf": {}, "extra1": True},
            {"type": "post_pr_reply", "repo": "o/r", "pr_number": 1, "comment_id": 1, "body": "B", "extra2": "x"},
            {"type": "post_comment", "issue": "TC-100", "body_adf": {}, "extra3": 42},
            {"type": "post_report"},
        ],
    }
    result = strip_extra_properties.strip(instance, schema, schema)
    assert "extra1" not in result["actions"][0]
    assert "extra2" not in result["actions"][1]
    assert "extra3" not in result["actions"][2]


def test_no_strip_when_additional_allowed():
    schema = {"type": "object", "properties": {"a": {"type": "string"}}}
    instance = {"a": "val", "b": "extra"}
    result = strip_extra_properties.strip(instance, schema, schema)
    assert "b" in result


# --- Integration test (full bash script) ---

def test_integration_strips_and_validates():
    payload = {
        "report": _make_report(),
        "actions": [
            {"type": "post_pr_reply", "repo": "o/r", "pr_number": 1,
             "comment_id": 1, "body": "B", "is_review_body": True},
            {"type": "post_report"},
        ],
    }
    work_dir = tempfile.mkdtemp()
    output_dir = os.path.join(work_dir, "output")
    os.makedirs(output_dir)
    result_file = os.path.join(output_dir, "agent-result.json")
    with open(result_file, "w") as f:
        json.dump(payload, f)

    result = subprocess.run(
        ["bash", VALIDATE_SCRIPT],
        cwd=work_dir,
        capture_output=True, text=True,
        env={**os.environ,
             "FULLSEND_OUTPUT_SCHEMA": os.path.abspath(SCHEMA_FILE),
             "FULLSEND_OUTPUT_FILE": "agent-result.json"},
    )
    assert result.returncode == 0, f"Expected pass, got exit {result.returncode}: {result.stdout}{result.stderr}"
    assert "stripped" in result.stdout
    assert "PASS" in result.stdout

    with open(result_file) as f:
        cleaned = json.load(f)
    assert "is_review_body" not in cleaned["actions"][0]

    shutil.rmtree(work_dir)


def test_integration_fails_on_missing_required():
    payload = {"report": _make_report(), "actions": [{"type": "create_subtask", "ref": "s1"}]}
    work_dir = tempfile.mkdtemp()
    output_dir = os.path.join(work_dir, "output")
    os.makedirs(output_dir)
    with open(os.path.join(output_dir, "agent-result.json"), "w") as f:
        json.dump(payload, f)

    result = subprocess.run(
        ["bash", VALIDATE_SCRIPT],
        cwd=work_dir,
        capture_output=True, text=True,
        env={**os.environ,
             "FULLSEND_OUTPUT_SCHEMA": os.path.abspath(SCHEMA_FILE),
             "FULLSEND_OUTPUT_FILE": "agent-result.json"},
    )
    assert result.returncode != 0
    assert "FAIL" in result.stdout + result.stderr

    shutil.rmtree(work_dir)


# --- runner ---

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = []
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed.append(t.__name__)
    print(f"{'=' * 60}")
    if failed:
        print(f"FAILED: {len(failed)}/{len(tests)} test(s) failed")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(tests)} tests passed")
        sys.exit(0)
