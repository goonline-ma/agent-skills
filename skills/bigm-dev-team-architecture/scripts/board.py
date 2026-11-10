#!/usr/bin/env python3
"""GitHub Projects v2 & fresh PR verification helper for multi-agent swarms.

Usage:
  python board.py list [--org goonline-ma] [--project 1]
  python board.py status <issue#> "<Backlog|Ready|In progress|In review|Done>" [--org goonline-ma] [--project 1]
  python board.py comment <issue#> "<body_or_VERDICT>" [--org goonline-ma] [--repo <slug>]
  python board.py verify-pr <pr#> [--org goonline-ma] [--repo <slug>]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

DEFAULT_ORG = os.environ.get("GITHUB_ORG", "goonline-ma")
DEFAULT_PROJECT = os.environ.get("GITHUB_PROJECT_NUM", "1")


def find_gh() -> str:
    if os.environ.get("GH_BIN"):
        return os.environ["GH_BIN"]
    found = shutil.which("gh")
    if found:
        return found
    win_gh = "C:/Program Files/GitHub CLI/gh.exe"
    if os.path.exists(win_gh):
        return win_gh
    return "gh"


GH = find_gh()


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    r = subprocess.run(
        [GH, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    if check and r.returncode != 0:
        sys.exit(f"gh failed ({' '.join(args[:3])}): {r.stderr.strip()[:400]}")
    return r


def detect_repo_slug(org_override: str | None, repo_override: str | None) -> tuple[str, str]:
    if repo_override and "/" in repo_override:
        o, r = repo_override.split("/", 1)
        return o, r
    org = org_override or DEFAULT_ORG
    if repo_override:
        return org, repo_override
    try:
        rem = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if rem.returncode == 0:
            m = re.search(r"github\.com[:/]([^/]+)/([^/.]+?)(?:\.git)?$", rem.stdout.strip())
            if m:
                return m.group(1), m.group(2)
    except OSError:
        pass
    sys.exit("Specify --repo <slug> (or run inside a git clone with a GitHub origin remote).")


def cmd_list(org: str, project: str) -> None:
    items = json.loads(
        gh("project", "item-list", project, "--owner", org, "--limit", "200", "--format", "json").stdout
    ).get("items", [])
    for it in items:
        num = it.get("content", {}).get("number", "-")
        title = it.get("title", "")[:65]
        status = it.get("status", "Unset")
        print(f"#{num:<5} [{status:<12}] {title}")
    print(f"Total items: {len(items)}")


def cmd_status(num: int, status: str, org: str, project: str) -> None:
    pid = json.loads(gh("project", "view", project, "--owner", org, "--format", "json").stdout)["id"]
    fields = json.loads(
        gh("project", "field-list", project, "--owner", org, "--format", "json", "--limit", "50").stdout
    )["fields"]
    st = next((f for f in fields if f["name"] == "Status"), None)
    if not st:
        sys.exit(f"No 'Status' field found on project #{project} in {org}")
    opt = next((o["id"] for o in st.get("options", []) if o["name"].lower() == status.lower()), None)
    if not opt:
        sys.exit(f"Unknown status {status!r}; valid options: {[o['name'] for o in st.get('options', [])]}")
    items = json.loads(
        gh("project", "item-list", project, "--owner", org, "--limit", "300", "--format", "json").stdout
    ).get("items", [])
    item = next((i for i in items if i.get("content", {}).get("number") == int(num)), None)
    if not item:
        sys.exit(f"Issue #{num} is not attached to project #{project} in {org}")
    gh(
        "project", "item-edit",
        "--id", item["id"],
        "--project-id", pid,
        "--field-id", st["id"],
        "--single-select-option-id", opt,
    )
    print(f"UPDATED: #{num} -> {status}")


def cmd_comment(num: int, body: str, org: str | None, repo: str | None) -> None:
    o, r = detect_repo_slug(org, repo)
    gh("issue", "comment", str(num), "--repo", f"{o}/{r}", "--body", body)
    print(f"COMMENT_POSTED: {o}/{r}#{num}")


def cmd_verify_pr(pr_num: int, org: str | None, repo: str | None) -> None:
    o, r = detect_repo_slug(org, repo)
    meta = json.loads(
        gh("pr", "view", str(pr_num), "--repo", f"{o}/{r}", "--json", "state,mergeable,mergedAt,headRefName").stdout
    )
    checks = gh("pr", "checks", str(pr_num), "--repo", f"{o}/{r}", check=False)
    print(f"PR {o}/{r}#{pr_num}: state={meta.get('state')} mergeable={meta.get('mergeable')} mergedAt={meta.get('mergedAt')}")
    if checks.stdout.strip():
        print(checks.stdout.strip())
    if checks.returncode != 0 and meta.get("state") != "MERGED":
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="GitHub Projects v2 & PR gate helper")
    sub = ap.add_subparsers(dest="action", required=True)

    p_ls = sub.add_parser("list")
    p_ls.add_argument("--org", default=DEFAULT_ORG)
    p_ls.add_argument("--project", default=DEFAULT_PROJECT)

    p_st = sub.add_parser("status")
    p_st.add_argument("issue", type=int)
    p_st.add_argument("value")
    p_st.add_argument("--org", default=DEFAULT_ORG)
    p_st.add_argument("--project", default=DEFAULT_PROJECT)

    p_cm = sub.add_parser("comment")
    p_cm.add_argument("issue", type=int)
    p_cm.add_argument("value")
    p_cm.add_argument("--org", default=None)
    p_cm.add_argument("--repo", default=None)

    p_pr = sub.add_parser("verify-pr")
    p_pr.add_argument("pr", type=int)
    p_pr.add_argument("--org", default=None)
    p_pr.add_argument("--repo", default=None)

    a = ap.parse_args()
    if a.action == "list":
        cmd_list(a.org, a.project)
    elif a.action == "status":
        cmd_status(a.issue, a.value, a.org, a.project)
    elif a.action == "comment":
        cmd_comment(a.issue, a.value, a.org, a.repo)
    elif a.action == "verify-pr":
        cmd_verify_pr(a.pr, a.org, a.repo)


if __name__ == "__main__":
    main()
