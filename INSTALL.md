# Agent-Executable Interactive Installation Guide (`INSTALL.md`)

> **For Human Users — One-Prompt Interactive Setup**
> Paste this single instruction into **Google Antigravity**, **Claude Code**, **Hermes Agent**, **Cursor**, **Codex**, or **Windsurf**:
>
> ```text
> Read https://raw.githubusercontent.com/goonline-ma/agent-skills/main/INSTALL.md and walk me through installing only the GoOnline skills and agents I need.
> ```
>
> *(Prefer a terminal wizard instead? Clone the repo and run `python scripts/install.py`.)*

---

## Instructions for the AI Agent Harness (Mandatory Protocol)

You are executing the interactive installer for **`goonline-ma/agent-skills`**. **NEVER install every skill and agent blindly.** Your job is to keep the user's context window lean by running a **multi-step interactive interview** using your harness's native question UI, then invoking `scripts/install.py` deterministically with only the user's chosen components.

### Which Native Question Tool to Use

| Your Harness | Required Interactive Question Tool | Fallback Rule |
| :--- | :--- | :--- |
| **Google Antigravity** | **`ask_question`** (`questions` array, `is_multi_select`, `(Recommended)` first option) | Never ask plain-text walls when `ask_question` is available. |
| **Claude Code** | **`AskUserQuestion`** (`questions` with `multiSelect: true` where applicable) | Wait for structured answers before running Step 4. |
| **Hermes Agent** | **`clarify`** tool (or concise numbered prompt per step) | Wait for user reply before running Step 4. |
| **Cursor / Codex / Windsurf** | Built-in multiple-choice question tool if exposed; otherwise numbered conversational steps | Pause after each step and wait for the user's selection. |

---

### Step 0 — Silent Preflight & Environment Detection

1. If you are not already inside a clone of `goonline-ma/agent-skills`, clone it shallowly to a temporary directory:
   ```bash
   git clone --depth 1 https://github.com/goonline-ma/agent-skills.git <temp_dir>/goonline-agent-skills
   ```
2. Run both discovery commands silently to inspect the host machine and current live catalog:
   ```bash
   python scripts/install.py --detect --json
   python scripts/install.py --catalog --json
   ```
3. Note which harnesses (`antigravity`, `claude-code`, `hermes`, `universal`) have `"detected": true`, whether the current working directory is a Git project (`is_git_repo`), and any discovered Hermes `profiles`.

---

### Step 1 — Round 1 Interview: Target Harness, Scope & Track

Ask the user these **3 structured questions** first (pre-marking the harness you are currently running in—plus any detected harnesses—as `(Recommended)`):

1. **Target Harness(es)** (`is_multi_select: true`):
   - `(Recommended) <Current/Detected Harness>` *(e.g., `Google Antigravity`, `Claude Code`, `Hermes Agent`, or `Universal .agents/ for Cursor & Codex`)*
   - List the remaining supported harnesses (`antigravity`, `claude-code`, `hermes`, `universal`) so multi-tool users can equip several harnesses in one pass.
2. **Installation Scope** (`is_multi_select: false`):
   - `(Recommended) Global user config` — available across every project on this machine (`~/.gemini/config/`, `~/.claude/`, or Hermes profile)
   - `Workspace / Project only` — committed inside this repository (`.agents/` or `.claude/`) so teammates share the exact setup
3. **Setup Mode / Track** (`is_multi_select: false`):
   - `(Recommended) Custom Pick — let me choose exact individual skills & agents in Step 2`
   - `Engineering Swarm & Figma UX/UI Preset` (`bigm-dev-team-architecture` + `cto`, `pixel`, `forge-fe`, `forge-be`, `datum`, `synapse`, `bastion`, `veritas` — `~383` idle tok)
   - `Digital Strategy, SEO/GEO & Growth Preset` (`growth-strategy` + `growth`, `ledger` — `~135` idle tok)
   - `UX/UI Figma & Frontend Preset` (`bigm-dev-team-architecture`, `growth-strategy` + `pixel`, `forge-fe`, `veritas` — `~231` idle tok)
   - `Master Skills Only (Zero Extra Agents)` (`growth-strategy` + `bigm-dev-team-architecture` — `~106` idle tok)
   - `Full Agency & Engineering Suite` (`All skills + all 10 agents` — `~519` idle tok)

