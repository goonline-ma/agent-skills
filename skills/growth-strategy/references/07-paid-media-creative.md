# 07 — Paid Media Architecture, Ad Creative & Agency Briefing

Use when designing paid acquisition campaigns (Google, Meta, LinkedIn, YouTube/TikTok), auditing ad accounts for wasted spend, writing direct-response ad creative matrices, or producing turnkey creative/media briefs (including `[HUMAN-GOONLINE]`).

*(Hard governance: Never commit media spend or launch paid campaigns without explicit CEO/user budget sign-off. Compute max allowable CPC/CPL via `scripts/growth_calc.py economics` first.)*

## 1. Channel Architecture by Intent & Modern Platform Algorithms

| Channel | Best Role | Modern Account Structure | Classic Budget-Burning Trap to Avoid |
| :--- | :--- | :--- | :--- |
| **Google Search** | Capture existing bottom-funnel intent | Tightly themed Exact + Phrase match ad groups per high-intent cluster; dedicated landing page per theme; aggressive shared **Negative Keyword** lists (`gratuit`, `emploi`, `stage`, `pdf`, `cours`, `open source`). | Launching PMax or Broad Match on low conversion volume (< 30 qualified conversions/mo) or sending paid clicks to a generic homepage. |
| **Meta Ads (FB/IG)** | Demand creation, SMB/B2B reach, retargeting | Consolidated **Creative-as-Targeting** structure (1 Prospecting CBO/ABO + 1 Proof Retargeting campaign); let the creative hook self-select the buyer persona. | Micro-slicing 10 tiny interest ad sets that starve learning phase instead of testing distinct creative angles. |
| **LinkedIn Ads** | Mid/Enterprise B2B ABM (`ACV > $5k`) | Matched Account List + strict Job Title/Seniority filter; lead with **Thought Leader Ads** (boosting high-performing founder posts) + Document/Carousel proof ads. | Turn **OFF** Audience Network & Audience Expansion immediately; never run cold Lead Gen Forms without a qualifying friction question. |
| **Retargeting (Cross-Platform)** | Close high-intent visitors (Pricing/Demo views, 50%+ video viewers) | Exclude existing customers; serve **objection-crushing proof** (case studies, 60s product walkthrough, migration guarantee)—never repeat the cold top-of-funnel ad. | Measuring platform-inflated 1-day view-through conversions as incremental new demand. |

## 2. The 5×3 Direct-Response Creative Matrix

Creative diversity—not bid tweaking—drives 80% of paid performance. Ship **5 distinct Hook Angles × 3 Formats** per sprint:

### 5 Core Hook Angles
1. **Direct Pain Callout:** *"Managing 80 SME accounting dossiers via WhatsApp photos and USB keys?"*
2. **Cost-of-Inaction Math:** *"One missed Law 69-21 quarterly declaration costs 3% + 0.85%/month in DGI penalties."*
3. **Live Mechanism Demo (Before → After):** Split-screen or screen-recording showing legacy chaos vs 10-second automated workflow.
4. **Habit / Competitor Reframe:** Show why the familiar workaround silently leaks margin (coopt rather than insult the user).
5. **Peer Case Proof:** *"How a 35-person Casablanca distributor cut order errors to zero in 14 days."*

### 3 Core Formats
- **Static Annotated UI / Contrast Card** (`1:1` `1080×1080` + `4:5` `1080×1350`)
- **Founder / Practitioner Direct-to-Camera + Screen Overlay** (`9:16` `1080×1920` + `4:5`, captioned FR + Darija/EN, hook in first 2.5s)
- **Carousel / Document Breakdown** (4–6 swipeable proof frames)

## 3. Wasted-Spend Paid Account Audit Rubric

When auditing an existing ad account, inspect in this exact order:
1. **Conversion Integrity:** Are platforms optimizing for *qualified pipeline / SQLs / purchases* via server-side CAPI / Offline Conversion Import, or optimizing for junk bot leads / page views?
2. **Search Terms / Placements Bleed:** % of spend on irrelevant search queries, mobile gaming app placements (Display/Audience Network), or unsegmented brand terms masquerading as prospecting ROAS.
3. **Creative Fatigue & Concentration:** Frequency > 3.5 on prospecting with rising CPA, or 90% of spend stuck in 1 aging ad with zero fresh angle tests.
4. **Post-Click Drop-Off:** High CTR (`> 1.5%`) paired with `< 2%` landing-page conversion = landing-page message mismatch or mobile load speed failure (`LCP > 3s`).

## 4. Turnkey Creative & Media Execution Brief (`[HUMAN-GOONLINE]` Standard)

Eliminate agency back-and-forth by supplying all 8 checkable blocks in one brief:
1. **Objective & Target KPI:** Business outcome, primary metric, max CPA/CPL ceiling (from `growth_calc.py`).
2. **Audience & Channel:** Exact segment, geography, language (`FR` / `EN` / `AR` / `Darija`), placement.
3. **Single-Minded Proposition + Verified Proof:** 1 sentence + approved facts (zero unverified claims, zero unapproved pricing).
4. **Ready-to-Use Copy Pack:** Final primary text + 3 headline hooks + description + CTA button label (written complete, zero `[insert copy]` placeholders).
5. **Asset & Brand Specs:** Exact dimensions/durations, brand palette/typography, **real product screenshots and real client/company footage only** (no AI-generated people/offices; include *"Publicité"* disclosure where Loi 31-08 Art. 23 applies).
6. **Tracking & Attribution:** Standardized UTM string (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content=<angle>_<format>_v1`), conversion event name, pixel/CAPI check, exact destination URL.
7. **Approved Budget & SLA:** CEO-approved test budget, launch date, max 2 review rounds.
8. **Acceptance Checklist:** Objective pass/fail criteria for `@veritas` / CEO review before go-live.

## Verification Checklist
- [ ] Max CPA/CPC mathematically validated against LTV/margin via `scripts/growth_calc.py`.
- [ ] Every ad angle maps to a congruent landing page H1 + clean UTM + verified conversion event.
