#!/usr/bin/env python3
"""Validate guardrail invariants in examples/scoring-cases.yaml.

This is intentionally a tiny parser for this repository's simple YAML shape,
not a general YAML implementation and not a scoring engine.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent.parent
CASES_FILE = ROOT_DIR / "examples" / "scoring-cases.yaml"
ALLOWED_BUCKETS = {"Precise", "Balanced", "Recall", "Exclude"}
EXCLUDE_CONSTRAINTS = {"contradicted", "out_of_scope"}


def parse_scalar(value: str):
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def split_key_value(line: str, line_number: int) -> tuple[str, object]:
    key, sep, value = line.partition(":")
    if not sep:
        raise ValueError(f"Line {line_number}: expected key/value pair")
    return key.strip(), parse_scalar(value.strip())


def parse_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    current: dict | None = None
    section: str | None = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue

        if raw_line.startswith("  - "):
            current = {}
            cases.append(current)
            section = None
            key, value = split_key_value(raw_line[4:], line_number)
            current[key] = value
            continue

        if current is None:
            continue

        if raw_line.startswith("    ") and not raw_line.startswith("      "):
            key, value = split_key_value(raw_line[4:], line_number)
            if value == "":
                current[key] = {}
                section = key
            else:
                current[key] = value
                section = None
            continue

        if raw_line.startswith("      ") and section:
            key, value = split_key_value(raw_line[6:], line_number)
            current[section][key] = value
            continue

        raise ValueError(f"Line {line_number}: unsupported YAML shape")

    return cases


def clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(value, upper))


def require(condition: bool, errors: list[str], case_id: object, message: str) -> None:
    if not condition:
        errors.append(f"{case_id}: {message}")


def validate_case(case: dict) -> list[str]:
    errors: list[str] = []
    case_id = case.get("id", "<missing id>")

    base_score = case.get("base_score")
    external_adjustment = case.get("external_adjustment")
    final_score = case.get("final_score")
    expected_bucket = case.get("expected_bucket")
    expected_bucket_not = case.get("expected_bucket_not")
    hard_conflict = case.get("hard_conflict")
    constraint_status = case.get("constraint_status")

    require(isinstance(base_score, dict), errors, case_id, "base_score must be a mapping")
    if isinstance(base_score, dict):
        base_values = list(base_score.values())
        require(
            all(isinstance(value, int) for value in base_values),
            errors,
            case_id,
            "base_score components must be integers",
        )
        base_total = sum(value for value in base_values if isinstance(value, int))
        require(0 <= base_total <= 100, errors, case_id, f"base_score total must be 0..100, got {base_total}")
    else:
        base_total = 0

    require(
        isinstance(external_adjustment, int) and -15 <= external_adjustment <= 15,
        errors,
        case_id,
        f"external_adjustment must be -15..15, got {external_adjustment}",
    )
    require(
        isinstance(final_score, int) and 0 <= final_score <= 100,
        errors,
        case_id,
        f"final_score must be 0..100, got {final_score}",
    )

    if isinstance(external_adjustment, int) and isinstance(final_score, int):
        expected_final = clamp(base_total + external_adjustment, 0, 100)
        require(
            final_score == expected_final,
            errors,
            case_id,
            f"final_score must equal clamp(base_score + external_adjustment, 0, 100): expected {expected_final}, got {final_score}",
        )

    require(expected_bucket in ALLOWED_BUCKETS, errors, case_id, f"expected_bucket must be one of {sorted(ALLOWED_BUCKETS)}")

    if hard_conflict is True:
        require(expected_bucket == "Exclude", errors, case_id, "hard_conflict true must have expected_bucket Exclude")

    if constraint_status in EXCLUDE_CONSTRAINTS:
        require(
            expected_bucket == "Exclude",
            errors,
            case_id,
            f"constraint_status {constraint_status} must have expected_bucket Exclude",
        )

    if base_total < 70:
        require(expected_bucket != "Precise", errors, case_id, "base_score below 70 must not be Precise")

    if expected_bucket_not is not None:
        require(
            expected_bucket != expected_bucket_not,
            errors,
            case_id,
            "expected_bucket must not equal expected_bucket_not",
        )

    return errors


def main() -> int:
    if not CASES_FILE.exists():
        print(f"Missing scoring cases file: {CASES_FILE}", file=sys.stderr)
        return 1

    try:
        cases = parse_cases(CASES_FILE)
    except ValueError as exc:
        print(f"Failed to parse {CASES_FILE}: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if not cases:
        errors.append("No cases found")

    for case in cases:
        errors.extend(validate_case(case))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"Scoring case guardrail check failed: {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Scoring case guardrail check passed: {len(cases)} case(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
