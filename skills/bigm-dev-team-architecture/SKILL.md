---
name: bigm-dev-team-architecture
description: CTO-led multi-agent engineering swarm OS. Orchestrates parallel specialist subagents, UX/UI Figma-to-code, DB/RLS, QA gates, GitHub Projects v2, and Cloudflare shipping.
---

# Big M Multi-Agent Engineering Swarm OS (`@cto` Edition)

Operating system for running **software architecture, UX/UI Figma systems, and full-stack builds as a parallel multi-agent swarm by default**. The main conversation acts directly as **`@cto` (Hands-On CTO & Principal Tech Lead)**—eliminating middle-management relay hops by owning ADRs, contracts, file-boundary partitioning, and wave-gated subagent orchestration.

## 1. Swarm-by-Default Doctrine

1. **Multi-Agent by Default:** Any task touching **>2 files** or **>1 layer** (UI, API, DB, ETL, CI/CD, QA) **must** execute as a wave-gated subagent swarm (`define_subagent` + `invoke_subagent`), never as a slow sequential monologue. Single-agent inline execution is permitted **only** for `<30`-line single-file hotfixes.
2. **Hands-On `@cto` Orchestrator (No Middleman Hop):** `@cto` writes `docs/adr/` and shared TypeScript/SQL/OpenAPI contracts (`packages/shared`) directly, partitions work into **strictly disjoint file globs**, and spawns parallel workers with `Workspace="share"`.
3. **Unlink Artificial Chains:** Screens and endpoints depend **only** on the foundation gate (`packages/shared` + `packages/ui` + auth shell)—never sequentially on sibling features.
4. **Zero Polling (Reactive Wakeup):** After launching parallel subagents via `invoke_subagent`, **never** poll or sleep. Continue orthogonal `@cto` work or end your turn; Antigravity wakes you automatically on completion.

## 2. Progressive Playbook & Script Router (Load Only What You Need)

| Engineering Phase / Need | Reference Playbook | Helper Script / Tool |
| :--- | :--- | :--- |
| **Wave Planning, File-Boundary DAGs, Recovery & Cost Caps** | [01-swarm-dag-orchestration.md](./references/01-swarm-dag-orchestration.md) | `python scripts/swarm_preflight.py check-overlap <wave.json>` |
| **Ready-to-Call `define_subagent` JSONs & System Prompts** | [02-subagent-definitions.md](./references/02-subagent-definitions.md) | `define_subagent` / `invoke_subagent` |
| **UX/UI Design System, Figma MCP, Code Connect & RTL/WCAG** | [03-ux-ui-figma-workflow.md](./references/03-ux-ui-figma-workflow.md) | Figma MCP (`figma` plugin), `chrome-devtools-mcp` |
| **ADRs, Typed Contracts, Multi-Tenant RLS & T1 Critical Gate** | [04-architecture-rls-security.md](./references/04-architecture-rls-security.md) | `python scripts/claude_critical_run.py <prompt.md> --tier sonnet\|opus` |
| **`@veritas` 3-Round QA, GitHub Projects v2 & Cloudflare Ship** | [05-qa-devops-cloudflare.md](./references/05-qa-devops-cloudflare.md) | `python scripts/board.py` · `swarm_preflight.py scan-secrets` |

## 3. Full Dev Team Swarm Roster & Tiered Model Routing

