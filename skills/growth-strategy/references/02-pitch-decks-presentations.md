# 02 — Pitch Decks, Sales Enablement & Brand-Matched Presentations

Use when crafting, challenging, or redesigning sales pitch decks, client marketing strategy decks, investor/accelerator decks, or executive presentations. **Output must be a finished, rendered, visually inspected `.pptx` + `.pdf`—never a text-only outline unless explicitly requested.**

## 1. Select Deck Mode & Storyline

| Mode | Trigger | Canonical Slide Arc (≤ 15 slides unless specified) | Hard Content Rules |
| :--- | :--- | :--- | :--- |
| **A. CEO / B2B Sales Deck** | Pre/post-call company or product pitch | 1. Title + Promise → 2. Prospect Context / Industry Shift → 3. Cost of Status Quo → 4. Our Platform / Architecture → 5. Key Capabilities (3 pillars, real UI) → 6. Shipped Case Studies / Proof → 7. Delivery & Governance → 8. Next Steps & Contact | **Zero pricing, packages, or discounts.** Zero placeholders. Real company/product screenshots only—never AI people/offices. |
| **B. Client Marketing / Challenge Deck** | Brief/spec handed over: "challenge & craft best pitch" | 1. Title + Promise → 2. Sourced Market Reality → 3. Real Competitor (entrenched habit + rivals) → 4. Buyer-Job Insight → 5. Big Idea + 3 Pillars → 6. Single Hero Argument → 7. Persona + Levers → 8. Forgotten Gatekeeper (e.g., distributors/partners) → 9. Credibility Rules (*On ne dit pas / On dit*) → 10. 12-Month Seasonal Plan → 11. Creative Engine & Month-1 Calendar → 12. Retention/Push Timing → 13. KPI Funnel → 14. Contact | **Spec beats brainstorm:** build a 3-column *Claim → Spec Reality → Honest Fix* challenge table first. Never promise unbuilt finance/delivery mechanics. |
| **C. Investor / Accelerator Deck** | Fundraising, grant, referencing, or demo day | 1. Hook + Traction Headline → 2. Problem → 3. Why Now → 4. Solution (real product UI) → 5. Mechanism / Defensibility → 6. Market Size (bottom-up math) → 7. Business Model → 8. Traction → 9. Go-To-Market → 10. Competitor Matrix (`●` native / `◐` partial / `○` absent—no brittle rival prices) → 11. Team → 12. Regional Ask + Network Intros | Never invent raise terms, LOIs, or CAC/LTV. Label illustrative scale math explicitly. |

## 2. Source Ingestion & Spec Challenge

1. **Ingest all sibling files first:** Read `.pptx` (skip `~$` lock files), `.docx` (paragraphs + tables in order), and `.pdf` (if text layer is empty, render pages via `pypdfium2` and inspect visually).
2. **Source Precedence:** CEO-confirmed facts > Signed CdCF / Functional Spec > Live Website > Aspirational brainstorms. If the live domain is "coming soon", state that plainly.
3. **Localization Realism:** For Moroccan B2B/artisan decks, use French for slide structure, Latin-script Darija for artisan taglines/push notifications (plan AR + Latin subtitles for video), and compute real seasonal peaks (pre-Ramadan, pre-Aïd al-Adha) in Python—never guess dates.

## 3. Brand Token Extraction & `python-pptx` Engineering

1. **Extract Brand Tokens:** Fetch the target website HTML/CSS (`/_next/static/chunks/*.css` or stylesheets). Extract `--color-*`, `--background`, surface/border hexes, font families, logo, and real product screenshots (compress PNGs to ~1600px JPG q≈86).
2. **Logo Alpha Fix:** Transparent RGBA logos often show box edges or crop poorly. Alpha-composite onto white to find tight pixel bounds (`min(RGB) < 200`), or mount inside a pure `#FFFFFF` pill/card rather than off-white.
3. **Font Discipline:** Download static TTF weights if needed (`https://cdn.jsdelivr.net/fontsource/fonts/<id>@latest/latin-<weight>-normal.ttf`), inspect `nameID 1` via `fontTools`, reference explicit weight family names (e.g., `Geist SemiBold` rather than `bold=True`), and set `font.name` plus XML `a:latin`, `a:ea`, and `a:cs` on every run so PowerPoint never falls back. Set `●◐○` symbols in `Segoe UI Symbol`.
4. **Slide Geometry Rules (16:9 = `13.333in × 7.5in`, Blank Layout 6):**
   - Full-bleed background rectangle on every slide; `shape.shadow.inherit = False`; zero textbox margins with explicit `word_wrap = True`.
   - Eyebrow `NN / SECTION` in tracked monospace (`rPr.set('spc', '180')`).
   - **Single-line Title Rule:** Keep 30pt titles ≤ 48 characters (`w <= 11.8in`) so titles never wrap onto fixed-`y` subtitles. Shorten copy—do not shrink font size.
   - **Right/Bottom Bounds:** Enforce `x + w <= 13.0in` and `y + h <= 7.2in`. Put source citations in a clean bottom-left footer (`NN / TOTAL` bottom-right) and speaker notes on every slide.

## 4. Mandatory Render, Lint & Visual QA Loop

Never deliver an unrendered `.pptx`. Run both structural lint and visual inspection:

1. **Structural & Bounds Audit:**
   ```powershell
   python "<skill_dir>/scripts/deck_qa.py" check path/to/deck.pptx
   ```
   Fix every reported right/bottom margin overflow, >48-char title wrap risk, or banned placeholder token (`TODO`, `TBD`, `Lorem`).
2. **Exact PowerPoint COM Render + Embedded Export (Windows):**
   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File "<skill_dir>/scripts/render_deck_windows.ps1" -src "C:\abs\draft.pptx" -outdir "C:\abs\render" -embedded "C:\abs\Final_Deck.pptx" -pdf "C:\abs\Final_Deck.pdf"
   ```
3. **Contact-Sheet Visual QA:**
   ```powershell
   python "<skill_dir>/scripts/deck_qa.py" grid "C:\abs\render" "C:\abs\qa_grids"
   ```
   Read every generated `grid_XX.png` (and `s01.png` at full resolution) with `read_file` to inspect visually for text overlap, clipped cards, low contrast, or awkward empty space. Patch the builder script and re-render until zero visual defects remain.

## Verification Checklist
- [ ] `deck_qa.py check` exits 0 (zero bounds overflows, zero placeholder tokens).
- [ ] Every slide carrying external data has a source line; zero pricing in sales/company decks.
- [ ] Contact sheets inspected visually after final re-render; both font-embedded `.pptx` and `.pdf` produced.
