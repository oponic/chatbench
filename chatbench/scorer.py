from __future__ import annotations

import json
import re
from typing import Any


def _norm(s: str) -> str:
    return s.strip().lower()


def _check(check: dict[str, Any], answer: str) -> tuple[bool, str]:
    kind = check["check"]

    if kind == "exact":
        ok = _norm(answer) == _norm(check["value"])
        return ok, f"exact == {check['value']!r}"

    if kind == "regex":
        ok = re.search(check["pattern"], answer) is not None
        return ok, f"regex {check['pattern']!r}"

    if kind == "contains_all":
        missing = [v for v in check["values"] if _norm(v) not in _norm(answer)]
        return not missing, f"contains_all (missing: {missing})"

    if kind == "contains_any":
        ok = any(_norm(v) in _norm(answer) for v in check["values"])
        return ok, f"contains_any {check['values']}"

    if kind == "not_contains":
        if check.get("case_sensitive"):
            present = [v for v in check["values"] if v in answer]
        else:
            present = [v for v in check["values"] if _norm(v) in _norm(answer)]
        return not present, f"not_contains (present: {present})"

    if kind == "json_valid":
        try:
            json.loads(answer)
            return True, "json_valid"
        except (json.JSONDecodeError, ValueError):
            return False, "json_valid (parse failed)"

    if kind == "json_keys":
        try:
            obj = json.loads(answer)
        except (json.JSONDecodeError, ValueError):
            return False, "json_keys (parse failed)"
        if not isinstance(obj, dict):
            return False, "json_keys (not an object)"
        missing = [k for k in check["values"] if k not in obj]
        return not missing, f"json_keys (missing: {missing})"

    raise ValueError(f"Unknown check type: {kind!r}")


def grade(grader: list[dict[str, Any]], answer: str) -> tuple[bool, list[str]]:
    """Return (passed, per-check descriptions with pass/fail)."""
    results: list[str] = []
    passed = True
    for check in grader:
        ok, desc = _check(check, answer)
        results.append(f"{'PASS' if ok else 'FAIL'} {desc}")
        passed = passed and ok
    return passed, results
