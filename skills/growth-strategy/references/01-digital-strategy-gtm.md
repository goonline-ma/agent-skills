# 01 — Digital Strategy, Positioning, Offer & GTM Architecture

Use when formulating or overhauling a go-to-market strategy, positioning spine, ICP segmentation, offer/pricing architecture, channel selection, or launch plan.

## 1. Context Spine (`.agents/product-marketing.md`)

Create or update `.agents/product-marketing.md` first so every downstream playbook inherits identical strategic truth:
1. **Category & Positioning** (April Dunford Canvas)
2. **ICP Tiers & Anti-ICP** (Firmographics, trigger events, buyer vs champion vs blocker)
3. **Value Equation & Core Offer** (Quantified outcome, mechanism, time-to-value, risk reversal)
4. **Channel-Model Fit & Funnel Architecture** (Primary 1–2 channels, unit economics ceilings)
5. **Proof Vault** (Verified metrics, shipped builds, named/anonymized case studies, regulatory badges)

## 2. Positioning & Offer Engineering

### April Dunford 5-Step Positioning Sequence
Run strictly in order—never pick a category before mapping alternatives:
1. **Competitive Alternatives:** What would the customer actually do if you didn't exist? *(Often Excel, WhatsApp + paper, legacy desktop like Sage 100, or hiring an intern—not another SaaS.)*
2. **Unique Attributes:** Capabilities/architecture you have that those alternatives lack (e.g., 10-min automated migration, sovereign hosting, native MCP, factory-backed app guarantee).
3. **Value + Proof:** Translate each attribute into a hard business metric (revenue unlocked, hours/errors cut, compliance fines avoided) backed by verifiable evidence.
4. **Best-Fit ICP:** Characteristics of buyers who care *most* urgently about that specific value right now.
5. **Market Category:** Frame the context that makes your unique attributes obvious winners (new game vs head-to-head vs niche wedge).

### Hormozi Offer Value Equation
Maximize: $\text{Value} = \frac{\text{Dream Outcome} \times \text{Perceived Likelihood}}{\text{Time Delay} \times \text{Effort \& Sacrifice}}$
- **Cut Time Delay:** Instant sandbox, 10-minute automated data import, Day-1 quick win before full rollout.
- **Cut Effort:** Done-for-you onboarding migration, pre-built industry templates, zero-retraining UX (coopt existing habits like WhatsApp delivery instead of fighting them).
- **Boost Likelihood & Reverse Risk:** Pilot milestones, conditional performance guarantees, live verifiable demos.

## 3. Channel-Model Fit Matrix

Never spread budget across 6 channels at launch. Pick **1 Primary Capture Channel** + **1 Primary Demand/Outbound Channel** based on ACV and existing search intent:

| ACV / Deal Size | High Existing Search Intent | Low / Latent Intent (New Mechanism) | Ecosystem / Aggregator Leverage |
| :--- | :--- | :--- | :--- |
| **< $1k/yr (SMB / Self-Serve)** | SEO/GEO Comparison & Use-Case Pages, Programmatic SEO, High-Intent Search | Viral/Artifact Loops, Founder/Creator Short-Form Video, Community | App Marketplaces, Built-In Shareable Artifacts (invoices, badges, guarantees) |
| **$1k–$15k/yr (Mid-Market B2B)** | Bottom-Funnel Google Search + GEO Shortlist Authority + Interactive Demo | Signal-Based Cold Outbound + Meta/LinkedIn Pain-Hook Video + Webinars | **B2B2B Partner Flywheel** (Accountants/Fiduciaires, Distributors, Agencies, Trade Associations) |
| **$15k–$100k+ (Enterprise / Custom)** | Executive Thought Leadership + Niche Benchmark Reports + Referral | **1:1 CEO/VP ABM** (Prospect Dossiers + Tailored Decks) + Executive Events | Institutional/Gov Referencing (e.g., Maroc PME PACTE TPME, Industry Federations) |

## 4. Packaging & Pricing Architecture

*(Note: Never put pricing in pitch decks; route final contract/pricing approval through `@ledger` + CEO.)*
- **Value Metric:** Charge along the axis where customer value scales (active dossiers/locations/volume, not seats when seat-friction blocks adoption—e.g., keep accountant/auditor seats free in B2B2B flywheels).
- **3-Tier Good / Better / Best Fencing:**
  - **Tier 1 (Entry Wedge):** Low-friction entry solving core pain with hard volume/automation cap.
  - **Tier 2 (Target Anchor — highlight):** Complete workflow + core automations; priced for target LTV:CAC ≥ 3:1.
  - **Tier 3 (Enterprise / Multi-Entity):** SSO, dedicated vault/SLA, custom integrations, multi-entity consolidation.
- Run `python scripts/growth_calc.py economics` and `funnel` to verify CAC payback ≤ 12 months before locking channel budgets.

## 5. Zero-Based Launch Sequence (T-4w to T+4w)

- **T-4w to T-2w (Foundation & Pioneers):** Lock `.agents/product-marketing.md`, ship conversion landing page + tracking events, onboard 5–15 design partners/pioneers for real screenshots and baseline outcomes.
- **T-1w (Enablement):** Arm sales/CEO with 1-page battlecards, objection matrix, demo flow, and outbound signal lists; warm partner/ecosystem channels.
- **Launch Week (Concentrated Spike):** Coordinated Founder narrative, live mechanism demo video, partner co-announcement, targeted ABM wave, and high-intent search/retargeting activation.
- **T+1w to T+4w (Loop Lock-In):** Audit drop-offs at first activation milestone, convert first wins into cited case studies, kill bottom-quartile channels, double down on lowest-CAC winner.

## Pitfalls & Verification
- **Pitfall:** Treating generic personas ("SME owners aged 30–55") as an ICP. Define ICP by **observable trigger + structural pain + tech/regulatory state**.
- **Pitfall:** Mixing verified product capabilities with roadmap wishes. Separate **Shipped Today** from **Planned** strictly.
- **Verification:** [ ] `.agents/product-marketing.md` written; [ ] Unit economics & funnel math verified via `growth_calc.py`; [ ] Every market stat cited; [ ] Roadmap split into Verified Facts, Hypotheses, and ICE-ranked 30/60/90 Actions.
