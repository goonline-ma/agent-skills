---
name: growth-strategy
description: Master digital strategy & growth OS. Routes GTM, positioning, pitch decks, SEO/GEO, web CRO, outbound/ABM, content, paid media, and growth loops to lean on-demand playbooks.
---

# Growth Strategy & Digital Marketing OS

High-signal router for end-to-end digital strategy, demand generation, sales enablement, and conversion engineering. Designed for minimum token footprint: **never load all references at once**—load only the 1–2 playbooks required for the active task.

## 1. Mandatory Pre-Flight Protocol

1. **Read Workspace Context First:** Before asking questions, check `.agents/product-marketing.md`, `docs/gtm/`, `docs/BUSINESS_MODEL.md`, `docs/SCOPE.md`, and `README.md`. Ask only for missing, decision-blocking inputs.
2. **Big M / Client Governance:** Whenever working on Big M Solutions brands (`bigmsolutions.net`, GoOnline, RestoHub, GoCRM, GOAI, Atlasbase, Copilote) or Moroccan/EU B2B engagements, load [09-bigm-and-compliance.md](./references/09-bigm-and-compliance.md). Hard rules: **draft-only externally** (CEO approves before send/publish), **no pricing in pitch decks**, **real screenshots only** (no AI people/offices), **zero placeholders**.
3. **Evidence & Deterministic Math:** Register external facts in [citation_ledger.py](./scripts/citation_ledger.py); label inferences `[hypothesis]`. Compute all CAC/LTV, funnel targets, and ICE/RICE scores via [growth_calc.py](./scripts/growth_calc.py)—never mental math.
4. **Zero AI Slop:** Enforce active human subjects, concrete numbers over adjectives, varied cadence, and zero throat-clearing or `"not X, it's Y"` clichés.

## 2. On-Demand Playbook Router

Read **only** the reference matching the user's immediate objective:

| Objective / Trigger | Load Playbook | Helper Script / Output |
| :--- | :--- | :--- |
| **Digital strategy, GTM plan, positioning, ICP, offer, pricing tiers, launch plan** | [01-digital-strategy-gtm.md](./references/01-digital-strategy-gtm.md) | `growth_calc.py funnel` → `.agents/product-marketing.md` + GTM Roadmap |
| **Pitch decks, investor/sales presentations, spec-vs-pitch challenge, slide visual QA** | [02-pitch-decks-presentations.md](./references/02-pitch-decks-presentations.md) | `render_deck_windows.ps1` + `deck_qa.py` → `.pptx` (embedded) + `.pdf` |
| **SEO, GEO / AI search citations (ChatGPT, Perplexity, AIO), `llms.txt`, clusters, pSEO** | [03-seo-geo-search.md](./references/03-seo-geo-search.md) | Technical/citability audit, answer blocks, JSON-LD, hub-spoke map |
| **Website design, high-converting landing pages, page/checkout CRO, hero/offer hierarchy** | [04-website-design-cro.md](./references/04-website-design-cro.md) | 10-block wireframe/code spec, Fogg friction audit, CWV gates |
| **Outbound GTM, Clay-style signals, cold email sequences, ABM, CEO prospect dossiers, case studies** | [05-outbound-abm-sales.md](./references/05-outbound-abm-sales.md) | `citation_ledger.py` → 1-page dossier, `<75w` sequences, case study |
| **Content strategy, conversion copywriting, LinkedIn founder engine, FR/EN/Darija atomization** | [06-content-copy-social.md](./references/06-content-copy-social.md) | Pillar-to-6× assets, awareness-matched copy, anti-slop pass |
| **Paid media (Google, Meta, LinkedIn), ad creative matrix, wasted-spend audit, agency briefs** | [07-paid-media-creative.md](./references/07-paid-media-creative.md) | `growth_calc.py economics` → Campaign architecture + creative brief |
| **Growth loops, KPI trees, ICE/RICE experiments, activation/onboarding, churn & attribution** | [08-growth-loops-analytics.md](./references/08-growth-loops-analytics.md) | `growth_calc.py score` → Loop spec, KPI tree, experiment backlog |
| **Big M brand facts, `@growth` workflow, `[HUMAN-GOONLINE]` handoffs, CNDP / Loi 31-08 / 69-21** | [09-bigm-and-compliance.md](./references/09-bigm-and-compliance.md) | Governance & regulatory compliance checklist |

## 3. Multi-Skill Chaining Recipes

When executing compound initiatives, chain playbooks sequentially (persisting shared truth in `.agents/product-marketing.md`):

- **0-to-1 Product GTM:** `01-digital-strategy-gtm` → `04-website-design-cro` → `03-seo-geo-search` → `05-outbound-abm-sales`
- **Enterprise Deal Closing:** `05-outbound-abm-sales` (Prospect Dossier) → `02-pitch-decks-presentations` (Tailored No-Price Deck) → hand off pricing/SOW to `@ledger`
- **Post-Ship Revenue Flywheel:** Closed `@veritas PASS` build → `05-outbound-abm-sales` (Case Study + 20-account ABM) → `06-content-copy-social` (CEO LinkedIn + Web Blurb)
- **Paid + Organic Scale:** `06-content-copy-social` + `07-paid-media-creative` → `08-growth-loops-analytics` (Attribution & RICE iteration)

## 4. Installed Specialist Tool Bridge (Load Only When Deep Execution Required)

Do not duplicate heavy runtimes already installed in the environment—delegate when deep automated tooling is requested:
- **Deep Automated Site Crawls:** `geoskills-cli`, `geo-audit`, `seo-audit`, or `firecrawl-seo-audit`
- **Production Frontend Build & Motion Polish:** `frontend-design`, `ui-ux-pro-max`, `emil-design-eng`, `web-perf`, and `chrome-devtools-mcp`
- **Workspace Collaboration Surfaces:** `gslides` / `gdocs` (Google Workspace) or `lark-doc` / `lark-im` (batch writes; respect 10k/mo Lark quota)
