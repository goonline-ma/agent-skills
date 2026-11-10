# 05 — Signal-Based Outbound, ABM, Cold Email & Sales Enablement

Use for B2B lead generation, Clay-style signal prospecting, cold email/LinkedIn sequences, pre-call CEO prospect dossiers, and turning shipped projects into case studies + lookalike ABM waves.

*(Hard governance: All outreach and dossiers are **draft-only** until explicit user/CEO sign-off. Comply strictly with GDPR and Moroccan Law 09-08 CNDP: business-role contacts from public/documented B2B sources only, clear opt-out, zero private data scraping.)*

## 1. Outbound Deliverability Prerequisites (Audit Before Sending)

Never burn the primary brand domain (`brand.com`) on cold outbound:
- **Isolated Infrastructure:** Warm 2–4 secondary domains (`getbrand.com`, `brand-hq.com`), max 2–3 mailboxes per domain, ≤ 35–50 cold emails/mailbox/day.
- **Authentication:** Valid `SPF`, `DKIM` (2048-bit), `DMARC` (`p=quarantine` or `reject`), custom tracking off (plain links or no tracking pixel on Touch 1).
- **Health Floors:** Hard bounce `< 2%` (verify catch-alls before queueing), spam complaint `< 0.1%`, Touch-1 plain text only (zero attachments, zero images, max 1 link—preferably zero links on Touch 1).

## 2. Signal-Based Prospecting Waterfall (Never Spray-and-Pray)

Segment accounts by **observable buying triggers** before writing a word:
- **Tier 1 — Strategic 1:1 ABM (10–25 accounts):** Custom research per account (CEO/VP target, tailored 1-page dossier + custom Loom/teardown).
- **Tier 2 — Signal-Triggered 1:Few (50–250 accounts):** Grouped by shared live signal:
  - *Hiring signal:* Job ads mentioning legacy stack (e.g., Sage Saari, manual reconciliation, multi-site POS ops).
  - *Regulatory/Market deadline:* Law 69-21 payment delay reporting, e-invoicing readiness, PACTE TPME digital subsidy windows.
  - *Digital/Tech gap:* Slow mobile checkout, broken reservation/order flow, missing AI/search visibility, new branch opening.
- **Tier 3 — Lookalike Case-Study Wave:** Exact sector + headcount + city Twins of a recently closed customer win.

## 3. Pre-Call CEO Prospect Dossier (1 Page Max, Fully Cited)

Run before every executive discovery call (register every URL in `scripts/citation_ledger.py`):
1. **Snapshot:** Offering, estimated headcount/locations, registry/corporate signals (e.g., OMPIC / `charika.ma` for MA firms), key decision-makers (public business roles only).
2. **Signals & Stack:** Live site stack, hiring priorities, recent 12-month press/expansion, UX/SEO friction spotted on their live site.
3. **3 Evidenced Pains:** Each tied to a concrete public signal (label inferences `[hypothesis]`).
4. **Value Hypothesis + Proof:** Match 1–2 specific offers + a shipped Big M / brand proof point + subsidy/program eligibility (e.g., Maroc PME PACTE TPME).
5. **5 Sharp Discovery Questions:** Diagnostic questions exposing cost of status quo (never leading feature pitches).
6. **Tailored Pitch Outline (5–7 slide titles, no pricing)** + **Sources (`[1]..[n]`)**.

## 4. The 4-Sentence "Poke-the-Bear" Cold Email (< 75 Words)

Read on mobile in 8 seconds. Cut *"I hope this finds you well"*, company history paragraphs, and 30-minute calendar asks:
1. **Subject (2–4 words, lowercase, internal-peer feel):** `sage migration`, `law 69-21 filings`, `[company] checkout`.
2. **Line 1 — Verified Signal:** Concrete observation proving why you wrote *them* *today* (zero fake flattery).
3. **Line 2 — Costly Problem Question:** Connect that signal to a specific bottleneck their role owns.
4. **Line 3 — Concrete Peer Proof:** 1 sentence with a real shipped mechanism + measured result.
5. **Line 4 — Zero-Friction Interest CTA:** Ask for interest or offer a concrete asset (*"Worth sending the 2-min teardown?"* / *"Open to seeing how [Peer/Sector] cut manual entry by 80%?"*)—send calendar link **only after** positive reply.

### 5-Touch Multi-Channel Sequence (14 Business Days)
- **Day 1 (Email 1):** 4-sentence Signal + Poke-the-Bear + Soft CTA (`< 75w`).
- **Day 2 (LinkedIn):** Blank or 1-line non-pitch connection request referencing shared market/signal.
- **Day 4 (Email 2 — Thread Reply):** Deliver a pure-value micro-asset (3-bullet site/workflow audit, benchmark table, or architecture diagram)—zero guilt-tripping (*"Just bumping this"* is banned).
- **Day 8 (LinkedIn DM / Voice Note):** Short peer angle or 45s teardown offer if connected.
- **Day 13 (Email 3 — New Angle + Clean Break):** Test a second stakeholder pain (e.g., risk/compliance vs speed) + polite permission to close loop.

## 5. Shipped Project → Case Study → ABM Engine

Whenever an engineering project ships (`@veritas` `VERDICT: PASS`):
1. **Permission Check:** Confirm whether client approved naming; if not, anonymize strictly (*"Casablanca 40-person textile distributor"*, zero logos/identifying numbers).
2. **Bilingual Case Study (FR + EN, 500–800w):** Context → Bottleneck → Plain-English Architecture → **Measured Outcomes Only** (zero invented KPIs) → Approved Quote.
3. **Derivative Pack:** 1 CEO LinkedIn post + 1 slide insert + 1 web blurb + 3-touch ABM sequence for 10–20 lookalike accounts.

## Verification Checklist
- [ ] Every touch is `< 85` words, mobile-scannable, plain-spoken, and free of AI clichés or unverified claims.
- [ ] Every factual claim in dossiers/case studies carries a verified source URL; pricing excluded unless CEO-approved.
