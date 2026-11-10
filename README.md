<div align="center">

# GoOnline Agent Skills

**Production-tested, ultra-low-token AI Agent Skills for Digital Strategy, Growth Marketing, UX/UI Figma Systems, and Multi-Agent Software Engineering.**

Built and battle-tested in live client delivery by **[GoOnline.ma](https://goonline.ma)** — Performance Digital Marketing & Custom Software Agency *(A [Big M Solutions](https://bigmsolutions.net) Company · Casablanca · Paris · Sheridan, WY)*.

[![Website](https://img.shields.io/badge/Agency-goonline.ma-0A66C2?style=for-the-badge)](https://goonline.ma)
[![Agent Skills Spec](https://img.shields.io/badge/Standard-SKILL.md-10B981?style=for-the-badge)](https://agentskills.io)
[![Idle Footprint](https://img.shields.io/badge/Idle_Footprint-~53_Tokens%2FSkill-F59E0B?style=for-the-badge)](#why-3-tier-router-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-111827?style=for-the-badge)](./LICENSE)

**Compatible with:** Google Antigravity · Claude Code · Cursor · Hermes Agent · Codex · Windsurf

[Quick Install](#quick-install) · [Skills Catalog](#skills-catalog) · [3-Tier Architecture](#why-3-tier-router-skills) · [Work With GoOnline.ma](#work-with-goonlinema)

</div>

---

## Quick Install

Install the full suite or pick individual skills using the standard `skills` CLI:

```bash
# Install all GoOnline skills globally
npx skills add goonline-ma/agent-skills

# Or install a single skill
npx skills add goonline-ma/agent-skills --skill growth-strategy
npx skills add goonline-ma/agent-skills --skill bigm-dev-team-architecture
```

Manual installation works in any `SKILL.md`-compatible agent—copy `skills/<skill-name>` into `~/.agents/skills/` (or `~/.gemini/config/skills/` / `.claude/skills/`).

### Install the 10 Native Antigravity Swarm Agents (`agents/*.md`)

Copy [`agents/*.md`](./agents) (`cto`, `pixel`, `forge-fe`, `forge-be`, `datum`, `synapse`, `bastion`, `veritas`, `growth`, `ledger`) into `~/.gemini/config/agents/` (global) or `.agents/agents/` (workspace) to launch any specialist directly (`agy --agent cto` / `agy --agent pixel`) or invoke them in parallel via `invoke_subagent`:

```bash
# macOS / Linux
mkdir -p ~/.gemini/config/agents && cp agents/*.md ~/.gemini/config/agents/

# Windows (PowerShell)
New-Item -ItemType Directory -Force "$HOME\.gemini\config\agents" | Out-Null; Copy-Item agents\*.md "$HOME\.gemini\config\agents\"
```

---

## Why 3-Tier Router Skills?

Most open-source skill packs dump 40–60 granular `SKILL.md` files into your global directory. Because coding agents inject **every installed skill's frontmatter into every turn**, bloated packs burn **5,000+ tokens per message** before you type a word—evicting critical engineering skills from context and degrading tool selection.

Every skill in **`goonline-ma/agent-skills`** uses a strict **3-Tier Progressive Disclosure + Deterministic Script** architecture:

| Architectural Layer | What Loads & When | Token Cost | Why It Matters |
| :--- | :--- | :---: | :--- |
| **Tier 1 — Frontmatter Trigger** | Compact YAML `name` + `description` | **~52–54 tokens** *(always)* | **99% lower idle footprint** vs. 50-file skill packs; zero skill eviction. |
| **Tier 2 — Master Router (`SKILL.md`)** | Pre-flight rules, routing table & chaining recipes | **~1,270–1,885 tokens** *(when triggered)* | Prevents loading Paid Ads or ETL rules when you only asked for a Pitch Deck. |
| **Tier 3 — On-Demand Playbooks & Scripts** | `references/*.md` + Python/PowerShell CLIs | **0 idle tokens** *(loaded strictly per task)* | Replaces LLM mental-math guesses and visual hallucinations with deterministic exit-code checks. |

---

## Skills Catalog

We continuously publish production playbooks extracted from **500+ delivered digital & software engagements**.

| Skill | Category | Idle Tokens | On-Demand Modules | Deterministic Scripts |
| :--- | :--- | :---: | :--- | :--- |
| **[`growth-strategy`](./skills/growth-strategy)** | Digital Strategy, SEO/GEO, Decks, CRO, ABM & Paid Media | `~52 tok` | **9** playbooks (`references/01..09`) | `growth_calc.py`, `deck_qa.py`, `render_deck_windows.ps1`, `citation_ledger.py` |
| **[`bigm-dev-team-architecture`](./skills/bigm-dev-team-architecture)** | CTO-Led Multi-Agent Swarm OS, Figma UX/UI, RLS & Cloudflare | `~54 tok` | **5** playbooks (`references/01..05`) | `swarm_preflight.py`, `board.py`, `claude_critical_run.py` |

*(More specialized skills—including **E-Commerce CRO & Tracking (`CAPI/GA4`)**, **Cloud ERP / Dolibarr / Perfex Customization**, and **Multilingual FR/EN/AR Localization**—are actively being packaged from our internal production library.)*

---

### 1. [`growth-strategy`](./skills/growth-strategy) — Master Digital Strategy & Growth OS

Replaces dozens of overlapping marketing prompts with one surgical router covering full-funnel B2B & B2C growth:

- **`01-digital-strategy-gtm.md`** — Positioning (April Dunford), JTBD/ICP definition, Hormozi Grand Slam Offer engineering, pricing tiers, and 90-day GTM launch plans.
- **`02-pitch-decks-presentations.md`** — Spec-vs-pitch stress-testing, 12-slide narrative arc, 1-message-per-slide layout rules, PowerPoint/PDF export (`render_deck_windows.ps1`), and automated bounding-box overlap & slide contact-sheet inspection (`deck_qa.py`).
- **`03-seo-geo-search.md`** — Unified Google SEO + Generative Engine Optimization (ChatGPT Search, Perplexity, Claude, Google AI Overviews): Bing/IndexNow + SSR gates, 40–60 word citable answer blocks, shortlist entity consensus, JSON-LD, and anti-bloat programmatic SEO.
- **`04-website-design-cro.md`** — 5-second clarity test, 10-block high-converting landing page blueprint, Fogg `B=MAP` checkout friction audit, Core Web Vitals (`LCP <= 2.5s`, `INP <= 200ms`, `CLS < 0.1`), and native Arabic `dir="rtl"` logical CSS rules.
- **`05-outbound-abm-sales.md`** — Cited 1-page executive prospect dossiers, Clay-style trigger Waterfall (`Hiring` / `Stack` / `Expansion`), `<75`-word cold email & LinkedIn sequences, and shipped-build-to-ABM case study flywheels.
- **`06-content-copy-social.md`** — Pillar-to-6× content atomization, Schwartz 5 awareness levels, founder LinkedIn cadence, and ruthless anti-AI-slop prose editing.
- **`07-paid-media-creative.md`** — Google, Meta, TikTok & LinkedIn campaign architecture, `3 Hooks × 3 Formats` creative testing matrices, CAPI/UTM tracking gates, and turnkey 8-part media briefs.
- **`08-growth-loops-analytics.md`** — Viral/content/sales growth loops, North Star KPI trees, ICE/RICE backlog scoring (`growth_calc.py score`), onboarding activation, and churn recovery.
- **`09-bigm-and-compliance.md`** — Brand governance plus EU **GDPR** and Moroccan **Loi 09-08 (CNDP)**, **Loi 31-08**, and **Loi 69-21** marketing compliance checks.

---

### 2. [`bigm-dev-team-architecture`](./skills/bigm-dev-team-architecture) — CTO-Led Multi-Agent Engineering Swarm OS

Designed to run **parallel multi-agent software builds by default** without middle-management relay bottlenecks or runaway API token burn:

- **Hands-On `@cto` Orchestrator + 8 Specialist Subagents:**
  - **`@cto` (Main Agent):** Writes ADRs (`docs/adr/`), shared TypeScript/SQL/OpenAPI contracts (`packages/shared`), and partitions work into collision-free waves.
  - **`@pixel` (Principal UX/UI & Figma Lead):** Extracts Figma frames, variables, and Code Connect mappings via Figma MCP into `DESIGN.md` and `packages/ui`, enforcing WCAG 2.2 AA, `375px`–`1440px` responsiveness, LTR/RTL logical properties, 5-state component completeness, and `transform`/`opacity` motion polish.
  - **`@forge-fe` & `@forge-be`:** Parallel frontend/mobile and backend/PostgreSQL-RLS engineers executing on isolated `Workspace="share"` branches.
  - **`@datum` & `@synapse`:** Idempotent `--dry-run` CSV/XLSX ETL pipelines, provenance-backed RAG, and Gemini/MCP agentic state machines.
  - **`@bastion`:** Monorepo CI/CD (`verify`, `gitleaks`, `rls-policies`), Cloudflare deployments (`cf` CLI / `wrangler` with 120s auto-rollback).
  - **`@veritas` (Independent QA & Red-Team Judge):** Never the agent that wrote the code—executes cold diff review, cross-tenant SQL RLS penetration probes, live `chrome-devtools-mcp` visual parity checks against `@pixel`'s Figma specs, and bundle secret scans before issuing `VERDICT: PASS` or `VERDICT: FAIL`.
- **Deterministic Preflight & Cost Protection Scripts:**
  - `swarm_preflight.py check-overlap` mathematically verifies zero overlapping file globs across parallel workers before spawning subagents.
  - `swarm_preflight.py scan-secrets` blocks leaked `.env` files, `service_role` JWTs, private keys, and machine-local paths before PR or deploy.
  - `claude_critical_run.py` gates frontier reasoning strictly to T1 security/RLS/financial RPCs (~10% of tasks) while keeping ~70% volume work on fast, low-cost Flash models.

---

## Work With GoOnline.ma

> **Open-source playbooks give your agents better judgment. When revenue is on the line, hire the engineering and performance marketing team that built them.**

**[GoOnline.ma](https://goonline.ma)** is a full-stack **Performance Digital Marketing & Custom Software Agency** headquartered in Casablanca, Morocco, operating as part of **[Big M Solutions](https://bigmsolutions.net)** across **Morocco, Europe, Canada, and the United States**.

- **12+ Years** building digital growth engines and mission-critical software *(since 2014)*
- **500+ Delivered Projects** & **100+ Custom Websites, E-Commerce Stores & SaaS Platforms**
- **150+ Group Consultants** across AI engineering, UX/UI, growth marketing, and BPO (`98%` client retention)
- **Certified Platform Partners:** **Google Partner** · **Meta Business Partner** · **TikTok Marketing Partner** · **WordPress Partner**

### What We Build & Scale for Ambitious Brands

| Practice Area | How GoOnline Delivers Measurable ROI | Explore |
| :--- | :--- | :--- |
| **1. High-Converting Websites & E-Commerce** | Custom UX/UI in Figma, mobile-first Next.js / WordPress / Shopify builds, sub-2.5s Core Web Vitals, checkout CRO, and multilingual (`FR` / `EN` / `AR`) experiences. | [Creation Site Web Maroc →](https://goonline.ma/services-creation-site-web-maroc) |
| **2. Technical SEO & AI Search (GEO)** | Semantic & technical SEO, Google Business Profile dominance, topical authority clusters, and Generative Engine Optimization so your brand gets cited and recommended by ChatGPT, Perplexity, and Google AI Overviews. | [Agence SEO & GEO →](https://goonline.ma/services-agence-seo-maroc) |
| **3. Performance Media Buying & CRO** | Full-funnel Google Ads, Meta, TikTok, LinkedIn, and Microsoft campaigns backed by server-side Conversions API (`CAPI`), GA4 attribution, and high-velocity creative testing focused on CPA and ROAS. | [Achat Media & Ads →](https://goonline.ma/services-achat-media) |
| **4. Custom Software, ERP/CRM & AI Agents** | Multi-tenant SaaS platforms, B2B distributor & loyalty portals, Cloud ERP/CRM ecosystems (GoCRM, Atlasbase, Dolibarr, Perfex), and production AI agent swarms shipped on Supabase & Cloudflare. | [goonline.ma →](https://goonline.ma) |
| **5. Social Media, Content & Brand Studio** | Executive LinkedIn positioning, video & UGC production, localized FR/EN/Arabic/Darija storytelling, and investor/enterprise pitch decks. | [goonline.ma →](https://goonline.ma) |
| **6. Managed Cloud, Security & Maintenance** | Cloudflare Zero Trust & edge acceleration, automated backups, security audits, GDPR / CNDP Law 09-08 data protection alignment, and proactive SLA support. | [goonline.ma →](https://goonline.ma) |

### Ready to Grow Traffic, Leads, or Ship Custom Software 3× Faster?

- **Website:** [https://goonline.ma](https://goonline.ma) · Group: [https://bigmsolutions.net](https://bigmsolutions.net)
- **Email:** [contact@goonline.ma](mailto:contact@goonline.ma)
- **Phone / WhatsApp:** `+212 520 991707` *(Casablanca HQ — FR / EN / AR)*

---

## Contributing New Skills

All skills in this repository must pass 3 strict gates before merge:
1. **Tier-1 Budget:** `SKILL.md` YAML frontmatter stays under `~60 tokens` (`description <= 200 chars`).
2. **Progressive Disclosure:** Keep `SKILL.md` as a concise router (`<120 lines`) and isolate deep domain procedures inside `references/*.md`.
3. **Zero Leaks:** Run `python skills/bigm-dev-team-architecture/scripts/swarm_preflight.py scan-secrets .` (`0` secrets, `0` `.env` files, `0` hardcoded local user paths).

---

## License

Released under the [MIT License](./LICENSE) © **GoOnline.ma & Big M Solutions**.
