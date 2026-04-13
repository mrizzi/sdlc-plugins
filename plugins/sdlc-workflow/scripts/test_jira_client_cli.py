#!/usr/bin/env python3
"""Integration tests for jira-client.py CLI argument validation.

Verifies that the CLI correctly handles:
- Malformed JSON in --fields-json argument
- Clear error messages for invalid input
- Non-zero exit codes on errors
"""

import subprocess
import sys
import os


def run_cli_command(args):
    """Run jira-client.py with given arguments and return (exit_code, stdout, stderr)."""
    script_path = os.path.join(os.path.dirname(__file__), 'jira-client.py')
    cmd = [sys.executable, script_path] + args

    # Run without credentials to avoid actual API calls
    env = os.environ.copy()
    env.pop('JIRA_SERVER_URL', None)
    env.pop('JIRA_EMAIL', None)
    env.pop('JIRA_API_TOKEN', None)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env
    )

    return result.returncode, result.stdout, result.stderr


def test_invalid_json_missing_quotes():
    """Test that malformed JSON (missing quotes) produces clear error."""
    exit_code, stdout, stderr = run_cli_command([
        'update_issue',
        'TC-123',
        '--fields-json', '{summary: "test"}'  # Missing quotes around key
    ])

    # Should exit with non-zero code
    assert exit_code != 0, f"Expected non-zero exit code, got {exit_code}"

    # Should have error message in stderr
    assert "Invalid JSON" in stderr, f"Expected 'Invalid JSON' in stderr, got: {stderr}"
    assert "❌" in stderr, f"Expected error emoji in stderr, got: {stderr}"

    # Should NOT have Python traceback
    assert "Traceback" not in stderr, f"Should not show Python traceback, got: {stderr}"
    assert "JSONDecodeError" not in stderr, f"Should not show raw JSONDecodeError, got: {stderr}"

    print("✓ Invalid JSON (missing quotes) test passed")


def test_invalid_json_trailing_comma():
    """Test that malformed JSON (trailing comma) produces clear error."""
    exit_code, stdout, stderr = run_cli_command([
        'update_issue',
        'TC-123',
        '--fields-json', '{"summary": "test",}'  # Trailing comma
    ])

    # Should exit with non-zero code
    assert exit_code != 0, f"Expected non-zero exit code, got {exit_code}"

    # Should have error message
    assert "Invalid JSON" in stderr, f"Expected 'Invalid JSON' in stderr, got: {stderr}"

    # Should NOT have Python traceback
    assert "Traceback" not in stderr, f"Should not show Python traceback, got: {stderr}"

    print("✓ Invalid JSON (trailing comma) test passed")


def test_invalid_json_unclosed_brace():
    """Test that malformed JSON (unclosed brace) produces clear error."""
    exit_code, stdout, stderr = run_cli_command([
        'update_issue',
        'TC-123',
        '--fields-json', '{"summary": "test"'  # Missing closing brace
    ])

    # Should exit with non-zero code
    assert exit_code != 0, f"Expected non-zero exit code, got {exit_code}"

    # Should have error message
    assert "Invalid JSON" in stderr, f"Expected 'Invalid JSON' in stderr, got: {stderr}"

    # Should NOT have Python traceback
    assert "Traceback" not in stderr, f"Should not show Python traceback, got: {stderr}"

    print("✓ Invalid JSON (unclosed brace) test passed")


def test_error_message_includes_position():
    """Test that error message includes line and column position."""
    exit_code, stdout, stderr = run_cli_command([
        'update_issue',
        'TC-123',
        '--fields-json', '{bad json}'
    ])

    # Should exit with non-zero code
    assert exit_code != 0, f"Expected non-zero exit code, got {exit_code}"

    # Should include position information
    assert "Position:" in stderr, f"Expected 'Position:' in stderr, got: {stderr}"
    assert "line" in stderr, f"Expected 'line' in stderr, got: {stderr}"
    assert "column" in stderr, f"Expected 'column' in stderr, got: {stderr}"

    print("✓ Error message includes position test passed")


def test_error_message_includes_help():
    """Test that error message includes helpful guidance."""
    exit_code, stdout, stderr = run_cli_command([
        'update_issue',
        'TC-123',
        '--fields-json', 'not-json'
    ])

    # Should include guidance
    assert "properly formatted" in stderr or "quotes around strings" in stderr, \
        f"Expected formatting guidance in stderr, got: {stderr}"

    print("✓ Error message includes help test passed")


def run_all_tests():
    """Run all CLI validation tests and report results."""
    tests = [
        test_invalid_json_missing_quotes,
        test_invalid_json_trailing_comma,
        test_invalid_json_unclosed_brace,
        test_error_message_includes_position,
        test_error_message_includes_help,
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
        print(f"FAILED: {len(failed)} CLI test(s) failed:")
        for name in failed:
            print(f"  - {name}")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(tests)} CLI tests passed!")
        sys.exit(0)


if __name__ == '__main__':
    run_all_tests()
