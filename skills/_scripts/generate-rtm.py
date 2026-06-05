#!/usr/bin/env python3
"""generate-rtm — derive Requirements Traceability Matrix from specs/*.md.

Walks every spec file in `specs/`, extracts canonical requirement IDs
(<DOC-TYPE>-<CATEGORY>-<NNN>), follows cross-references between files, and
writes a derived `specs/RTM.md` with an upstream→downstream matrix.

The RTM is regenerated on every run — do not hand-edit `specs/RTM.md`.

Exit codes:
  0 = RTM generated successfully
  1 = no specs found
  2 = malformed spec (cannot extract IDs)

Usage:
  python generate-rtm.py
  python generate-rtm.py --specs-dir specs --output specs/RTM.md
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR / "lib"))
import gdd_common as gdd  # noqa: E402


def collect_ids(specs_dir: Path) -> dict[str, dict]:
    """Walk specs/ and return {spec_filename: {own_ids, referenced_ids}}.

    own_ids = IDs declared in this file's DOC-TYPE (e.g. URS.md owns URS-* IDs)
    referenced_ids = IDs of OTHER documents that this file references
    """
    by_file: dict[str, dict] = {}
    for spec_path in gdd.walk_specs(specs_dir):
        frontmatter, body = gdd.parse_frontmatter(spec_path)
        own_doc_type = frontmatter.get("template_id") or frontmatter.get("based_on_template")

        all_ids = gdd.extract_requirement_ids(body)
        own_ids: set[str] = set()
        ref_ids: set[str] = set()

        if own_doc_type:
            # IDs that start with the own DOC-TYPE prefix
            for rid in all_ids:
                if rid.startswith(f"{own_doc_type}-"):
                    own_ids.add(rid)
                else:
                    ref_ids.add(rid)
        else:
            ref_ids = all_ids

        by_file[spec_path.name] = {
            "doc_type": own_doc_type or "?",
            "own_ids": own_ids,
            "referenced_ids": ref_ids,
            "body": body,
        }
    return by_file


def build_forward_trace(by_file: dict[str, dict]) -> dict[str, set[str]]:
    """For each upstream ID, find the downstream IDs that reference it ON THE SAME ROW.

    Precise (row-scoped) traceability: a downstream ID is linked to an upstream ID
    only when both appear on the same line — i.e. the same markdown table row
    (e.g. `| RA-DET-001 | URS-FUNC-003 | RA-INIT-001 | … |` links RA-DET-001 from
    URS-FUNC-003 and RA-INIT-001). This avoids the cartesian file-level product
    that would otherwise link every referenced ID to every owned ID in the file.

    Returns {upstream_id: {downstream_ids…}}.
    """
    trace: dict[str, set[str]] = defaultdict(set)
    for info in by_file.values():
        own_doc = info["doc_type"]
        if own_doc == "?":
            continue
        prefix = f"{own_doc}-"
        for line in info["body"].splitlines():
            ids = gdd.extract_requirement_ids(line)
            if len(ids) < 2:
                continue
            own_on_row = {rid for rid in ids if rid.startswith(prefix)}
            refs_on_row = ids - own_on_row
            for ref_id in refs_on_row:
                for own_id in own_on_row:
                    trace[ref_id].add(own_id)
    return dict(trace)


def find_orphans(by_file: dict[str, dict]) -> dict[str, list[str]]:
    """Find IDs that have no forward or backward trace.

    Returns {orphan_type: [ids]} where types are:
      - "no_downstream": owned ID never referenced by any other doc
      - "dangling_reference": referenced ID that no file owns
    """
    all_own: set[str] = set()
    all_referenced: set[str] = set()
    for info in by_file.values():
        all_own |= info["own_ids"]
        all_referenced |= info["referenced_ids"]

    return {
        "no_downstream": sorted(all_own - all_referenced),
        "dangling_reference": sorted(all_referenced - all_own),
    }


def render_rtm(by_file: dict[str, dict], trace: dict[str, set[str]],
               orphans: dict[str, list[str]]) -> str:
    """Render the RTM as Markdown."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    parts: list[str] = []
    parts.append("---")
    parts.append("title: Requirements Traceability Matrix (derived)")
    parts.append("type: derived")
    parts.append("generator: skills/_scripts/generate-rtm.py")
    parts.append(f"generated_at: \"{now}\"")
    parts.append("status: auto-generated")
    parts.append("---")
    parts.append("")
    parts.append("# Requirements Traceability Matrix (RTM)")
    parts.append("")
    parts.append("> ⚙ This file is **derived automatically** from `specs/*.md` by `skills/_scripts/generate-rtm.py`. **Do not hand-edit** — re-run the generator instead.")
    parts.append("")
    parts.append(f"**Generated at**: `{now}`")
    parts.append("")

    # ─── Summary ───
    parts.append("## Summary")
    parts.append("")
    parts.append(f"- Spec files scanned: **{len(by_file)}**")
    total_ids = sum(len(info["own_ids"]) for info in by_file.values())
    parts.append(f"- Total requirement IDs declared: **{total_ids}**")
    total_traces = sum(len(downstream) for downstream in trace.values())
    parts.append(f"- Forward-trace links: **{total_traces}**")
    parts.append(f"- IDs without downstream: **{len(orphans['no_downstream'])}**")
    parts.append(f"- Dangling references: **{len(orphans['dangling_reference'])}**")
    parts.append("")

    # ─── Per-file IDs ───
    parts.append("## Requirement IDs per spec file")
    parts.append("")
    parts.append("| Spec file | DOC-TYPE | Own IDs | References others |")
    parts.append("|---|---|---:|---:|")
    for fname in sorted(by_file):
        info = by_file[fname]
        parts.append(
            f"| `{fname}` | {info['doc_type']} | {len(info['own_ids'])} | {len(info['referenced_ids'])} |"
        )
    parts.append("")

    # ─── Forward trace ───
    parts.append("## Forward traceability (upstream → downstream)")
    parts.append("")
    if not trace:
        parts.append("_No forward traces found yet (project may be in early specification phase)._")
    else:
        parts.append("| Upstream ID | Downstream IDs |")
        parts.append("|---|---|")
        for upstream in sorted(trace):
            downstreams = sorted(trace[upstream])
            ds_str = ", ".join(f"`{d}`" for d in downstreams)
            parts.append(f"| `{upstream}` | {ds_str} |")
    parts.append("")

    # ─── Orphans ───
    parts.append("## Gaps and orphans")
    parts.append("")

    if orphans["no_downstream"]:
        parts.append("### IDs with no downstream reference")
        parts.append("")
        parts.append("These requirements are declared but never referenced by any downstream document. This is acceptable for:")
        parts.append("- Requirements at the **last layer** of the V-Model (e.g. `PQ-*` IDs)")
        parts.append("- Requirements marked `GxP=N` (out of scope of formal validation)")
        parts.append("")
        parts.append("Investigate if these IDs should have downstream consumers:")
        parts.append("")
        for orphan_id in orphans["no_downstream"][:50]:
            parts.append(f"- `{orphan_id}`")
        if len(orphans["no_downstream"]) > 50:
            parts.append(f"- … and {len(orphans['no_downstream']) - 50} more")
        parts.append("")

    if orphans["dangling_reference"]:
        parts.append("### Dangling references (referenced but not declared)")
        parts.append("")
        parts.append("⚠ These IDs are referenced by some spec file but no file declares them. **This is a bug** — fix before promoting any spec to `approved`.")
        parts.append("")
        for dangling in orphans["dangling_reference"][:50]:
            parts.append(f"- `{dangling}`")
        if len(orphans["dangling_reference"]) > 50:
            parts.append(f"- … and {len(orphans['dangling_reference']) - 50} more")
        parts.append("")

    if not orphans["no_downstream"] and not orphans["dangling_reference"]:
        parts.append("✅ No orphans or dangling references detected.")
        parts.append("")

    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--specs-dir",
        type=Path,
        default=Path("specs"),
        help="Directory containing spec instance files (default: specs/)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path for RTM.md (default: <specs-dir>/RTM.md)",
    )
    args = parser.parse_args()

    gdd.reconfigure_stdout_utf8()

    specs_dir = args.specs_dir
    if not specs_dir.is_dir():
        print(f"FAIL specs directory not found: {specs_dir}", file=sys.stderr)
        return 1

    output_path = args.output or (specs_dir / "RTM.md")

    by_file = collect_ids(specs_dir)
    if not by_file:
        print(f"FAIL no spec files found in {specs_dir}", file=sys.stderr)
        return 1

    trace = build_forward_trace(by_file)
    orphans = find_orphans(by_file)
    rtm_content = render_rtm(by_file, trace, orphans)

    output_path.write_text(rtm_content, encoding="utf-8")
    print(f"OK RTM written to {output_path}")
    print(f"   {len(by_file)} spec files, "
          f"{sum(len(i['own_ids']) for i in by_file.values())} IDs, "
          f"{len(orphans['dangling_reference'])} dangling refs")

    return 0 if not orphans["dangling_reference"] else 2


if __name__ == "__main__":
    sys.exit(main())
