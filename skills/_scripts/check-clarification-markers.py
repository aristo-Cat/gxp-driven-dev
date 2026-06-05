#!/usr/bin/env python3
"""check-clarification-markers — find `[NEEDS CLARIFICATION:` markers in specs.

Spec instances may carry `[NEEDS CLARIFICATION: question]` markers when an AI
agent (or a human) could not resolve a placeholder at instantiation time. This
script grep-counts them and reports file + line + question.

A spec should not be promoted from `draft` to `in-review` while it still has
clarification markers.

Exit codes:
  0 = no markers found (spec is clean), OR markers found with --draft
  1 = markers found (without --draft)
  2 = file not found

Usage:
  python check-clarification-markers.py specs/URS.md
  python check-clarification-markers.py --all              # scans specs/*.md
  python check-clarification-markers.py --all --quiet      # exit code only
  python check-clarification-markers.py specs/URS.md --draft  # report but exit 0 (CI on drafts)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))
import gdd_common as gdd  # noqa: E402


def check_one(path: Path) -> list[tuple[int, str]]:
    if not path.exists():
        return []
    return gdd.find_clarification_markers(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "paths",
        type=Path,
        nargs="*",
        help="Spec files to check. Ignored if --all is given.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan all `specs/*.md` files in the consumer project",
    )
    parser.add_argument(
        "--specs-dir",
        type=Path,
        default=Path("specs"),
        help="Specs directory (default: specs/) — used with --all",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-marker output; only exit code matters",
    )
    parser.add_argument(
        "--draft",
        "--allow-markers",
        dest="draft",
        action="store_true",
        help=(
            "Draft mode: report markers but exit 0 (markers are expected in "
            "draft status). Use in CI to avoid failing on legitimate draft "
            "specs; run without this flag when gating promotion to in-review."
        ),
    )
    args = parser.parse_args()

    gdd.reconfigure_stdout_utf8()

    files_to_check: list[Path] = []
    if args.all:
        if not args.specs_dir.is_dir():
            print(f"FAIL specs dir not found: {args.specs_dir}", file=sys.stderr)
            return 2
        files_to_check = list(gdd.walk_specs(args.specs_dir))
    else:
        files_to_check = args.paths

    if not files_to_check:
        print("FAIL no files to check (provide path or use --all)", file=sys.stderr)
        return 2

    total_markers = 0
    for path in files_to_check:
        markers = check_one(path)
        if not markers:
            if not args.quiet:
                print(f"OK {path} — no clarification markers")
            continue
        total_markers += len(markers)
        if not args.quiet:
            print(f"FAIL {path} — {len(markers)} marker(s):")
            for line_no, question in markers:
                print(f"  L{line_no}: {question}")

    if total_markers == 0:
        if not args.quiet:
            print()
            print(f"OK All {len(files_to_check)} file(s) clean of clarification markers")
        return 0

    if not args.quiet:
        print()
        if args.draft:
            print(
                f"OK (draft) {total_markers} clarification marker(s) across "
                f"{len(files_to_check)} file(s) — expected in draft status"
            )
        else:
            print(f"FAIL {total_markers} clarification marker(s) across {len(files_to_check)} file(s)")
    return 0 if args.draft else 1


if __name__ == "__main__":
    sys.exit(main())
