# Usage Guide — GoOnline Agent Skills & Swarm Suite (`USAGE.md`)

Complete operational reference for invoking **`growth-strategy`**, **`bigm-dev-team-architecture`**, and the **10 Swarm Agents** across **Google Antigravity**, **Claude Code**, **Hermes Agent**, **Cursor**, and **Codex**.

---

## 1. Quick Invocation Matrix by Harness

| Action | Google Antigravity | Claude Code | Hermes Agent | Cursor / Codex |
| :--- | :--- | :--- | :--- | :--- |
| **Trigger a Skill** | Automatic by intent, or mention `use growth-strategy` | `/growth-strategy` or natural prompt | `hermes -p <profile> --skill growth-strategy` | Reference `@growth-strategy` or ask naturally |
| **Start Session as CTO** | `agy --agent cto` *(or select `cto` in UI)* | `claude --agent cto` *(or `"Act as @cto..."`)* | `hermes -p coo` / `--skill bigm-dev-team-architecture` | Open chat with `@cto.md` |
| **Start Session as UX/UI** | `agy --agent pixel` | `claude --agent pixel` | `hermes` with `03-ux-ui-figma-workflow.md` | Open chat with `@pixel.md` |
| **Parallel Subagents** | Automatic via `invoke_subagent(..., Workspace="share")` | Automatic via Claude `Task` subagent delegation | `hermes kanban` DAG waves | Sequential or multi-tab worktrees |

---

## 2. End-to-End Engineering Swarm Workflows (`bigm-dev-team-architecture`)

### Workflow A — Full Multi-Agent Product or Sprint Build (`@cto` Mode)

Launch Antigravity (`agy --agent cto`) or instruct your main session:

```text
Use bigm-dev-team-architecture as @cto. Read docs/SCOPE.md (or our PRD), lock Wave 0 ADRs and shared contracts, have @pixel establish DESIGN.md + packages/ui and @bastion bootstrap CI, verify Wave 1 with @veritas, then fan out Wave 2 features in parallel across @forge-fe, @forge-be, and @datum.
```

**What happens under the hood:**
1. **Wave 0 (Parallel Foundation):**
   - `cto` writes `docs/DECISIONS.md` (`D-01..D-NN`), `docs/adr/001-stack.md`, and `packages/shared` schemas.
   - `pixel` extracts Figma tokens/components into `DESIGN.md` + `packages/ui`.
   - `bastion` configures workspace scripts, GitHub Actions (`lint`, `typecheck`, `gitleaks`), and preview deployment config.
2. **Wave 1 (Blocking Gate):**
   - `veritas` runs cold checks (`lint + typecheck + test`). Wave 2 stays locked until `VERDICT: PASS`.
3. **Wave 2 (Collision-Free Parallel Fan-Out):**
   - `cto` writes a wave manifest and runs `swarm_preflight.py check-overlap` to guarantee zero overlapping file globs before spawning parallel `forge-fe`, `forge-be`, `datum`, and `synapse` workers on `feat/<issue#>-<slug>` branches.
4. **Wave 3 (Independent QA & Ship):**
   - `veritas` executes 3-round QA: cold diff audit, cross-tenant PostgreSQL RLS penetration probes, live `chrome-devtools-mcp` browser checks (`375px` mobile, `1440px` desktop, `dir="rtl"`), and `swarm_preflight.py scan-secrets`.
   - After `VERDICT: PASS` and `board.py verify-pr`, `bastion` deploys to Cloudflare with a 120s auto-rollback gate.

---

### Workflow B — Figma Design-to-Production Code (`@pixel` → `@forge-fe` → `@veritas`)

Prerequisite: Connect your Figma MCP server (in Antigravity, install the official **Figma** plugin from Customizations → Plugins).

```text
@pixel Extract the design tokens, auto-layout structure, and component mappings from https://www.figma.com/design/<fileKey>/<fileName>?node-id=12-34 into DESIGN.md and packages/ui, then have @forge-fe implement the screen with all 5 states (populated, loading, empty, error, pending) and @veritas verify visual parity at 375px, 1440px, and RTL.
```

---

### Workflow C — Independent Security, RLS & Visual Audit (`@veritas` Standalone)

Run `veritas` on any existing PR or branch before shipping to production:

```bash
# Headless CLI audit in Antigravity
agy --agent veritas -p "Audit git diff main...HEAD against issue #18, run cross-tenant RLS checks, scan-secrets, and output VERDICT: PASS or FAIL."
```

---

## 3. Digital Strategy, SEO/GEO & Revenue Workflows (`growth-strategy`)

Because `growth-strategy` uses a **3-Tier Progressive Router**, your agent loads **only** the 1–2 playbooks required for your prompt—keeping 85%+ of your context window free for your actual business documents and data.

