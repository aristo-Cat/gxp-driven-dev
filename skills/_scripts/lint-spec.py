#!/usr/bin/env python3
"""lint-spec — wrapper running frontmatter + clarification + RTM dry-run checks.

Combines the 3 main lints in one pass:
  1. validate-frontmatter.py on each target
  2. check-clarification-markers.py on each target
  3. generate-rtm.py in dry-run mode (no file written, only reports gaps)

Exit codes:
  0 = all checks pass
  1 = one or more checks failed
  2 = setup error (file/dir not found)

Usage:
  python lint-spec.py specs/URS.md
  python lint-spec.py --all
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))
import gdd_common as gdd  # noqa: E402

VALIDATE_SCRIPT = _SCRIPT_DIR / "validate-frontmatter.py"
CHECK_MARKERS_SCRIPT = _SCRIPT_DIR / "check-clarification-markers.py"
GENERATE_RTM_SCRIPT = _SCRIPT_DIR / "generate-rtm.py"


def run_check(name: str, cmd: list[str]) -> tuple[bool, str]:
    """Run a subprocess. Return (success, captured_output)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        output = result.stdout + result.stderr
        return result.returncode == 0, output
    except Exception as e:
        return False, f"Exception running {name}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "paths", type=Path, nargs="*", help="Spec files to lint (ignored with --all)"
    )
    parser.add_argument(
        "--all", action="store_true", help="Lint every specs/*.md"
    )
    parser.add_argument(
        "--specs-dir", type=Path, default=Path("specs"),
        help="Specs directory (default: specs/)"
    )
    parser.add_argument(
        "--skip-rtm", action="store_true",
        help="Skip the RTM dry-run check (faster for single-file lint)"
    )
    args = parser.parse_args()

    gdd.reconfigure_stdout_utf8()

    files_to_check: list[Path]
    if args.all:
        if not args.specs_dir.is_dir():
            print(f"FAIL specs dir not found: {args.specs_dir}", file=sys.stderr)
            return 2
        files_to_check = list(gdd.walk_specs(args.specs_dir))
    else:
        files_to_check = args.paths

    if not files_to_check:
        print("FAIL no files to lint (provide path or use --all)", file=sys.stderr)
        return 2

    overall_pass = True

    print("=" * 60)
    print(f"lint-spec — {len(files_to_check)} file(s)")
    print("=" * 60)

    # Step 1: validate-frontmatter on each file
    print("\n[1/3] Frontmatter validation")
    print("-" * 60)
    for path in files_to_check:
        ok, output = run_check(
            "validate-frontmatter",
            [sys.executable, str(VALIDATE_SCRIPT), str(path)],
        )
        if ok:
            print(f"  OK {path.name}")
        else:
            overall_pass = False
            print(f"  FAIL {path.name}")
            for line in output.strip().splitlines():
                print(f"     {line}")

    # Step 2: check-clarification-markers on each file
    print("\n[2/3] Clarification markers")
    print("-" * 60)
    for path in files_to_check:
        ok, output = run_check(
            "check-clarification-markers",
            [sys.executable, str(CHECK_MARKERS_SCRIPT), str(path), "--quiet"],
        )
        if ok:
            print(f"  OK {path.name}")
        else:
            overall_pass = False
            # Re-run non-quiet to get detail
            _, detail = run_check(
                "check-clarification-markers",
                [sys.executable, str(CHECK_MARKERS_SCRIPT), str(path)],
            )
            print(f"  FAIL {path.name}")
            for line in detail.strip().splitlines():
                print(f"     {line}")

    # Step 3: RTM dry-run (optional)
    if not args.skip_rtm and args.all:
        print("\n[3/3] RTM coherence (dry-run)")
        print("-" * 60)
        ok, output = run_check(
            "generate-rtm",
            [sys.executable, str(GENERATE_RTM_SCRIPT), "--specs-dir", str(args.specs_dir)],
        )
        for line in output.strip().splitlines():
            print(f"  {line}")
        if not ok:
            overall_pass = False
    else:
        print("\n[3/3] RTM coherence — SKIPPED (use --all to enable)")

    print()
    print("=" * 60)
    if overall_pass:
        print(f"OK lint-spec passed for {len(files_to_check)} file(s)")
        return 0
    print(f"FAIL lint-spec failed — review errors above")
    return 1


if __name__ == "__main__":
    sys.exit(main())
