# 04 — High-Converting Website Design, Landing Pages & Page CRO

Use when planning, wireframing, writing copy for, auditing, or building conversion-focused websites, SaaS/B2B landing pages, pricing pages, and onboarding/checkout funnels.

*(When implementing frontend code, pair this conversion architecture with `frontend-design`, `ui-ux-pro-max`, or `emil-design-eng`, and verify live in `chrome-devtools-mcp`.)*

## 1. The 5-Second Above-the-Fold Test

A cold visitor must answer 4 questions within 5 seconds without scrolling: **What is it? Who is it for? Why is it better than my current habit? What happens when I click?**

- **Eyebrow Badge:** Category + sharpest trust/trigger signal (e.g., *"100% Native PCGM · Law 69-21 Ready"*).
- **Outcome-Specific H1:** Concrete transformation + mechanism—ban vague slogans (*"Empowering Digital Transformation"* → *"Migrate 15 Years of Desktop Sage to Sovereign Cloud in 10 Minutes"*).
- **Subheadline (1–2 sentences):** Name the exact ICP, what manual pain disappears, and why switching is safe.
- **Friction-Matched Primary CTA + Micro-Reducer:** Match CTA commitment to awareness/ACV (*"Simulate My Import Free"* or *"Book a 15-Min Architecture Audit"* > *"Submit"*). Place 1 line of risk reduction directly beneath (*"No credit card · Sovereign MA hosting · CNDP compliant"*).
- **Visual Anchor:** Real interactive product UI, live workflow state, or crisp before/after artifact—**never** generic 3D blobs, stock handshakes, or AI-generated people.

## 2. Canonical 10-Block High-Conversion Page Arc

| # | Section | Conversion Job | Non-Negotiable Execution Rule |
| :---: | :--- | :--- | :--- |
| 1 | **Hero** | Pass 5-second clarity & hook intent | Single primary CTA; real UI frame above or straddling fold |
| 2 | **Proof Bar** | Neutralize "am I the guinea pig?" | Verified client logos, shipped volume metrics, press/gov badges (zero fake logos) |
| 3 | **Status-Quo Cost** | Agitate the real enemy (manual habit) | Quantify hours/margin/fines lost to current workaround (WhatsApp, Excel, legacy server) |
| 4 | **Mechanism (3 Pillars)** | Show *how* the outcome works | 3 concrete capabilities with interactive tabs or annotated product UI |
| 5 | **Aha-Moment Demo** | Collapse perceived effort | Interactive sandbox, 60s silent UI walkthrough, or live calculator |
| 6 | **Persona / Use-Case Split** | Speak to each stakeholder's job | Role tabs (e.g., *CEO / CFO* vs *Partner Accountant* vs *Ops Manager*) |
| 7 | **Honest Comparison** | Win shortlist evaluation | Current Habit vs Legacy Rivals vs Us (`● / ◐ / ○` capabilities, no fragile rival prices) |
| 8 | **Verified Case Proof** | Prove peer outcomes | Context → Solution → Measured metric (anonymized by sector/city if NDA-bound) |
| 9 | **Objection-Killing FAQ** | Pre-empt deal blockers on-page | Security/CNDP, migration time, ERP/API compatibility, contract lock-in |
| 10 | **Final Risk-Reversed CTA** | Capture high-intent scrollers | Restate core value + exact next step (what happens in the first 15 minutes) |

## 3. Behavioral CRO & Funnel Friction Audit (Fogg `B = M × A × P`)

Audit existing pages across three levers—**Ability (removing friction) beats Motivation 3-to-1**:
1. **Message Match:** Ad/outbound hook → Landing H1 must share exact vocabulary and promise.
2. **Hick's Law & Form Reduction:**
   - Remove top-nav escape hatches on dedicated paid landing pages.
   - Cut lead/signup forms to essential fields (≤ 4 fields; enrich company size/stack asynchronously from work domain, or use progressive 2-step forms starting with lowest-friction input).
3. **Trust Proximity:** Place security badges, SLA/refund guarantees, and peer quotes **within the same viewport** as pricing toggles, checkout buttons, and form submits—not buried at the top.
4. **Mobile & Multilingual Ergonomics:**
   - ≥ 65% of regional B2B/SMB social traffic lands on mobile: verify thumb-zone sticky CTA, 44×44px tap targets, zero horizontal overflow at `375px`, and readable UI crops (zoom into the active UI component on mobile rather than shrinking a full desktop dashboard).
   - For FR/EN/AR (`dir="rtl"`), use logical CSS properties (`ms-*`, `me-*`, `ps-*`, `pe-*`) and native Arabic/Latin type scales.

## 4. Technical Performance & Motion Guardrails

Every 100ms of delay taxes conversion:
- **Core Web Vitals Floors:** `LCP < 2.5s`, `INP < 200ms`, `CLS < 0.1`, Lighthouse SEO & Accessibility = `100`.
- **Zero-Jank Motion:** Animate `transform` and `opacity` only (never `width`/`height`/`top`), honor `prefers-reduced-motion`, preload hero font + LCP image (WebP/AVIF with explicit `width`/`height`), lazy-load below-fold media.

## Verification Checklist
- [ ] Hero passes the 5-second test with zero buzzwords and zero AI-generated human/office photos.
- [ ] Every major sales objection (migration, security/CNDP, TCO, adoption) is answered before the final CTA.
- [ ] Mobile (`375px`) and Desktop (`1440px`) viewports verified free of clipping, CLS, and dead links.
