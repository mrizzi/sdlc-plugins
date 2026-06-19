#!/usr/bin/env python3
"""Tests for execute-actions.py ref resolution and action processing."""

import sys
import os
import json
import importlib.util

script_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "execute_actions",
    os.path.join(script_dir, "execute-actions.py"),
)
execute_actions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(execute_actions)

resolve_refs = execute_actions.resolve_refs


def test_resolve_refs_replaces_key():
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "Sub-task [{{subtask-1.key}}]({{subtask-1.url}}) created."
    result = resolve_refs(text, registry)
    assert result == "Sub-task [TC-100](https://jira.example.com/browse/TC-100) created.", f"Got: {result}"


def test_resolve_refs_no_placeholders():
    registry = {}
    text = "No placeholders here."
    result = resolve_refs(text, registry)
    assert result == "No placeholders here."


def test_resolve_refs_unknown_ref_raises():
    registry = {}
    text = "{{unknown-ref.key}}"
    try:
        resolve_refs(text, registry)
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_resolve_refs_in_adf():
    registry = {"rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"}}
    adf = {
        "type": "doc",
        "content": [
            {"type": "text", "text": "Task {{rc-1.key}} created"}
        ]
    }
    result = execute_actions.resolve_refs_in_obj(adf, registry)
    assert result["content"][0]["text"] == "Task TC-200 created"


def test_resolve_refs_multiple_different_refs():
    registry = {
        "subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"},
        "rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"},
    }
    text = "Sub-task {{subtask-1.key}} and root-cause {{rc-1.key}} ({{rc-1.url}})."
    result = resolve_refs(text, registry)
    assert result == "Sub-task TC-100 and root-cause TC-200 (https://jira.example.com/browse/TC-200).", f"Got: {result}"


def test_resolve_refs_repeated_placeholder():
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "{{subtask-1.key}} depends on {{subtask-1.key}}."
    result = resolve_refs(text, registry)
    assert result == "TC-100 depends on TC-100.", f"Got: {result}"


def test_resolve_refs_mixed_key_url_same_ref():
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "See {{subtask-1.key}} at {{subtask-1.url}}; {{subtask-1.key}} must be done first."
    result = resolve_refs(text, registry)
    assert result == "See TC-100 at https://jira.example.com/browse/TC-100; TC-100 must be done first.", f"Got: {result}"


if __name__ == "__main__":
    test_resolve_refs_replaces_key()
    test_resolve_refs_no_placeholders()
    test_resolve_refs_unknown_ref_raises()
    test_resolve_refs_in_adf()
    test_resolve_refs_multiple_different_refs()
    test_resolve_refs_repeated_placeholder()
    test_resolve_refs_mixed_key_url_same_ref()
    print("All tests passed.")
