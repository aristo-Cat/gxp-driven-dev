#!/usr/bin/env python3
"""anti-leak-guard — enforce the anonymization rule (see CLAUDE.md).

This toolkit is open-source and must never carry the identity of any organization a
contributor distilled it from: no source-organization name, internal document/ID codes,
site codes, or non-English heritage terms.

This guard ships as a GENERIC ENGINE. Organization-specific patterns are NOT baked in
(that would leak them in a public repo). They are supplied locally, never committed, via:
  - a git-ignored overlay file:  skills/_scripts/.leak-overlay.txt
  - or the LEAK_OVERLAY env var  (newline-separated; handy as a CI secret)
Each overlay line is `<regex>` or `<regex> || <reason>`. Lines starting with # are comments;
matching is case-insensitive.

With no overlay configured the guard still runs and exits 0 (so public CI stays green); it then
only catches the generic built-in patterns. Full protection comes from the local overlay plus a
pre-commit hook (the enforcing lock).

Exit codes:
  0 = clean
  1 = leak(s) found
  2 = setup error (root not found)

Usage:
  python anti-leak-guard.py                 # scan the toolkit root (parent of skills/)
  python anti-leak-guard.py --root <dir>
  python anti-leak-guard.py --quiet         # exit code only
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_OVERLAY_FILE = _SCRIPT_DIR / ".leak-overlay.txt"
_OVERLAY_DELIM = "||"

# Generic, organization-agnostic patterns that are safe to ship publicly.
# Add only patterns that name no specific organization. Org-specific terms go in the overlay.
BUILTIN_PATTERNS: list[tuple[re.Pattern[str], str]] = []

# Files the guard never scans: its own overlay (holds the secret patterns) and the
# git-ignored private journal. Everything else (incl. CLAUDE.md/AGENTS.md/STATE.md) is scanned.
SKIP_NAMES: frozenset[str] = frozenset({".leak-overlay.txt", "PROGRESS.md"})

SCAN_SUFFIXES: frozenset[str] = frozenset(
    {".md", ".py", ".yaml", ".yml", ".txt", ".json"}
)
SKIP_DIRS: frozenset[str] = frozenset(
    {".git", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache"}
)


def _parse_overlay_lines(lines: list[str]) -> list[tuple[re.Pattern[str], str]]:
    """Parse `<regex> || <reason>` overlay lines into compiled patterns."""
    patterns: list[tuple[re.Pattern[str], str]] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        regex, _, reason = line.partition(_OVERLAY_DELIM)
        regex = regex.strip()
        if not regex:
            continue
        try:
            patterns.append(
                (re.compile(regex, re.IGNORECASE), reason.strip() or "overlay pattern")
            )
        except re.error as exc:
            print(f"WARN skipping invalid overlay regex {regex!r}: {exc}", file=sys.stderr)
    return patterns


def load_patterns() -> list[tuple[re.Pattern[str], str]]:
    """Built-in generic patterns + organization-specific overlay (env var and/or file)."""
    patterns = list(BUILTIN_PATTERNS)
    env = os.environ.get("LEAK_OVERLAY")
    if env:
        patterns.extend(_parse_overlay_lines(env.splitlines()))
    if _OVERLAY_FILE.is_file():
        patterns.extend(
            _parse_overlay_lines(_OVERLAY_FILE.read_text(encoding="utf-8").splitlines())
        )
    return patterns


def scan_file(
    path: Path, patterns: list[tuple[re.Pattern[str], str]]
) -> list[tuple[int, str, str]]:
    """Return [(line_no, reason, snippet)] for each banned match in the file."""
    hits: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return hits
    for i, line in enumerate(text.splitlines(), start=1):
        for pattern, reason in patterns:
            if pattern.search(line):
                hits.append((i, reason, line.strip()[:120]))
    return hits


def iter_target_files(root: Path):
    """Yield content files under root, skipping skip-listed files + skip dirs."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix not in SCAN_SUFFIXES:
            continue
        if path.name in SKIP_NAMES:
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=_SCRIPT_DIR.parent.parent,  # toolkit root = parent of skills/
        help="Toolkit root to scan (default: the gxp-driven-dev root)",
    )
    parser.add_argument("--quiet", action="store_true", help="Exit code only")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    root = args.root.resolve()
    if not root.is_dir():
        print(f"FAIL root not found: {root}", file=sys.stderr)
        return 2

    patterns = load_patterns()
    overlay_note = (
        ""
        if patterns
        else " (no patterns configured — set LEAK_OVERLAY or add .leak-overlay.txt)"
    )

    total = 0
    scanned = 0
    for path in iter_target_files(root):
        scanned += 1
        hits = scan_file(path, patterns)
        if hits:
            total += len(hits)
            if not args.quiet:
                rel = path.relative_to(root)
                for line_no, reason, snippet in hits:
                    print(f"LEAK {rel}:{line_no} [{reason}] {snippet}")

    if total == 0:
        if not args.quiet:
            print(f"OK anti-leak-guard — {scanned} file(s) scanned, 0 leaks{overlay_note}")
        return 0

    if not args.quiet:
        print()
        print(
            f"FAIL anti-leak-guard — {total} leak(s) found across {scanned} scanned file(s)"
        )
        print("Fix the content. Org-specific patterns live in the git-ignored overlay, not in the repo.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