### Workflow D — 0-to-1 Go-To-Market & Positioning

```text
Use growth-strategy to build our 90-day GTM plan, positioning matrix, ICP definition, and pricing-tier unit economics for [Product/Service]. Validate CAC, LTV, and monthly lead targets with growth_calc.py.
```

### Workflow E — Unified Technical SEO + AI Search Citability (GEO)

Optimize pages to get ranked in Google **and** cited/recommended by ChatGPT Search, Perplexity, Claude, and Google AI Overviews:

```text
Use growth-strategy (03-seo-geo-search) to audit https://example.com. Check SSR & AI crawler access (OAI-SearchBot, PerplexityBot, Bing/IndexNow), rewrite key sections with 40–60 word citable answer blocks, generate Organization + Product JSON-LD, and map a BoFu comparison cluster.
```

### Workflow F — Pre-Call Executive Prospect Dossier & Outbound ABM (`@growth`)

```text
@growth Build a 1-page cited pre-call prospect dossier on [Company URL]. Track every factual source in citation_ledger.py, label inferences [hypothesis], list 5 discovery questions, and draft a 3-touch <75-word ABM sequence.
```

### Workflow G — Zero-Overlap Executive Pitch Deck (`.pptx` + `.pdf`)

```text
@growth Create a 12-slide executive capability deck for [Client/Opportunity] following growth-strategy (02-pitch-decks-presentations). Export slide PNGs and embedded PDF via render_deck_windows.ps1 and run deck_qa.py check + grid until issues=0.
```

### Workflow H — Deal Economics, Margin Audit & CNDP Law 09-08 Review (`@ledger`)

```text
@ledger Model three SOW delivery options in Python (comparing engineering hours, AI token overhead, and net margin), and review our lead-capture & analytics flow against GDPR, Moroccan CNDP Law 09-08, Law 31-08, and Law 69-21 payment terms.
```

---

## 4. Deterministic Helper Scripts Reference

Every script runs standalone with Python 3.9+ standard library (only `deck_qa.py` uses `python-pptx` / `Pillow` when inspecting `.pptx` files):

```bash
# 1. Interactive / selective multi-harness installer
python scripts/install.py                                     # Interactive terminal wizard
python scripts/install.py --detect --json                     # Auto-detect installed harnesses
python scripts/install.py --list-installed                    # Inspect installed modules

# 2. Swarm file-collision & secret preflight (bigm-dev-team-architecture)
python skills/bigm-dev-team-architecture/scripts/swarm_preflight.py wave-template --out wave.json
python skills/bigm-dev-team-architecture/scripts/swarm_preflight.py check-overlap wave.json
python skills/bigm-dev-team-architecture/scripts/swarm_preflight.py scan-secrets .

# 3. GitHub Projects v2 & fresh PR gate (bigm-dev-team-architecture)
python skills/bigm-dev-team-architecture/scripts/board.py list --org <org> --project 1
python skills/bigm-dev-team-architecture/scripts/board.py status 14 "In review" --org <org> --project 1
python skills/bigm-dev-team-architecture/scripts/board.py verify-pr 27 --org <org> --repo <slug>

# 4. Unit economics, funnel reverse-engineering & ICE/RICE scoring (growth-strategy)
python skills/growth-strategy/scripts/growth_calc.py economics --arpu 250 --gross-margin 0.80 --monthly-churn 0.03 --cac 600
python skills/growth-strategy/scripts/growth_calc.py funnel --revenue-goal 50000 --acv 5000 --win-rate 0.25 --sql-rate 0.40 --lead-rate 0.04
python skills/growth-strategy/scripts/growth_calc.py score --mode rice --items '[{"name":"GEO Comparison Hub","reach":2000,"impact":2.0,"confidence":0.8,"effort":2}]'

# 5. Citation provenance ledger & PPTX visual QA (growth-strategy)
python skills/growth-strategy/scripts/citation_ledger.py add --claim "12+ years active" --url "https://goonline.ma" --file ledger.json
python skills/growth-strategy/scripts/deck_qa.py check presentation.pptx
```

---

## 5. Adding, Updating, or Removing Modules Later

Re-run the installer at any time to adjust your setup without affecting unrelated skills:

```bash
# Add a single agent later (e.g., equip Claude Code with @pixel and @veritas)
python scripts/install.py --harness claude-code --scope global --agents pixel,veritas

# Preview token footprint before installing (--dry-run)
python scripts/install.py --harness antigravity --preset marketing --dry-run

# Cleanly uninstall specific agents or skills
python scripts/install.py --uninstall --harness antigravity --scope global --agents datum,synapse
```
