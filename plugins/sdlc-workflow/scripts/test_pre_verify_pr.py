#!/usr/bin/env python3
"""Tests for pre_verify_pr.py — PR URL extraction and input transformation."""

import json
import os
import subprocess
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
import pre_verify_pr


# --- extract_pr_url ---

def test_extract_pr_url_adf_inline_card():
    issue = {"fields": {"customfield_10875": {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [
            {"type": "inlineCard", "attrs": {"url": "https://github.com/org/repo/pull/42"}}
        ]}]
    }}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "https://github.com/org/repo/pull/42", f"Got: {result}"


def test_extract_pr_url_plain_string():
    issue = {"fields": {"customfield_10875": "https://github.com/org/repo/pull/7"}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "https://github.com/org/repo/pull/7", f"Got: {result}"


def test_extract_pr_url_missing_field():
    issue = {"fields": {}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "", f"Expected empty string, got: {result}"


def test_extract_pr_url_null_field():
    issue = {"fields": {"customfield_10875": None}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "", f"Expected empty string, got: {result}"


def test_extract_pr_url_adf_no_inline_card():
    issue = {"fields": {"customfield_10875": {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [
            {"type": "text", "text": "no link here"}
        ]}]
    }}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "", f"Expected empty string, got: {result}"


# --- transform_to_input ---

def test_transform_basic():
    issue = {"fields": {
        "summary": "Add feature X",
        "description": {"type": "doc", "content": []},
        "status": {"name": "In Progress"},
        "labels": ["backend", "api"],
        "issuelinks": [],
    }}
    result = pre_verify_pr.transform_to_input(issue, "TC-100", "https://github.com/o/r/pull/1")
    assert result["task_id"] == "TC-100"
    assert result["task"]["summary"] == "Add feature X"
    assert result["task"]["status"] == "In Progress"
    assert result["task"]["labels"] == ["backend", "api"]
    assert result["task"]["issue_links"] == []
    assert result["pr_url"] == "https://github.com/o/r/pull/1"
    assert result["source"]["tracker"] == "jira"
    assert result["source"]["raw"] is issue


def test_transform_issue_links():
    issue = {"fields": {
        "summary": "S", "description": {}, "status": {"name": "Open"},
        "labels": [], "issuelinks": [
            {"type": {"name": "Blocks"}, "outwardIssue": {"key": "TC-200"}},
            {"type": {"name": "Related"}, "inwardIssue": {"key": "TC-300"}},
        ],
    }}
    links = pre_verify_pr.transform_to_input(issue, "TC-100", "")["task"]["issue_links"]
    assert len(links) == 2
    assert links[0] == {"type": "Blocks", "direction": "outward", "key": "TC-200"}
    assert links[1] == {"type": "Related", "direction": "inward", "key": "TC-300"}


def test_transform_custom_fields():
    issue = {"fields": {
        "summary": "S", "description": {}, "status": None, "labels": [],
        "issuelinks": [],
        "customfield_10875": "https://github.com/o/r/pull/5",
        "customfield_99999": {"value": "something"},
        "priority": {"name": "High"},
    }}
    cf = pre_verify_pr.transform_to_input(issue, "TC-1", "")["task"]["custom_fields"]
    assert "customfield_10875" in cf
    assert "customfield_99999" in cf
    assert "priority" not in cf


def test_transform_empty_fields():
    issue = {"fields": {}}
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "")
    assert result["task"]["summary"] == ""
    assert result["task"]["status"] == ""
    assert result["task"]["labels"] == []
    assert result["task"]["issue_links"] == []


def test_transform_null_status():
    issue = {"fields": {"summary": "S", "status": None, "labels": [], "issuelinks": []}}
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "")
    assert result["task"]["status"] == ""


def test_transform_large_payload():
    """Regression test: large payloads must work via stdin, not argv."""
    issue = {"fields": {
        "summary": "Large issue",
        "description": "x" * 500_000,
        "status": {"name": "Open"},
        "labels": [],
        "issuelinks": [],
    }}
    payload = json.dumps(issue)
    assert len(payload) > 500_000

    result = subprocess.run(
        [sys.executable, os.path.join(script_dir, "pre_verify_pr.py"),
         "transform", "TC-BIG", "https://example.com/pr/1"],
        input=payload, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    output = json.loads(result.stdout)
    assert output["task_id"] == "TC-BIG"
    assert output["task"]["summary"] == "Large issue"


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
