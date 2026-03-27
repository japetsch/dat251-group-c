from datetime import datetime
from typing import Any


def assert_dicts_match(actual: dict[str, Any], expected: dict[str, Any]):
    """Compare dicts, allowing datetime to be compared to ISO8601-timestamps"""
    for key, expected_val in expected.items():
        actual_val = actual[key]

        if isinstance(expected_val, datetime):
            assert (
                datetime.fromisoformat(actual_val) == expected_val
            ), f"{key}: {actual_val} != {expected_val}"
        elif isinstance(expected_val, list):
            assert len(actual_val) == len(
                expected_val
            ), f"{key}: length {len(actual_val)} != {len(expected_val)}"
            for a, e in zip(actual_val, expected_val):
                assert_dicts_match(a, e)
        elif isinstance(expected_val, dict):
            assert_dicts_match(actual_val, expected_val)
        else:
            assert actual_val == expected_val, f"{key}: {actual_val} != {expected_val}"


def dictmatch_in(haystack: list[dict[str, Any]], needle: dict[str, Any]) -> bool:
    """
    This is very hacky and will return bad error messages.

    TODO: rephrase tests using it
    """
    for x in haystack:
        try:
            assert_dicts_match(x, needle)
            return True
        except AssertionError:
            pass

    return False
