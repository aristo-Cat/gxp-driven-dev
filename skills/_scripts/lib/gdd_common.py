"""gdd_common — shared helpers for gxp-driven-dev auxiliary scripts.

All scripts in skills/_scripts/ depend on this module. Stdlib + PyYAML only.
Target: Python 3.12+.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterator
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Canonical requirement ID: <DOC-TYPE>-<CATEGORY>-<NNN>
# DOC-TYPE is alpha (possibly with hyphen, e.g. RA-INIT, RA-DET)
# CATEGORY is one of the 22 canonical acronyms (alpha only)
# NNN is 3-digit number
REQUIREMENT_ID_RE = re.compile(
    r"\b(?P<doc>[A-Z]+(?:-[A-Z]+)?)-(?P<category>[A-Z]{2,8})-(?P<num>\d{3})\b"
)

# Marker pattern for AI agents to flag uncertainty
CLARIFICATION_MARKER_RE = re.compile(
    r"\[NEEDS CLARIFICATION:\s*(?P<question>[^\]]+)\]"
)

# Frontmatter delimiter
FRONTMATTER_DELIMITER = "---"


# ---------------------------------------------------------------------------
# Canonical category set (22) — from docs/requirement-id-scheme.md
# ---------------------------------------------------------------------------

CANONICAL_CATEGORIES: frozenset[str] = frozenset({
    "FUNC", "PERF", "QUAL", "TRAIN", "DEVENV",
    "DATA", "FLOW", "REPORT", "SEC", "PROC",
    "UI", "API", "MIGR", "ARCH", "OPS",
    "DOCS", "TEST", "DELIV", "PERIPH", "HW",
    "EREC", "ESIG",
})

# Middle tokens of CATEGORY-LESS ID schemes — NOT one of the 22 canonical
# categories. These arise from doc-types whose ID is `<DOC>-<NNN>` with a
# multi-part DOC (RA-INIT-001, RA-DET-001) or a fixed test marker
# (IQ-TC-001, OQ-TC-001, PQ-SCEN-001). The category-extraction regex would
# otherwise mis-segment them as phantom categories INIT / DET / TC / SCEN.
NON_CATEGORY_MIDDLES: frozenset[str] = frozenset({"INIT", "DET", "TC", "SCEN"})

# Banned categories (legacy corporate-origin codes) — flag if found
BANNED_CATEGORIES: frozenset[str] = frozenset({
    "FCT", "ARC", "DST", "END", "FLO", "GUI", "INT", "ORG",
    "PER", "QAL", "REP", "SUP", "SYO", "TRQ", "TST", "ER", "ES",
    "DEV", "DMI", "DOC",
})

# Canonical DOC-TYPE prefixes — flag unknown ones (warning, not error)
KNOWN_DOC_TYPES: frozenset[str] = frozenset({
    "VMP", "GXP-ASSESS", "VP", "SUP-ASSESS", "RA-INIT", "RA-DET",
    "URS", "FS", "CS", "DS", "API-SPEC", "DBS", "UC", "AC", "ADR",
    "IQ", "OQ", "PQ", "UT-PLAN", "IT-PLAN", "SEC-TEST", "PERF-TEST",
    "CR", "RTM", "VR", "RN", "DEPLOY-RUN",
    "PR", "CC", "IR", "CONFIG-BL", "UAR", "BRR",
    "DECOM-PLAN", "RETIRE-REPORT",
    "DPIA", "CYBER-RA", "AISC", "P11M", "SVP",
    "SOC-EVIDENCE", "SLA", "SHARED-RESP", "EXIT-PLAN",
})


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file.

    Returns (frontmatter_dict, body_text). If no frontmatter found, returns
    ({}, full_content).

    Raises FileNotFoundError if path does not exist.
    Raises yaml.YAMLError if frontmatter is malformed.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith(FRONTMATTER_DELIMITER):
        return {}, text

    end_idx = text.find(FRONTMATTER_DELIMITER, len(FRONTMATTER_DELIMITER))
    if end_idx == -1:
        return {}, text

    fm_block = text[len(FRONTMATTER_DELIMITER):end_idx].strip()
    body = text[end_idx + len(FRONTMATTER_DELIMITER):]

    frontmatter = yaml.safe_load(fm_block) or {}
    return frontmatter, body


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------


def find_manifest(start_dir: Path | None = None) -> Path | None:
    """Locate `.gxp-dev.yaml` by walking up from start_dir.

    Returns None if not found in any parent.
    """
    current = (start_dir or Path.cwd()).resolve()
    while True:
        candidate = current / ".gxp-dev.yaml"
        if candidate.exists():
            return candidate
        if current.parent == current:
            return None
        current = current.parent


def load_manifest(path: Path | None = None) -> dict:
    """Load `.gxp-dev.yaml` as a dict. Returns {} if not found."""
    manifest_path = path or find_manifest()
    if manifest_path is None or not manifest_path.exists():
        return {}
    return yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}


def find_active_templates(manifest: dict) -> list[str]:
    """Read `templates_active` from a manifest dict. Returns [] if absent."""
    active = manifest.get("templates_active", [])
    if not isinstance(active, list):
        return []
    return [str(t) for t in active]


# ---------------------------------------------------------------------------
# Spec walking
# ---------------------------------------------------------------------------


def walk_specs(specs_dir: Path) -> Iterator[Path]:
    """Yield `.md` files inside specs/ in canonical (sorted) order.

    Excludes `RTM.md` and any file starting with `_` (private).
    """
    if not specs_dir.is_dir():
        return
    for md_file in sorted(specs_dir.glob("*.md")):
        if md_file.name == "RTM.md" or md_file.name.startswith("_"):
            continue
        yield md_file


# ---------------------------------------------------------------------------
# Requirement ID extraction
# ---------------------------------------------------------------------------


def extract_requirement_ids(content: str) -> set[str]:
    """Extract all canonical requirement IDs from text.

    Returns a set of strings like {"URS-FUNC-001", "FS-API-002", ...}.
    """
    matches = REQUIREMENT_ID_RE.finditer(content)
    return {m.group(0) for m in matches}


def extract_categories_used(content: str) -> set[str]:
    """Extract the <CATEGORY> portion of all canonical requirement IDs in text.

    Excludes the middle tokens of category-less ID schemes (RA-INIT-/RA-DET- doc
    IDs, IQ-TC-/OQ-TC- test cases, PQ-SCEN- scenarios) — their middle segment is a
    doc-type continuation or a test marker, not one of the 22 canonical categories.
    """
    return {
        m.group("category")
        for m in REQUIREMENT_ID_RE.finditer(content)
        if m.group("category") not in NON_CATEGORY_MIDDLES
    }


# ---------------------------------------------------------------------------
# Clarification markers
# ---------------------------------------------------------------------------


def find_clarification_markers(path: Path) -> list[tuple[int, str]]:
    """Find all [NEEDS CLARIFICATION: ...] markers in a file.

    Returns list of (line_number, question) tuples, 1-indexed.
    """
    results: list[tuple[int, str]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for m in CLARIFICATION_MARKER_RE.finditer(line):
            results.append((i, m.group("question").strip()))
    return results


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def reconfigure_stdout_utf8() -> None:
    """On Windows, reconfigure stdout to utf-8 to allow emoji / unicode output."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
