#!/usr/bin/env python3
"""Export the list + knowledge base as JSONL, ready to embed into a RAG index.

One JSON object per line. Two record kinds:

    {"kind": "project", ...}    one per entry in data/projects.yml
    {"kind": "knowledge", ...}  one per section of knowledge/*.md

Usage:
    python3 scripts/export_dataset.py            # write data/dataset.jsonl
    python3 scripts/export_dataset.py --check    # exit 1 if the file is stale
    python3 scripts/export_dataset.py --stats    # print a summary only

Chunking: knowledge documents are split on `## ` headings, and every chunk is
prefixed with the document title so it stays self-describing once embedded.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "projects.yml"
STARS = ROOT / "data" / "stars.json"
KB = ROOT / "knowledge"
OUT = ROOT / "data" / "dataset.jsonl"


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:  # pragma: no cover
        sys.exit("PyYAML is required: python3 -m pip install pyyaml")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def split_front_matter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        _, front, body = text.split("---", 2)
        return load_yaml_text(front), body.strip()
    return {}, text.strip()


def load_yaml_text(block: str) -> dict:
    import yaml

    return yaml.safe_load(block) or {}


def knowledge_records() -> list[dict]:
    records: list[dict] = []
    if not KB.exists():
        return records
    for path in sorted(KB.glob("*.md")):
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        title = meta.get("title") or path.stem
        chunks: list[tuple[str, str]] = []
        current_heading, current_lines = "", []
        for line in body.splitlines():
            if line.startswith("## "):
                chunks.append((current_heading, "\n".join(current_lines).strip()))
                current_heading, current_lines = line[3:].strip(), []
            else:
                current_lines.append(line)
        chunks.append((current_heading, "\n".join(current_lines).strip()))

        for idx, (heading, content) in enumerate(chunks):
            if not content:
                continue
            prefix = f"{title} — {heading}" if heading else title
            records.append(
                {
                    "id": f"knowledge:{path.stem}:{idx}",
                    "kind": "knowledge",
                    "doc": path.name,
                    "title": title,
                    "heading": heading or None,
                    "board": meta.get("board"),
                    "source": meta.get("source"),
                    "tags": meta.get("tags", []),
                    "retrieved": str(meta.get("retrieved", "")),
                    "provenance": "summary written from vendor documentation and hands-on checks",
                    "text": f"{prefix}\n\n{content}",
                }
            )
    return records


def project_records() -> list[dict]:
    data = load_yaml(DATA)
    stars = {}
    if STARS.exists():
        blob = json.loads(STARS.read_text(encoding="utf-8"))
        stars = blob.get("repos", {})
        snapshot = blob.get("snapshot")
    else:
        snapshot = None

    meta = data["meta"]
    section_titles = {s["id"]: s["en"] for s in data["sections"]}
    section_titles_zh = {s["id"]: s["zh"] for s in data["sections"]}

    records: list[dict] = []
    for p in data["projects"]:
        repo = p["repo"]
        records.append(
            {
                "id": f"project:{repo}",
                "kind": "project",
                "title": repo,
                "url": f"https://github.com/{repo}",
                "section": p["section"],
                "section_title": section_titles.get(p["section"]),
                "section_title_zh": section_titles_zh.get(p["section"]),
                "support": p.get("support"),
                "license": p.get("license"),
                "stars": stars.get(repo),
                "stars_snapshot": snapshot,
                "board": meta.get("board"),
                "compatible_with": meta.get("also_compatible"),
                "summary_en": p.get("en"),
                "summary_zh": p.get("zh"),
                "text": f"{repo}\n\n{p.get('zh')}\n\n{p.get('en')}",
            }
        )
    return records


def build() -> str:
    records = project_records() + knowledge_records()
    records.sort(key=lambda r: (r["kind"], r["id"]))
    lines = [json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    payload = build()

    if args.stats:
        records = [json.loads(line) for line in payload.splitlines()]
        kinds: dict[str, int] = {}
        for r in records:
            kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
        print("records:", len(records), "|", ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
        print("chars:", len(payload))
        return 0

    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != payload:
            print("dataset.jsonl is out of date. Run: python3 scripts/export_dataset.py")
            return 1
        print("dataset.jsonl is up to date.")
        return 0

    OUT.write_text(payload, encoding="utf-8")
    count = payload.count("\n")
    print(f"wrote {OUT.relative_to(ROOT)} — {count} records, {len(payload)} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
