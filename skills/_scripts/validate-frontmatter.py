#!/usr/bin/env python3
"""validate-frontmatter — verify a spec instance's frontmatter is coherent.

Checks:
  1. YAML frontmatter parses without error
  2. `type` field is "instance" (or "template" with --template-mode)
  3. `based_on_template` field matches the file's expected template
  4. `status` is one of: draft | in-review | approved | superseded
  5. If `status: approved`: `approved_by` is present
  6. `version` follows semver if status != draft
  7. Required fields per `instance_frontmatter_spec` of the source template
  8. No `[NEEDS CLARIFICATION: …]` markers in required fields when status > draft

Exit codes:
  0 = valid
  1 = validation error
  2 = file not found or parse error

Usage:
  python validate-frontmatter.py specs/URS.md
  python validate-frontmatter.py --dry-run templates/csv/URS.md   # validates the template
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add lib/ to path so we can import gdd_common
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))
import gdd_common as gdd  # noqa: E402

# Spec lifecycle: draft → in-review → approved → superseded.
# Test-protocol lifecycle (IQ/OQ/PQ) uses in-execution / executed instead of
# in-review (GAMP test-execution states). Both are accepted.
VALID_STATUSES = {
    "draft", "in-review", "approved", "superseded",
    "in-execution", "executed",
}
SEMVER_RE = gdd.re.compile(r"^\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9.-]+)?$")

# Templates live at <install>/templates/csv/ — siblings of skills/ in the install.
_TEMPLATES_DIR = _SCRIPT_DIR.parent.parent / "templates" / "csv"

# Fields validated by dedicated checks above — skip them in the spec-driven loop
# to avoid duplicate error messages.
_ALREADY_CHECKED = {"type", "based_on_template", "status", "version"}


def load_required_fields(based_on: str) -> tuple[list[tuple[str, object]], str | None]:
    """Read `instance_frontmatter_spec.required_fields` from the source template.

    Returns (fields, error). `fields` is a list of (field_name, expected_value|None)
    — expected_value is set only for spec entries written as `field: value`.
    `error` is a message if the template could not be located/parsed, else None.
    """
    template_path = _TEMPLATES_DIR / f"{based_on}.md"
    if not template_path.exists():
        return [], f"Source template not found for required-field check: {template_path}"
    try:
        frontmatter, _ = gdd.parse_frontmatter(template_path)
    except Exception as e:  # noqa: BLE001 — surfaced to the user as a validation error
        return [], f"Failed to parse source template {template_path}: {e}"

    spec = frontmatter.get("instance_frontmatter_spec") or {}
    raw = spec.get("required_fields") or []
    fields: list[tuple[str, object]] = []
    for item in raw:
        if isinstance(item, dict):
            for key, value in item.items():
                fields.append((str(key), value))
        else:
            fields.append((str(item), None))
    return fields, None


def validate(path: Path, dry_run: bool = False) -> tuple[bool, list[str]]:
    """Return (is_valid, list_of_errors)."""
    errors: list[str] = []

    if not path.exists():
        return False, [f"File not found: {path}"]

    try:
        frontmatter, body = gdd.parse_frontmatter(path)
    except Exception as e:
        return False, [f"Failed to parse frontmatter: {e}"]

    if not frontmatter:
        return False, ["No frontmatter found (must start with ---)"]

    # In dry-run mode, we validate a template itself (different rules)
    if dry_run:
        return _validate_template(frontmatter)

    # Instance mode
    file_type = frontmatter.get("type")
    if file_type != "instance":
        errors.append(f"Expected `type: instance`, got `{file_type}`")

    based_on = frontmatter.get("based_on_template")
    if not based_on:
        errors.append("Missing required field `based_on_template`")

    status = frontmatter.get("status")
    if status not in VALID_STATUSES:
        errors.append(
            f"Invalid `status: {status}`. Must be one of: {sorted(VALID_STATUSES)}"
        )

    version = frontmatter.get("version")
    if status and status != "draft":
        if not version:
            errors.append(f"`version` is required when status != draft (got status: {status})")
        elif not SEMVER_RE.match(str(version)):
            errors.append(f"`version` does not match semver: {version}")

    if status == "approved":
        approved_by = frontmatter.get("approved_by")
        if not approved_by:
            errors.append("`approved_by` is required when status == approved")

    # Required fields per the source template's instance_frontmatter_spec
    if based_on:
        required, load_err = load_required_fields(str(based_on))
        if load_err:
            errors.append(load_err)
        else:
            for field_name, expected in required:
                if field_name in _ALREADY_CHECKED:
                    continue
                value = frontmatter.get(field_name)
                if value is None or (isinstance(value, str) and not value.strip()):
                    errors.append(f"Missing required field per template spec: `{field_name}`")
                elif expected is not None and str(value) != str(expected):
                    errors.append(
                        f"Field `{field_name}` expected `{expected}`, got `{value}`"
                    )

    # Check for clarification markers in required fields when status > draft
    if status and status != "draft":
        markers = gdd.find_clarification_markers(path)
        if markers:
            for line_no, question in markers[:5]:  # cap output
                errors.append(
                    f"Unresolved [NEEDS CLARIFICATION] at line {line_no}: {question}"
                )
            if len(markers) > 5:
                errors.append(f"… and {len(markers) - 5} more clarification markers")

    return len(errors) == 0, errors


def _validate_template(frontmatter: dict) -> tuple[bool, list[str]]:
    """Validation rules for a template itself (--dry-run mode)."""
    errors: list[str] = []
    required = [
        "title", "type", "template_id", "template_version",
        "v_model_phase", "language",
    ]
    for field in required:
        if field not in frontmatter:
            errors.append(f"Template missing required field: `{field}`")

    if frontmatter.get("type") != "template":
        errors.append(f"Expected `type: template`, got `{frontmatter.get('type')}`")

    template_id = frontmatter.get("template_id", "")
    if not template_id or not template_id.replace("-", "").isalpha():
        errors.append(
            f"Invalid template_id: `{template_id}` (must be alpha-only, possibly with hyphens)"
        )

    return len(errors) == 0, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("path", type=Path, help="Spec instance or template to validate")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate a template (not an instance)",
    )
    args = parser.parse_args()

    gdd.reconfigure_stdout_utf8()

    is_valid, errors = validate(args.path, dry_run=args.dry_run)

    if is_valid:
        mode = "template" if args.dry_run else "instance"
        print(f"OK {args.path} — valid {mode} frontmatter")
        return 0

    print(f"FAIL {args.path}", file=sys.stderr)
    for err in errors:
        print(f"  - {err}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
