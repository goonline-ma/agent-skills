#!/usr/bin/env python3
"""Interactive & CLI selective installer for GoOnline Agent Skills & Swarm Agents.

Supports:
  - Google Antigravity (~/.gemini/config/{skills,agents} or .agents/{skills,agents})
  - Claude Code        (~/.claude/{skills,agents} or .claude/{skills,agents})
  - Hermes Agent       ($LOCALAPPDATA/hermes/profiles/<profile>/skills/goonline or ~/.hermes/...)
  - Universal .agents  (~/.agents/{skills,agents} or .agents/{skills,agents} for Cursor/Codex/Windsurf)

Modes:
  1. AI-Harness Discovery & Catalog (used by INSTALL.md multi-step flow):
       python scripts/install.py --detect --json
       python scripts/install.py --catalog --json

  2. Deterministic Selective Install (called by AI harness after multi-step Q&A):
       python scripts/install.py --harness antigravity --scope global \
         --skills growth-strategy --agents growth,ledger

  3. Interactive Human Terminal Wizard (when run in an interactive TTY with no install flags):
       python scripts/install.py

  4. Inspect or Uninstall:
       python scripts/install.py --list-installed [--harness all]
       python scripts/install.py --uninstall --harness antigravity --scope global --agents datum,synapse
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
AGENTS_DIR = REPO_ROOT / "agents"

HARNESS_CHOICES = ("antigravity", "claude-code", "hermes", "universal")

PRESETS: dict[str, dict[str, Any]] = {
    "full": {
        "label": "Full Agency & Engineering Suite",
        "description": "All skills + all 10 specialist swarm agents.",
        "skills": ["*"],
        "agents": ["*"],
    },
    "engineering": {
        "label": "Engineering Swarm & Figma UX/UI",
        "description": "Multi-agent software architecture, Figma design systems, DB/RLS, QA & Cloudflare.",
        "skills": ["bigm-dev-team-architecture"],
        "agents": ["cto", "pixel", "forge-fe", "forge-be", "datum", "synapse", "bastion", "veritas"],
    },
    "marketing": {
        "label": "Digital Strategy, SEO/GEO & Growth",
        "description": "GTM, pitch decks, SEO/GEO citability, CRO, outbound ABM, paid media & FinOps.",
        "skills": ["growth-strategy"],
        "agents": ["growth", "ledger"],
    },
    "ux-frontend": {
        "label": "UX/UI Figma & Frontend Delivery",
        "description": "Figma-to-code design systems, CRO/landing architecture, frontend build & visual QA.",
        "skills": ["bigm-dev-team-architecture", "growth-strategy"],
        "agents": ["pixel", "forge-fe", "veritas"],
    },
    "skills-only": {
        "label": "Master Skills Only (Zero Extra Agents)",
        "description": "Install the low-token skill routers without adding custom subagent personas.",
        "skills": ["*"],
        "agents": [],
    },
}

HERMES_SHORT_DESCRIPTIONS: dict[str, str] = {
    "growth-strategy": "Digital strategy, GTM, decks, SEO/GEO, CRO, ABM, and loops.",
    "bigm-dev-team-architecture": "CTO multi-agent swarm OS: Figma UX, RLS, QA, and Cloudflare.",
}


def parse_frontmatter(md_path: Path) -> tuple[dict[str, Any], str]:
    raw = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.S)
    if not m:
        return {}, raw
    fm_text, body = m.group(1), m.group(2)
    meta: dict[str, Any] = {}
    for line in fm_text.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    meta["_raw_frontmatter"] = fm_text
    return meta, body


def discover_catalog() -> dict[str, Any]:
    skills = []
    if SKILLS_DIR.is_dir():
        for sdir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()):
            meta, _ = parse_frontmatter(sdir / "SKILL.md")
            fm_len = len(meta.get("_raw_frontmatter", ""))
            refs = sorted(p.name for p in (sdir / "references").glob("*.md")) if (sdir / "references").is_dir() else []
            scripts = (
                sorted(p.name for p in (sdir / "scripts").iterdir() if p.is_file())
                if (sdir / "scripts").is_dir()
                else []
            )
            skills.append({
                "name": sdir.name,
                "description": meta.get("description", ""),
                "idle_tokens": max(1, round(fm_len / 4)),
                "references_count": len(refs),
                "scripts": scripts,
            })

    agents = []
    if AGENTS_DIR.is_dir():
        for amd in sorted(AGENTS_DIR.glob("*.md")):
            meta, _ = parse_frontmatter(amd)
            desc = meta.get("description", "")
            line_cost = len(f"- {amd.stem}: {desc}")
            agents.append({
                "name": amd.stem,
                "model": meta.get("model", "inherit"),
                "description": desc,
                "idle_tokens": max(1, round(line_cost / 4)),
            })

    return {"presets": PRESETS, "skills": skills, "agents": agents}


def get_hermes_root() -> Path:
    home = Path.home()
    if os.name == "nt":
        local_app = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
        win_path = local_app / "hermes"
        if win_path.exists() or not (home / ".hermes").exists():
            return win_path
    return home / ".hermes"


def detect_environment(workspace_dir: Path) -> dict[str, Any]:
    home = Path.home()
    agy_bin = shutil.which("agy") or str(
        Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local")) / "agy" / "bin" / "agy.exe"
    )
    has_agy = bool(shutil.which("agy") or Path(agy_bin).is_file() or (home / ".gemini" / "config").is_dir())
    has_claude = bool(shutil.which("claude") or (home / ".claude").is_dir())
    hermes_root = get_hermes_root()
    has_hermes = bool(shutil.which("hermes") or hermes_root.is_dir())
    hermes_profiles = (
        sorted(p.name for p in (hermes_root / "profiles").iterdir() if p.is_dir())
        if (hermes_root / "profiles").is_dir()
        else []
    )
    has_universal = (home / ".agents").is_dir() or (workspace_dir / ".agents").is_dir()

    detected = []
    if has_agy:
        detected.append("antigravity")
    if has_claude:
        detected.append("claude-code")
    if has_hermes:
        detected.append("hermes")
    if has_universal or not detected:
        detected.append("universal")

    return {
        "os": os.name,
        "workspace_dir": str(workspace_dir),
        "is_git_repo": (workspace_dir / ".git").exists(),
        "detected_harnesses": detected,
        "harnesses": {
            "antigravity": {
                "detected": has_agy,
                "global_skills": str(home / ".gemini" / "config" / "skills"),
                "global_agents": str(home / ".gemini" / "config" / "agents"),
                "workspace_skills": str(workspace_dir / ".agents" / "skills"),
                "workspace_agents": str(workspace_dir / ".agents" / "agents"),
            },
            "claude-code": {
                "detected": has_claude,
                "global_skills": str(home / ".claude" / "skills"),
                "global_agents": str(home / ".claude" / "agents"),
                "workspace_skills": str(workspace_dir / ".claude" / "skills"),
                "workspace_agents": str(workspace_dir / ".claude" / "agents"),
            },
            "hermes": {
                "detected": has_hermes,
                "root": str(hermes_root),
                "profiles": hermes_profiles,
            },
            "universal": {
                "detected": has_universal,
                "global_skills": str(home / ".agents" / "skills"),
                "global_agents": str(home / ".agents" / "agents"),
                "workspace_skills": str(workspace_dir / ".agents" / "skills"),
                "workspace_agents": str(workspace_dir / ".agents" / "agents"),
            },
        },
    }


def resolve_targets(
    harness: str,
    scope: str,
    workspace_dir: Path,
    hermes_profiles: list[str],
) -> list[tuple[str, Path, Path | None]]:
    """Return list of (target_label, skills_dir, agents_dir_or_None)."""
    home = Path.home()
    if harness == "antigravity":
        if scope == "global":
            base = home / ".gemini" / "config"
        else:
            base = workspace_dir / ".agents"
        return [(f"antigravity ({scope})", base / "skills", base / "agents")]

    if harness == "claude-code":
        base = (home / ".claude") if scope == "global" else (workspace_dir / ".claude")
        return [(f"claude-code ({scope})", base / "skills", base / "agents")]

    if harness == "hermes":
        hroot = get_hermes_root()
        profs = hermes_profiles or ["default"]
        out = []
        for pr in profs:
            pbase = hroot / "profiles" / pr
            out.append((f"hermes (profile:{pr})", pbase / "skills" / "goonline", pbase / "agents"))
        return out

    if harness == "universal":
        base = (home / ".agents") if scope == "global" else (workspace_dir / ".agents")
        return [(f"universal ({scope})", base / "skills", base / "agents")]

    raise ValueError(f"Unsupported harness: {harness}")


def adapt_skill_for_hermes(skill_name: str, skill_md_path: Path) -> None:
    meta, body = parse_frontmatter(skill_md_path)
    short_desc = HERMES_SHORT_DESCRIPTIONS.get(skill_name)
    if not short_desc:
        raw_desc = meta.get("description", "GoOnline production skill.")
        short_desc = (raw_desc[:56].rstrip(" .,;:") + ".") if len(raw_desc) > 60 else raw_desc
        if not short_desc.endswith("."):
            short_desc = short_desc[:59] + "."
    hermes_fm = (
        f"---\n"
        f"name: {skill_name}\n"
        f'description: "{short_desc}"\n'
        f"version: 2.0.0\n"
        f"license: MIT\n"
        f"platforms: [linux, macos, windows]\n"
        f"---\n"
    )
    skill_md_path.write_text(hermes_fm + body, encoding="utf-8")


def adapt_agent_content(harness: str, src_md: Path, claude_volume_model: str) -> str:
    raw = src_md.read_text(encoding="utf-8")
    if harness != "claude-code":
        return raw
    meta, body = parse_frontmatter(src_md)
    name = meta.get("name", src_md.stem)
    desc = meta.get("description", "")
    agy_model = meta.get("model", "inherit")
    cc_model = claude_volume_model if agy_model == "flash" else "inherit"
    return f'---\nname: {name}\ndescription: "{desc}"\nmodel: {cc_model}\n---\n{body}'


def parse_csv_selection(val: str | None, valid_names: list[str]) -> list[str]:
    if val is None:
        return []
    cleaned = val.strip()
    if not cleaned or cleaned.lower() == "none":
        return []
    if cleaned.lower() in ("all", "*"):
        return list(valid_names)
    picked = []
    for item in [x.strip() for x in cleaned.split(",") if x.strip()]:
        if item not in valid_names:
            sys.exit(f"ERROR: Unknown item '{item}'. Available: {', '.join(valid_names)}")
        if item not in picked:
            picked.append(item)
    return picked


def execute_install(
    harnesses: list[str],
    scope: str,
    skills: list[str],
    agents: list[str],
    workspace_dir: Path,
    hermes_profiles: list[str],
    claude_volume_model: str,
    dry_run: bool,
    uninstall: bool,
) -> dict[str, Any]:
    catalog = discover_catalog()
    skill_tokens = {s["name"]: s["idle_tokens"] for s in catalog["skills"]}
    agent_tokens = {a["name"]: a["idle_tokens"] for a in catalog["agents"]}

    actions: list[dict[str, str]] = []
    for h in harnesses:
        for label, s_dst_root, a_dst_root in resolve_targets(h, scope, workspace_dir, hermes_profiles):
            for sname in skills:
                src = SKILLS_DIR / sname
                dst = s_dst_root / sname
                if uninstall:
                    if dst.exists():
                        if not dry_run:
                            shutil.rmtree(dst)
                        actions.append({"target": label, "kind": "skill", "name": sname, "op": "removed", "path": str(dst)})
                else:
                    if not dry_run:
                        s_dst_root.mkdir(parents=True, exist_ok=True)
                        if dst.exists():
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
                        if h == "hermes":
                            adapt_skill_for_hermes(sname, dst / "SKILL.md")
                    actions.append({"target": label, "kind": "skill", "name": sname, "op": "installed", "path": str(dst)})

            if a_dst_root is not None:
                for aname in agents:
                    src_md = AGENTS_DIR / f"{aname}.md"
                    dst_md = a_dst_root / f"{aname}.md"
                    if uninstall:
                        if dst_md.exists():
                            if not dry_run:
                                dst_md.unlink()
                            actions.append({"target": label, "kind": "agent", "name": aname, "op": "removed", "path": str(dst_md)})
                    else:
                        if not dry_run:
                            a_dst_root.mkdir(parents=True, exist_ok=True)
                            rendered = adapt_agent_content(h, src_md, claude_volume_model)
                            dst_md.write_text(rendered, encoding="utf-8")
                        actions.append({"target": label, "kind": "agent", "name": aname, "op": "installed", "path": str(dst_md)})

    est_tokens = sum(skill_tokens.get(s, 0) for s in skills) + sum(agent_tokens.get(a, 0) for a in agents)
    return {
        "dry_run": dry_run,
        "operation": "uninstall" if uninstall else "install",
        "harnesses": harnesses,
        "scope": scope,
        "skills": skills,
        "agents": agents,
        "estimated_idle_tokens_per_harness": est_tokens,
        "actions": actions,
    }


def list_installed(workspace_dir: Path) -> dict[str, Any]:
    catalog = discover_catalog()
    known_skills = {s["name"] for s in catalog["skills"]}
    known_agents = {a["name"] for a in catalog["agents"]}
    env = detect_environment(workspace_dir)
    report: dict[str, Any] = {}

    for h in ("antigravity", "claude-code", "universal"):
        info = env["harnesses"][h]
        found_s_g = sorted(p.name for p in Path(info["global_skills"]).iterdir() if p.name in known_skills) if Path(info["global_skills"]).is_dir() else []
        found_a_g = sorted(p.stem for p in Path(info["global_agents"]).glob("*.md") if p.stem in known_agents) if Path(info["global_agents"]).is_dir() else []
        found_s_w = sorted(p.name for p in Path(info["workspace_skills"]).iterdir() if p.name in known_skills) if Path(info["workspace_skills"]).is_dir() else []
        found_a_w = sorted(p.stem for p in Path(info["workspace_agents"]).glob("*.md") if p.stem in known_agents) if Path(info["workspace_agents"]).is_dir() else []
        if any((found_s_g, found_a_g, found_s_w, found_a_w)):
            report[h] = {
                "global": {"skills": found_s_g, "agents": found_a_g},
                "workspace": {"skills": found_s_w, "agents": found_a_w},
            }

    hroot = Path(env["harnesses"]["hermes"]["root"])
    if (hroot / "profiles").is_dir():
        hermes_found = {}
        for pr in env["harnesses"]["hermes"]["profiles"]:
            s_found = []
            for sub in ("goonline", "bigm-operations"):
                sp = hroot / "profiles" / pr / "skills" / sub
                if sp.is_dir():
                    s_found.extend(p.name for p in sp.iterdir() if p.name in known_skills)
            ap = hroot / "profiles" / pr / "agents"
            a_found = sorted(p.stem for p in ap.glob("*.md") if p.stem in known_agents) if ap.is_dir() else []
            if s_found or a_found:
                hermes_found[pr] = {"skills": sorted(set(s_found)), "agents": a_found}
        if hermes_found:
            report["hermes"] = hermes_found

    return report


NON_TTY_GUIDE = (
    "INTERACTIVE_HARNESS_REQUIRED: Non-interactive stdin detected.\n"
    "If you are an AI agent (Antigravity, Claude Code, Hermes Agent, Cursor, Codex):\n"
    "  1. Run `python scripts/install.py --detect --json` and `python scripts/install.py --catalog --json`.\n"
    "  2. Follow INSTALL.md to prompt the user via your native multi-step question tool "
    "(`ask_question`, `AskUserQuestion`, or `clarify`) so they choose only the skills/agents they need.\n"
    "  3. Re-run `python scripts/install.py --harness <...> --scope <...> --skills <...> --agents <...>`."
)


def prompt_line(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        ans = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        sys.exit(NON_TTY_GUIDE)
    return ans if ans else default


def prompt_indices(prompt: str, options: list[tuple[str, str]], default_indices: list[int], allow_empty: bool = False) -> list[str]:
    print(f"\n{prompt}")
    for idx, (key, desc) in enumerate(options, 1):
        mark = "*" if idx in default_indices else " "
        print(f"  [{mark}] {idx}. {key:<28} {desc}")
    default_str = ",".join(str(i) for i in default_indices) if default_indices else ("none" if allow_empty else "1")
    while True:
        raw = prompt_line("Enter numbers (comma-separated, 'all', or 'none')", default_str).lower()
        if raw == "all":
            return [k for k, _ in options]
        if raw == "none" and allow_empty:
            return []
        try:
            nums = [int(x.strip()) for x in raw.split(",") if x.strip()]
            if nums and all(1 <= n <= len(options) for n in nums):
                out = []
                for n in nums:
                    k = options[n - 1][0]
                    if k not in out:
                        out.append(k)
                return out
        except ValueError:
            pass
        print(f"  Please enter numbers between 1 and {len(options)}, 'all'" + (", or 'none'." if allow_empty else "."))


def run_interactive_wizard(workspace_dir: Path) -> int:
    env = detect_environment(workspace_dir)
    catalog = discover_catalog()
    all_skills = [s["name"] for s in catalog["skills"]]
    all_agents = [a["name"] for a in catalog["agents"]]

    print("=" * 72)
    print("  GoOnline.ma — Interactive Agent Skills & Swarm Installer")
    print("=" * 72)

    # Step 1: Target Harness(es)
    h_opts = []
    def_h = []
    for idx, h in enumerate(HARNESS_CHOICES, 1):
        det = env["harnesses"][h]["detected"]
        tag = "(detected)" if det else ""
        h_opts.append((h, tag))
        if det and h != "universal":
            def_h.append(idx)
    if not def_h:
        def_h = [1]
    harnesses = prompt_indices("Step 1/4 — Select target AI harness(es):", h_opts, def_h)

    # Step 2: Scope (+ Hermes profiles if chosen)
    scope = "global"
    if any(h != "hermes" for h in harnesses):
        s_choice = prompt_indices(
            "Step 2/4 — Choose installation scope:",
            [
                ("global", "User-level config (available across all projects)"),
                ("workspace", f"Project-scoped VCS config inside {workspace_dir}"),
            ],
            [1],
        )
        scope = s_choice[0]

    hermes_profiles: list[str] = []
    if "hermes" in harnesses:
        known_profs = env["harnesses"]["hermes"]["profiles"] or ["default"]
        p_opts = [(p, "Hermes profile") for p in known_profs]
        hermes_profiles = prompt_indices("Step 2b — Select Hermes profile(s) to equip:", p_opts, [1])

    # Step 3: Preset vs Custom Multi-Select
    preset_items = [(k, f"{v['label']} — {v['description']}") for k, v in PRESETS.items()]
    preset_items.append(("custom", "Custom Multi-Select — pick exact individual skills and agents"))
    chosen_preset = prompt_indices("Step 3/4 — Choose a role bundle or Custom Multi-Select:", preset_items, [len(preset_items)])[0]

    if chosen_preset == "custom":
        s_opts = [(s["name"], f"(~{s['idle_tokens']} tok) {s['description'][:72]}") for s in catalog["skills"]]
        picked_skills = prompt_indices("Step 3a — Select Skills to install:", s_opts, list(range(1, len(s_opts) + 1)), allow_empty=True)

        a_opts = [(a["name"], f"[{a['model']:<7} ~{a['idle_tokens']} tok] {a['description'][:62]}") for a in catalog["agents"]]
        picked_agents = prompt_indices("Step 3b — Select Swarm Agents to install:", a_opts, [1, 8, 10], allow_empty=True)
    else:
        pdef = PRESETS[chosen_preset]
        picked_skills = all_skills if pdef["skills"] == ["*"] else list(pdef["skills"])
        picked_agents = all_agents if pdef["agents"] == ["*"] else list(pdef["agents"])

    if not picked_skills and not picked_agents:
        print("\nNothing selected. Exiting without changes.")
        return 0

    # Step 4: Preview & Confirm
    preview = execute_install(
        harnesses=harnesses,
        scope=scope,
        skills=picked_skills,
        agents=picked_agents,
        workspace_dir=workspace_dir,
        hermes_profiles=hermes_profiles,
        claude_volume_model="sonnet",
        dry_run=True,
        uninstall=False,
    )
    print("\nStep 4/4 — Installation Summary")
    print(f"  Harnesses : {', '.join(harnesses)} (scope: {scope})")
    print(f"  Skills    : {', '.join(picked_skills) if picked_skills else '(none)'}")
    print(f"  Agents    : {', '.join(picked_agents) if picked_agents else '(none)'}")
    print(f"  Footprint : ~{preview['estimated_idle_tokens_per_harness']} idle tokens/turn")
    confirm = prompt_line("Proceed with installation? (y/n)", "y").lower()
    if not confirm.startswith("y"):
        print("Cancelled.")
        return 0

    res = execute_install(
        harnesses=harnesses,
        scope=scope,
        skills=picked_skills,
        agents=picked_agents,
        workspace_dir=workspace_dir,
        hermes_profiles=hermes_profiles,
        claude_volume_model="sonnet",
        dry_run=False,
        uninstall=False,
    )
    print_receipt(res)
    return 0


def print_receipt(res: dict[str, Any]) -> None:
    verb = "DRY-RUN" if res["dry_run"] else ("UNINSTALLED" if res["operation"] == "uninstall" else "INSTALLED")
    print(f"\n[{verb}] {len(res['actions'])} item(s) | ~{res['estimated_idle_tokens_per_harness']} idle tokens/turn per harness")
    for act in res["actions"]:
        print(f"  - [{act['target']}] {act['kind']:<5} {act['name']:<28} -> {act['path']}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Selective multi-harness installer for GoOnline Skills & Agents")
    ap.add_argument("--detect", action="store_true", help="Detect installed AI harnesses and target paths")
    ap.add_argument("--catalog", action="store_true", help="Print available presets, skills, and agents")
    ap.add_argument("--list-installed", action="store_true", help="List currently installed GoOnline skills and agents")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON output")
    ap.add_argument("--harness", default=None, help="Comma-separated: antigravity,claude-code,hermes,universal")
    ap.add_argument("--scope", choices=["global", "workspace"], default="global")
    ap.add_argument("--workspace-dir", default=".", help="Target workspace directory when --scope workspace")
    ap.add_argument("--hermes-profile", default="default", help="Comma-separated Hermes profile names (default: default)")
    ap.add_argument("--preset", choices=list(PRESETS.keys()), default=None, help="Named bundle preset")
    ap.add_argument("--skills", default=None, help="Comma-separated skill names, 'all', or 'none'")
    ap.add_argument("--agents", default=None, help="Comma-separated agent names, 'all', or 'none'")
    ap.add_argument("--claude-volume-model", choices=["sonnet", "haiku", "inherit"], default="sonnet")
    ap.add_argument("--dry-run", action="store_true", help="Preview actions and token cost without writing files")
    ap.add_argument("--uninstall", action="store_true", help="Remove the specified skills/agents from target harness")
    args = ap.parse_args()

    ws = Path(args.workspace_dir).resolve()

    if args.detect:
        data = detect_environment(ws)
        print(json.dumps(data, indent=2) if args.json else json.dumps(data, indent=2))
        return

    if args.catalog:
        data = discover_catalog()
        print(json.dumps(data, indent=2) if args.json else json.dumps(data, indent=2))
        return

    if args.list_installed:
        data = list_installed(ws)
        print(json.dumps(data, indent=2))
        return

    # If no installation flags were passed, run interactive TTY wizard—or guide non-TTY AI harnesses!
    if not any((args.harness, args.preset, args.skills is not None, args.agents is not None)):
        if not sys.stdin.isatty():
            sys.exit(NON_TTY_GUIDE)
        sys.exit(run_interactive_wizard(ws))

    catalog = discover_catalog()
    valid_skills = [s["name"] for s in catalog["skills"]]
    valid_agents = [a["name"] for a in catalog["agents"]]

    if not args.harness:
        env = detect_environment(ws)
        harnesses = [h for h in env["detected_harnesses"] if h != "universal"] or ["universal"]
    else:
        harnesses = parse_csv_selection(args.harness, list(HARNESS_CHOICES))

    if args.preset:
        pdef = PRESETS[args.preset]
        skills = valid_skills if pdef["skills"] == ["*"] else list(pdef["skills"])
        agents = valid_agents if pdef["agents"] == ["*"] else list(pdef["agents"])
    else:
        skills = []
        agents = []

    if args.skills is not None:
        skills = parse_csv_selection(args.skills, valid_skills)
    if args.agents is not None:
        agents = parse_csv_selection(args.agents, valid_agents)

    if not skills and not agents:
        sys.exit("Nothing selected to install/uninstall. Pass --preset <name> or --skills / --agents.")

    h_profiles = [p.strip() for p in args.hermes_profile.split(",") if p.strip()]
    res = execute_install(
        harnesses=harnesses,
        scope=args.scope,
        skills=skills,
        agents=agents,
        workspace_dir=ws,
        hermes_profiles=h_profiles,
        claude_volume_model=args.claude_volume_model,
        dry_run=args.dry_run,
        uninstall=args.uninstall,
    )
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print_receipt(res)


if __name__ == "__main__":
    main()
