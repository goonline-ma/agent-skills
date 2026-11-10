# 08 — Growth Loops, ICE/RICE Experimentation, Lifecycle & Attribution

Use when engineering compounding product/ecosystem growth loops, building KPI trees, prioritizing growth backlogs with ICE/RICE, optimizing onboarding/activation/push timing, preventing churn, or designing attribution.

## 1. Funnels End; Compounding Loops Scale

Funnels consume linear budget ($1 in → $X out). Pair acquisition with at least **one self-reinforcing Growth Loop** where 1 cohort's normal product usage generates the next cohort's input:

| Loop Archetype | Mechanism (`New User → Action → Output → New User`) | High-Leverage B2B / SMB Examples |
| :--- | :--- | :--- |
| **1. Artifact / Viral Utility Loop** | User completes core job → sends branded output to external counterparty → recipient sees proof/utility & adopts | App-issued factory guarantee sent to end-buyer via WhatsApp; interactive invoice/payment portal; shared audit report with *"Powered by [Brand]"*. |
| **2. B2B2B Ecosystem / Partner Loop** | Partner adopts free multi-client cockpit → migrates client roster to cut manual work → platform routes new leads back to top partners | Accountant/Fiduciaire multi-client portal; distributor validation portal gating artisan rewards. |
| **3. User / Data Content Loop** | Anonymized platform activity / directory listings → structured high-intent pages → Google + AI search citations → new users | Verified supplier/partner directories, public benchmark calculators, template libraries. |
| **4. Sales-to-Case-Study ABM Loop** | Closed deal passes QA → quantified case study + 20 lookalike accounts → higher reply/close rate on twins | Automated post-milestone case study + sector-twin ABM wave (`05-outbound-abm-sales.md`). |

Measure loop health via **Loop Cycle Time** (how fast 1 turn completes—shorten relentlessly) and **Viral/Expansion Coefficient** ($K$-factor or net partner seats added per cohort).

## 2. North Star Metric (NSM) & KPI Tree

Never track vanity totals (impressions, raw signups). Anchor on **1 North Star Metric** capturing delivered customer value (e.g., *Weekly Active Reconciled Dossiers*, *Completed Verified Orders*, *Active Paying Locations*) decomposed into controllable input levers:

- **Acquisition Quality:** Qualified Visitor → Signup/Lead % (by channel & intent tier)
- **Activation (Aha Moment):** % reaching first real value within $T$ hours/minutes + **Time-to-First-Value (TTFV)**
- **Engagement / Habit:** D7 / D30 core-action retention, multi-feature / team-invite depth
- **Monetization & Efficiency:** PQL/SQL → Paid %, ACV, **LTV:CAC ≥ 3:1**, **CAC Payback ≤ 12 months**, **Net Revenue Retention (NRR)**

Run `python scripts/growth_calc.py economics` and `funnel` to compute exact sensitivity before picking focus areas.

## 3. Disciplined Experimentation OS (Hypothesis → Score → Ship → Log)

Ban ad-hoc "let's try X" tasks. Every experiment requires a falsifiable card:
1. **Observation / Evidence:** Exact funnel drop-off, session recording, search gap, or interview signal.
2. **Falsifiable Hypothesis:** *"Because [evidence], changing [specific lever] for [segment] will move [primary metric] from [baseline] to [target] within [N days / M conversions], without degrading [guardrail metric]."*
3. **Deterministic RICE / ICE Scoring:** Run `python scripts/growth_calc.py score` to rank candidates objectively:
   - $\text{RICE} = \frac{\text{Reach} \times \text{Impact (0.25..3)} \times \text{Confidence (0.5..1.0)}}{\text{Effort (person-weeks)}}$
   - $\text{ICE} = \text{Impact (1..10)} \times \text{Confidence (1..10)} \times \text{Ease (1..10)}$
4. **Outcome Ledger:** Record `WIN / FLAT / LOSS` + root learning in repo docs (`docs/gtm/EXPERIMENTS.md`) so future cycles compound institutional memory.

## 4. Onboarding Activation, Push Timing & Churn Rescue

1. **Collapse Time-to-First-Value:** Strip non-essential setup steps before the Aha moment (let users simulate a file import or see pre-loaded sample data in < 60s before demanding company tax IDs or billing setup).
2. **Permission Timing Rule (Android 13+ / iOS / Web Push):** Never trigger `POST_NOTIFICATIONS` on cold app launch (opt-in craters). Trigger permission **immediately after** a high-value event where push utility is obvious (e.g., *"Order submitted—enable alerts to get live dispatch updates"*).
3. **Behavioral Lifecycle Triggers (Not Calendar Blasts):**
   - *Stalled Activation (T+24h zero core action):* Plain-text 1-click concierge rescue or 45s GIF walkthrough of the exact stuck step.
   - *Habit Drop (14d usage decay on active account):* Proactive CSM/automated check-in before renewal risk solidifies.
   - *Cancellation / Save Flow:* Structured exit reason → tailored remedy (pause, tier right-size, done-for-you data import fix—never blanket discounts that train abuse) + involuntary churn dunning sequence (pre-expiry + retry days 1, 3, 7).

## 5. Hybrid Attribution (Surviving Dark Social & AI Search)

Cookie/UTM click-attribution alone undercounts Founder LinkedIn, WhatsApp shares, word-of-mouth, and ChatGPT/Perplexity research:
- Combine **1) Digital UTMs + First/Last-Touch CRM logging**, **2) Mandatory Self-Reported Attribution** on demo/signup forms (*"How did you first hear about us?"* free-text field—catches *"ChatGPT"*, *"My accountant"*, *"LinkedIn"*), and **3) Cohort Holdout / Lift Checks** before scaling paid spend.

## Verification Checklist
- [ ] Growth plan includes ≥ 1 compounding loop alongside acquisition channels, with TTFV and NSM defined.
- [ ] Experiment backlog scored deterministically via `scripts/growth_calc.py score` with explicit guardrails.
