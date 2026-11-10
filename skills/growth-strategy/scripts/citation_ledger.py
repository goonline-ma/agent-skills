#!/usr/bin/env python3
"""Lightweight Grounded Citation Ledger for Dossiers, Strategies, and Decks.

Prevents hallucinated URLs and renumbering drift by mapping retrieved URLs to stable [n] IDs.

Usage:
  python citation_ledger.py reset [--ledger path.json]
  python citation_ledger.py add <url> [--title "Source Title"] [--note "Key stat"]
  python citation_ledger.py list
  python citation_ledger.py render [--cited-in draft.md]
  python citation_ledger.py verify draft.md
"""
import argparse
import json
import os
import pathlib
import re
import sys
import tempfile
from urllib.parse import urlparse, urlunparse

DEFAULT_LEDGER = pathlib.Path(tempfile.gettempdir()) / "growth_citation_ledger.json"
CITE_RE = re.compile(r"\[(\d+)\]")


def normalize_url(u: str) -> str:
    p = urlparse(u.strip())
    path = p.path.rstrip("/") or "/"
    return urlunparse((p.scheme.lower(), p.netloc.lower(), path, p.params, p.query, ""))


def load_ledger(path: pathlib.Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"sources": []}


def save_ledger(path: pathlib.Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic URL -> [n] Citation Ledger")
    ap.add_argument("--ledger", default=os.environ.get("GROWTH_CITATION_LEDGER", str(DEFAULT_LEDGER)))
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("reset")

    pa = sub.add_parser("add")
    pa.add_argument("url")
    pa.add_argument("--title", default="")
    pa.add_argument("--note", default="")

    sub.add_parser("list")

    pr = sub.add_parser("render")
    pr.add_argument("--cited-in", default="")

    pv = sub.add_parser("verify")
    pv.add_argument("draft")

    args = ap.parse_args()
    lpath = pathlib.Path(args.ledger)

    if args.cmd == "reset":
        save_ledger(lpath, {"sources": []})
        print(f"Reset ledger at {lpath}")
        return 0

    data = load_ledger(lpath)
    sources = data["sources"]

    if args.cmd == "add":
        norm = normalize_url(args.url)
        for s in sources:
            if s["norm"] == norm:
                if args.title and not s.get("title"):
                    s["title"] = args.title
                if args.note:
                    s["note"] = args.note
                save_ledger(lpath, data)
                print(f"[{s['id']}]")
                return 0
        new_id = len(sources) + 1
        sources.append({"id": new_id, "url": args.url.strip(), "norm": norm, "title": args.title, "note": args.note})
        save_ledger(lpath, data)
        print(f"[{new_id}]")
        return 0

    if args.cmd == "list":
        print(json.dumps(sources, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "render":
        only_ids = None
        if args.cited_in:
            text = pathlib.Path(args.cited_in).read_text(encoding="utf-8")
            only_ids = {int(m) for m in CITE_RE.findall(text)}
        print("## Sources")
        for s in sources:
            if only_ids is not None and s["id"] not in only_ids:
                continue
            label = f"{s['title']} — {s['url']}" if s.get("title") else s["url"]
            print(f"- [{s['id']}] {label}")
        return 0

    if args.cmd == "verify":
        text = pathlib.Path(args.draft).read_text(encoding="utf-8")
        cited = sorted({int(m) for m in CITE_RE.findall(text)})
        known = {s["id"] for s in sources}
        unknown = [cid for cid in cited if cid not in known]
        if unknown:
            print(f"FAIL: unknown citation IDs in {args.draft}: {unknown}", file=sys.stderr)
            return 1
        print(f"PASS: {len(cited)} verified source IDs cited ({cited}).")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
