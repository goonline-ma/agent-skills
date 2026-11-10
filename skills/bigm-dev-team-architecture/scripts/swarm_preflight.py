#!/usr/bin/env python3
"""Deterministic multi-agent swarm preflight & secret scanner.

Subcommands:
  python swarm_preflight.py wave-template [--out wave.json]
  python swarm_preflight.py check-overlap <wave.json>
  python swarm_preflight.py scan-secrets [target_dir]
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".next", ".nuxt", ".svelte-kit",
    ".venv", "venv", "__pycache__", ".turbo", ".cache", "coverage",
}

SECRET_PATTERNS = [
    ("Private Key Block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PRIVATE )?PRIVATE KEY-----")),
    ("Anthropic API Key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("OpenAI API Key", re.compile(r"\bsk-(?:proj|live)-[A-Za-z0-9_-]{20,}\b")),
    ("Stripe Live Key", re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{20,}\b")),
    ("GitHub PAT", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{25,}\b")),
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Supabase Service Role Assignment", re.compile(r"SUPABASE_SERVICE_ROLE_KEY\s*=\s*['\"]?eyJ[A-Za-z0-9_-]{20,}")),
    ("Hardcoded Windows User Path", re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9 _.-]+\\")),
]

SAMPLE_WAVE = {
    "wave": "M1-parallel-features",
    "tasks": [
        {
            "id": "issue-12-catalog-ui",
            "agent": "forge-fe",
            "branch": "feat/12-catalog-ui",
            "owned_globs": ["apps/web/src/features/catalog/**", "apps/web/src/app/(app)/catalog/**"],
        },
        {
            "id": "issue-13-orders-ui",
            "agent": "forge-fe",
            "branch": "feat/13-orders-ui",
            "owned_globs": ["apps/web/src/features/orders/**", "apps/web/src/app/(app)/orders/**"],
        },
        {
            "id": "issue-14-orders-api",
            "agent": "forge-be",
            "branch": "feat/14-orders-api",
            "owned_globs": ["packages/api/src/orders/**", "supabase/migrations/2026111001_orders.sql"],
        },
    ],
}


def norm_glob(g: str) -> str:
    return g.strip().replace("\\", "/").lstrip("./")


def glob_prefix(g: str) -> str:
    ng = norm_glob(g)
    for idx, ch in enumerate(ng):
        if ch in "*?[":
            return ng[:idx].rstrip("/")
    return ng.rstrip("/")


def globs_overlap(a: str, b: str) -> bool:
    na, nb = norm_glob(a), norm_glob(b)
    if na == nb:
        return True
    if fnmatch.fnmatchcase(na, nb) or fnmatch.fnmatchcase(nb, na):
        return True
    pa, pb = glob_prefix(na), glob_prefix(nb)
    if not pa or not pb:
        return True
    is_wild_a = any(c in na for c in "*?[")
    is_wild_b = any(c in nb for c in "*?[")
    if pa == pb and (is_wild_a or is_wild_b):
        return True
    if is_wild_a and (pb == pa or pb.startswith(pa + "/")):
        return True
    if is_wild_b and (pa == pb or pa.startswith(pb + "/")):
        return True
    return False


def cmd_wave_template(out_path: str | None) -> int:
    text = json.dumps(SAMPLE_WAVE, indent=2) + "\n"
    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")
        print(f"Wrote wave template to {out_path}")
    else:
        print(text, end="")
    return 0


def cmd_check_overlap(manifest_path: str) -> int:
    p = Path(manifest_path)
    if not p.is_file():
        sys.exit(f"ERROR: Wave manifest not found: {manifest_path}")
    data = json.loads(p.read_text(encoding="utf-8"))
    tasks = data.get("tasks", data if isinstance(data, list) else [])
    if not tasks:
        sys.exit("ERROR: Wave manifest contains zero tasks.")

    conflicts: list[str] = []
    seen_branches: dict[str, str] = {}
    for i, t1 in enumerate(tasks):
        tid1 = t1.get("id") or f"task-{i}"
        br1 = t1.get("branch")
        if br1:
            if br1 in seen_branches:
                conflicts.append(f"Duplicate branch '{br1}' shared by {seen_branches[br1]} and {tid1}")
            seen_branches[br1] = tid1
        g1_list = t1.get("owned_globs") or t1.get("globs") or []
        if not g1_list:
            conflicts.append(f"Task '{tid1}' has empty owned_globs (unbounded write scope).")
        for j in range(i + 1, len(tasks)):
            t2 = tasks[j]
            tid2 = t2.get("id") or f"task-{j}"
            g2_list = t2.get("owned_globs") or t2.get("globs") or []
            for ga in g1_list:
                for gb in g2_list:
                    if globs_overlap(ga, gb):
                        conflicts.append(f"Overlap between '{tid1}' ({ga}) and '{tid2}' ({gb})")

    if conflicts:
        print("OVERLAP_CHECK: FAIL")
        for c in conflicts:
            print(f"  - {c}")
        return 1

    print(f"OVERLAP_CHECK: PASS ({len(tasks)} parallel tasks, 0 file-boundary collisions)")
    return 0


def cmd_scan_secrets(target: str) -> int:
    root_path = Path(target).resolve()
    if not root_path.exists():
        sys.exit(f"ERROR: Path does not exist: {target}")

    findings: list[str] = []
    scanned = 0
    self_path = Path(__file__).resolve()

    files_to_check: list[Path] = []
    if root_path.is_file():
        files_to_check.append(root_path)
    else:
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                fp = Path(dirpath) / fn
                if fp.resolve() == self_path:
                    continue
                if fn.startswith(".env") and fn not in (".env.example", ".env.sample", ".env.template"):
                    findings.append(f"{fp.relative_to(root_path)}: Prohibited env file present ({fn})")
                    continue
                files_to_check.append(fp)

    text_exts = {
        ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".md", ".py",
        ".sql", ".yml", ".yaml", ".toml", ".html", ".css", ".sh", ".ps1", ".env",
    }
    for fp in files_to_check:
        if fp.suffix.lower() not in text_exts and fp.name not in ("Dockerfile",):
            continue
        try:
            if fp.stat().st_size > 2 * 1024 * 1024:
                continue
            content = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        scanned += 1
        rel = fp.relative_to(root_path) if root_path.is_dir() else fp.name
        for lineno, line in enumerate(content.splitlines(), 1):
            if "gitleaks:allow" in line or "scan-secrets:allow" in line:
                continue
            for label, rx in SECRET_PATTERNS:
                if rx.search(line):
                    findings.append(f"{rel}:{lineno}: {label}")

    if findings:
        print(f"SECRET_SCAN: FAIL ({len(findings)} finding(s) across {scanned} files)")
        for f in findings[:30]:
            print(f"  - {f}")
        return 1

    print(f"SECRET_SCAN: PASS ({scanned} files scanned, 0 leaks)")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Swarm file-boundary & secret preflight validator")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_tpl = sub.add_parser("wave-template", help="Print or write a sample wave manifest JSON")
    p_tpl.add_argument("--out", default=None)

    p_ov = sub.add_parser("check-overlap", help="Verify parallel tasks have disjoint owned_globs")
    p_ov.add_argument("manifest", help="Path to wave JSON manifest")

    p_sc = sub.add_parser("scan-secrets", help="Scan directory for leaked secrets or hardcoded user paths")
    p_sc.add_argument("target", nargs="?", default=".")

    args = ap.parse_args()
    if args.cmd == "wave-template":
        sys.exit(cmd_wave_template(args.out))
    elif args.cmd == "check-overlap":
        sys.exit(cmd_check_overlap(args.manifest))
    elif args.cmd == "scan-secrets":
        sys.exit(cmd_scan_secrets(args.target))


if __name__ == "__main__":
    main()