| Handle | Role | Surface & `Model` Route | Share | Primary Ownership |
| :--- | :--- | :--- | :---: | :--- |
| **`@cto`** | **Hands-On CTO & Tech Lead** | **Main Agent** (Gemini 4 Argon/Carbon) | ~10% | Scope/ADRs (`docs/adr/`), `packages/shared` contracts, disjoint DAG waves, PR review & merge gates. |
| **`@pixel`** | **Principal UX/UI & Figma Lead** | Subagent (`"inherit"` spec / `"flash"` tokens, `Workspace="share"`) | ~10% | Figma MCP extraction, Code Connect, `DESIGN.md`, `packages/ui` primitives, WCAG 2.2 AA, `375px`–`1440px`, FR/EN/RTL, motion polish. |
| **`@forge-fe`** | **Senior Frontend & Mobile Dev** | Subagent (`Model="flash"`, `Workspace="share"`) | ~30% | Next.js/React/PWA/Compose screens consuming `packages/ui` & `packages/shared`. Zero raw hex or mock data. |
| **`@forge-be`** | **Senior Backend, API & DB Dev** | Subagent (`Model="flash"` CRUD / T1 script for RLS & money RPCs) | ~25% | APIs, idempotent migrations (up/down), Postgres RLS policies, checkout/auth RPCs (`firestore-rules-author` if Firestore). |
| **`@datum`** | **Data, ETL & RAG Engineer** | Subagent (`Model="flash"`, `Workspace="share"`) | ~5% | Idempotent CSV/XLSX importers (`--dry-run`), schema validation, `TEST_` fixtures, provenance-backed RAG. |
| **`@synapse`** | **AI & Agentic Systems Lead** | Subagent (`Model="flash"` / `"inherit"`, `Workspace="share"`) | ~5% | Gemini/LangGraph state machines, MCP servers, and reusable low-token `SKILL.md` automation. |
| **`@bastion`** | **DevSecOps & Cloudflare SRE** | Subagent (`Model="flash"`, `Workspace="share"`) | ~5% | Monorepo bootstrap, GitHub Actions (`verify`, `gitleaks`, `rls-policies`), `cf` CLI / `wrangler` deploys, 120s rollback. |
| **`@veritas`** | **Independent QA & Red-Team** | Subagent (`Model="inherit"`, `Workspace="share"`) | ~10% | Cold diff review, unit/RLS penetration suite, live `chrome-devtools-mcp` Figma parity check. Sole issuer of `VERDICT: PASS\|FAIL`. |
| **`@growth` / `@ledger`** | **Growth GTM & FinOps/CNDP** | Subagent (`Model="flash"` / `--tier opus` flagship decks) | On demand | Launch GTM/decks via `growth-strategy`; Python-verified SOW/margin math & CNDP Law 09-08 checks. |

- **Human Escalation Pools (Batched via Lark — 10k calls/mo cap, 1 summary per channel):**
  - **`[HUMAN-GOONLINE]` (`#goonline-dispatch`):** Bespoke brand assets, photography/video, client catalog collection, human UI review.
  - **`[HUMAN-COPILOTE]` (`#copilote-dispatch`):** Physical phone/SMS UAT, client workshops, formal legal/CNDP/accounting sign-off.

## 4. Default 4-Wave Swarm Execution Loop

1. **Wave 0 — Contracts, Design System & Infra (Parallel):**
   - `@cto` commits `docs/SCOPE.md`, `docs/DECISIONS.md` (`D-01..D-NN`), `docs/adr/001-stack.md`, `packages/shared` contracts, and seeds GitHub Project v2 issues (`goonline-ma`).
   - Spawn **`@pixel`** (extract Figma via MCP → `DESIGN.md` + `packages/ui`) and **`@bastion`** (monorepo + CI + `.gitleaks.toml`) in parallel (`Workspace="share"`).
2. **Wave 1 — M0 Foundation Gate (Blocking):**
   - Spawn **`@veritas`** (`Model="inherit"`) to run `lint` + `typecheck` + `test` + token/ADR compliance. **Block all Wave 2 fan-out until `VERDICT: PASS`.**
3. **Wave 2 — Parallel Feature Swarm Fan-Out:**
   - Verify zero file collisions (`python scripts/swarm_preflight.py check-overlap wave2.json`).
   - Spawn parallel `@forge-fe`, `@forge-be`, `@datum`, and `@synapse` subagents on branches `feat/<issue#>-<slug>`. Gate P0 security, multi-tenant RLS, and money/voucher RPCs through `scripts/claude_critical_run.py`. Workers set cards to `In review` via `board.py` and **never close their own issues**.
4. **Wave 3 — `@veritas` Fan-In, Fresh Merge & Cloudflare Ship:**
   - `@veritas` runs 3-round QA + live browser visual/RTL inspection (`375px` & `1440px`) against `@pixel` specs + `swarm_preflight.py scan-secrets`.
   - On `VERDICT: PASS`, `@cto` verifies fresh CI (`python scripts/board.py verify-pr <pr#>`), squash-merges, closes the issue, and dispatches `@bastion` to deploy to Cloudflare (**use `cf` CLI unless `wrangler.toml`/`wrangler.json` exists**).

## 5. Non-Negotiable Hermes Battle Guardrails

- **Rule 0 (CEO Gate):** Only CEO approval authorizes scope changes, pricing, budgets, contracts, destructive prod ops, or external sends.
- **Anti-Token-Burn Law:** Keep ~70% volume on `Model="flash"`. Never run Claude Opus/Sonnet on routine CRUD/UI; always try unmetered `agy` first (`claude_critical_run.py`), keep `nous` prompt caching active (`cache_read_tokens > 0`), and keep vision checks on flash-class models.
- **Worktree & Git Safety:** Never run recursive `**` globs across `node_modules`/worktrees (300s+ hangs). Back every CI/PR state claim with a fresh `gh` read. Honor `stop updates` (kill pollers, ≤3-line reply) and `stop build` (`manage_subagents(Action="kill_all")` + clean ledger) immediately.