---

### Step 2 — Round 2 Interview: Granular Component & Profile Selection

Run **Step 2** whenever the user selected **`Custom Pick`** in Step 1 **OR** selected **`hermes`** as a target harness:

1. **If `Custom Pick` was selected — ask 2 multi-select questions built dynamically from `--catalog --json`:**
   - **Select Skills to Install** (`is_multi_select: true`):
     - `growth-strategy (~52 idle tok)` — Digital strategy, GTM, pitch decks, SEO/GEO citability, web CRO, outbound ABM, paid media & compliance
     - `bigm-dev-team-architecture (~54 idle tok)` — CTO-led 4-wave multi-agent swarm OS, Figma UX/UI workflow, Postgres RLS, QA & Cloudflare
     - *(Include any newer skills returned by `--catalog --json`)*
   - **Select Swarm Agents to Install** (`is_multi_select: true`):
     - `cto (~39 tok, inherit)` — Hands-On CTO & Swarm Tech Lead (ADRs, shared contracts, parallel wave dispatch)
     - `pixel (~42 tok, inherit)` — Principal UX/UI & Figma Systems Lead (Figma MCP, Code Connect, `DESIGN.md`, WCAG 2.2, RTL)
     - `forge-fe (~42 tok, flash)` — Senior Frontend, PWA & Mobile Engineer
     - `forge-be (~42 tok, flash)` — Senior Backend, API & PostgreSQL RLS Engineer
     - `datum (~40 tok, flash)` — Data, CSV/XLSX ETL & Hybrid RAG Engineer
     - `synapse (~42 tok, inherit)` — Principal AI, MCP & Low-Token `SKILL.md` Architect
     - `bastion (~41 tok, flash)` — DevSecOps, CI/CD, Secret Scanning & Cloudflare SRE
     - `veritas (~41 tok, inherit)` — Independent 3-Round QA, DevTools Visual Parity & Red-Team Judge
     - `growth (~42 tok, flash)` — VP Growth, Prospect Dossiers, SEO/GEO, ABM & Verified Pitch Decks
     - `ledger (~41 tok, flash)` — Deal Desk, Python Margin/ROI Models & GDPR / CNDP Law 09-08 Audits
     - `None (install skills only, no agents)`

2. **If `hermes` was selected in Step 1 — ask which Hermes Profile(s) to equip** (`is_multi_select: true`):
   - Offer the actual profile directories returned in `harnesses.hermes.profiles` from `--detect --json` (e.g., `default`, `coo`, `growth`, `forge`), defaulting to `(Recommended) default` if none exist yet.

---

### Step 3 — Deterministic Installation & Verification

1. Preview or execute `scripts/install.py` passing the exact answers collected in Steps 1–2:
   ```bash
   python scripts/install.py \
     --harness <comma_separated_harnesses> \
     --scope <global|workspace> \
     --workspace-dir "<user_workspace_path>" \
     --hermes-profile <comma_separated_profiles> \
     --skills <comma_separated_skills_or_none> \
     --agents <comma_separated_agents_or_none> \
     --json
   ```
   *(Notice what `install.py` automatically handles per harness: native Antigravity frontmatter for `antigravity`, Anthropic `.claude/agents/` model/frontmatter adaptation for `claude-code`, and `<= 60`-char description validation for `hermes`!)*
2. Run post-install verification:
   - On **Antigravity**: run `agy agents` (if `agy` CLI is present) to confirm newly installed agents appear live, and check whether `pixel` was installed without the official Figma plugin—if so, suggest installing `antigravity-plugins-partners/plugin/figma`.
   - Run `python scripts/install.py --list-installed --workspace-dir "<user_workspace_path>"` to confirm target state.
3. If you created a temporary clone in Step 0, remove the temporary clone directory cleanly.

---

### Step 4 — Concise Hand-Off Receipt

Report back to the user in a compact summary containing:
1. **Installed Harnesses, Skills & Agents** + exact file paths written.
2. **Idle Context Cost Added** (`estimated_idle_tokens_per_harness` from `--json` output).
3. **3 Tailored Starter Commands / Prompts** matching the exact components they chose (see [`USAGE.md`](./USAGE.md)).
4. **Modify / Uninstall One-Liner:** Remind them they can add or remove modules anytime via `python scripts/install.py` or `--uninstall`.
