#!/usr/bin/env python3
"""Execute a T1 Critical Task using Claude Sonnet 5.5 or Claude Opus 5.5 with strict cost & secret guardrails.

Usage:
  # Critical implementation / RLS / security fix (tries unmetered `agy` claude-sonnet-5-5-high first, then Nous):
  python claude_critical_run.py <prompt_file> --tier sonnet [--cwd <repo_clone>]

  # Critical architecture / P0 deadlock / flagship strategy (calls anthropic/claude-opus-5.5 via Nous/OpenRouter):
  python claude_critical_run.py <prompt_file> --tier opus [--out <output_file>]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


def candidate_agy_bins() -> list[Path]:
    home = Path.home()
    local_app = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
    return [
        local_app / "agy" / "bin" / "agy.exe",
        local_app / "agy" / "bin" / "agy.cmd",
        home / ".local" / "bin" / "agy",
        Path("/usr/local/bin/agy"),
    ]


def candidate_env_files() -> list[Path]:
    home = Path.home()
    local_app = Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local"))
    return [
        local_app / "hermes" / ".env",
        local_app / "hermes" / "profiles" / "coo" / ".env",
        home / ".hermes" / ".env",
    ]


def load_env_keys() -> dict[str, str]:
    keys: dict[str, str] = {}
    for env_path in candidate_env_files():
        if env_path.is_file():
            for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    keys[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("NOUS_API_KEY", "OPENROUTER_API_KEY"):
        if os.environ.get(k):
            keys[k] = os.environ[k]
    return keys


def check_no_secrets(cwd: str) -> str | None:
    skip = {".git", "node_modules", ".next", "dist", "build", ".venv", "venv"}
    for root, dirs, files in os.walk(cwd):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in files:
            if f.startswith(".env") and f not in (".env.example", ".env.sample", ".env.template"):
                return f"Refused: secret-bearing file found in working directory: {os.path.join(root, f)}"
    return None


def find_agy() -> str | None:
    found = shutil.which("agy")
    if found:
        return found
    for p in candidate_agy_bins():
        if p.exists():
            return str(p)
    return None


def run_agy_sonnet(prompt_file: str, cwd: str, timeout_min: int) -> tuple[bool, str]:
    err = check_no_secrets(cwd)
    if err:
        print(f"CRITICAL_REFUSED: {err}", file=sys.stderr)
        sys.exit(3)
    agy = find_agy()
    if not agy:
        return False, "agy binary not found"
    rel = os.path.relpath(os.path.abspath(prompt_file), cwd).replace("\\", "/")
    prompt = (
        f"Read {rel} and implement the critical requirement exactly. "
        "Do not read/print .env files or commit/push; leave changes in the working tree for review."
    )
    try:
        p = subprocess.run(
            [
                agy, "--model", "claude-sonnet-5-5-high",
                "--dangerously-skip-permissions",
                "--print-timeout", f"{timeout_min}m",
                "--print", prompt,
            ],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=(timeout_min + 2) * 60,
        )
        if p.returncode == 0:
            return True, p.stdout
        return False, f"exit {p.returncode}"
    except Exception as e:
        return False, str(e)


def call_api(model_id: str, prompt_text: str, keys: dict[str, str]) -> str:
    # Always prioritize `nous` first so Anthropic prompt caching stays active!
    endpoints: list[tuple[str, str, str]] = []
    if keys.get("NOUS_API_KEY"):
        endpoints.append(("nous", "https://inference-api.nousresearch.com/v1/chat/completions", keys["NOUS_API_KEY"]))
    if keys.get("OPENROUTER_API_KEY"):
        endpoints.append(("openrouter", "https://openrouter.ai/api/v1/chat/completions", keys["OPENROUTER_API_KEY"]))
    if not endpoints:
        raise RuntimeError("Neither NOUS_API_KEY nor OPENROUTER_API_KEY found in environment or local config.")

    last_err = None
    for prov, url, api_key in endpoints:
        body = json.dumps({
            "model": model_id,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a T1 Critical Principal Engineer. Deliver exact, production-hardened "
                        "SQL/TypeScript/architecture output with zero placeholders or mock logic."
                    ),
                },
                {"role": "user", "content": prompt_text},
            ],
            "temperature": 0.1,
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                usage = data.get("usage", {})
                cached = (
                    usage.get("cache_read_input_tokens")
                    or usage.get("prompt_tokens_details", {}).get("cached_tokens", 0)
                )
                content = data["choices"][0]["message"]["content"]
                print(
                    f"[CRITICAL_OK] provider={prov} model={model_id} cached_tokens={cached} usage={json.dumps(usage)}",
                    file=sys.stderr,
                )
                return content
        except Exception as e:
            last_err = f"{prov}: {e}"
    raise RuntimeError(f"All critical endpoints failed: {last_err}")


def main() -> None:
    ap = argparse.ArgumentParser(description="T1 Critical Claude Sonnet/Opus runner with cost & secret gates")
    ap.add_argument("prompt_file", help="Path to markdown prompt file describing the critical task")
    ap.add_argument("--tier", choices=["sonnet", "opus"], default="sonnet")
    ap.add_argument("--cwd", default=".", help="Working directory for code execution (sonnet agy route)")
    ap.add_argument("--out", default=None, help="Optional file path to write the response")
    ap.add_argument("--timeout-min", type=int, default=20)
    args = ap.parse_args()

    pfile = Path(args.prompt_file)
    if not pfile.is_file():
        sys.exit(f"Prompt file not found: {args.prompt_file}")

    prompt_text = pfile.read_text(encoding="utf-8")

    if args.tier == "sonnet":
        ok, info = run_agy_sonnet(args.prompt_file, os.path.abspath(args.cwd), args.timeout_min)
        if ok:
            print("[CRITICAL_OK] route=agy model=claude-sonnet-5-5-high (unmetered)", file=sys.stderr)
            if args.out:
                Path(args.out).write_text(info, encoding="utf-8")
            else:
                print(info)
            return
        print(f"[INFO] agy claude-sonnet-5-5-high unavailable ({info}), falling back to API...", file=sys.stderr)
        model_id = "anthropic/claude-sonnet-5.5"
    else:
        model_id = "anthropic/claude-opus-5.5"

    keys = load_env_keys()
    result = call_api(model_id, prompt_text, keys)
    if args.out:
        Path(args.out).write_text(result, encoding="utf-8")
    else:
        print(result)


if __name__ == "__main__":
    main()
