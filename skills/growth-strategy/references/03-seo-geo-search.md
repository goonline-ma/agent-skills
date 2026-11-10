# 03 — Unified SEO, GEO / AI Search & Programmatic Architecture

Use for search visibility strategy across Google Organic, Google AI Overviews (AIO), ChatGPT Search, Perplexity, Claude, Gemini, and Bing Copilot—covering index access, citability engineering, topic clusters, comparison pages, and programmatic SEO.

*(For automated multi-page crawls or PDF client reports, invoke `seo-audit`, `geo-audit`, or `geoskills-cli`—or enable the `seo-geo-deep-suite` plugin in Antigravity—after locking strategy here.)*

## 1. Layer 1 — Hard Index & AI Crawler Prerequisites (Check First)

Content tweaks fail if engines cannot crawl, render, or index the site:
1. **Dual-Index Baseline:**
   - **Google Search Console:** Entry ticket for Google Organic, AI Overviews, and Gemini.
   - **Bing Webmaster Tools + IndexNow:** Mandatory entry ticket for ChatGPT Search and Copilot.
2. **Server-Side Rendering (SSR):** AI retrieval bots (`OAI-SearchBot`, `PerplexityBot`, `ClaudeBot`) rarely execute heavy client-side JS bundles. Core copy, pricing/specs, JSON-LD, and internal links must exist in initial SSR/SSG HTML.
3. **Crawler Access vs Training Separation (`robots.txt` + WAF/Cloudflare):**
   - **Allow Search/Citation Bots:** `Googlebot`, `Bingbot`, `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Claude-SearchBot`, `Applebot`. Check Cloudflare Bot Fight Mode / WAF rules so agent user-agents are not 403-challenged.
   - **Optional Training Control:** `GPTBot`, `Google-Extended`, `CCBot` control model *training* separately from live search citations—decide deliberately per client policy.
   - **Snippet Traps:** Strip accidental `nosnippet` or restrictive `max-snippet` meta/X-Robots-Tag directives on public pages; they kill both AIO and LLM citations.
4. **`/llms.txt` Reality Check:** Treat `/llms.txt` as a **canonical anti-hallucination facts hedge** (concise company identity, exact pricing/compliance boundaries, canonical URL map)—**not** a primary ranking/citation lever.

## 2. Layer 2 — GEO Citability & Shortlist Engineering

Traditional SEO earns **rank**; GEO earns **passage extraction + shortlist recommendation**:
1. **Information-Gain Gate:** Before briefing any searchable page, inspect top results and write **one sentence** stating the net-new asset your page adds (original benchmark/dataset, interactive calculator/template, verified architecture teardown, regulatory table). No net-new gain = do not publish.
2. **Extractable Answer Blocks:**
   - Mirror real buyer fan-out questions in `H2`/`H3` headings.
   - Immediately follow key headings with a **self-contained 40–60 word direct answer** (subject named explicitly—no pronouns like *"It offers..."* that lose meaning when chunked) before expanding with nuance.
   - Replace prose walls with structured comparison tables, numbered procedures, and dated primary-source stats (+30–40% GEO lift when verifiable stats + citations are present).
3. **Citations vs. Shortlist Recommendations Gap:**
   - Being *cited* on an informational blog post does not put your brand on *"Best X for Y in [Region]"* shortlists.
   - LLMs synthesize shortlists from **entity consensus across third-party surfaces**: YouTube video titles/chapters/transcripts (highest AIO domain correlation), Reddit/community threads, LinkedIn articles, G2/Capterra/directory profiles, and press/partner mentions. Align exact category + use-case phrasing across all owned and third-party profiles.
4. **Entity Disambiguation (`Schema.org` JSON-LD):**
   - Schema does not force LLM citations on weak content, but earns Google Rich Results and eliminates entity ambiguity. Ship validated `Organization` (`sameAs`, official address/ICE/contact), `WebSite`, `SoftwareApplication`/`Product` (`offers`), `BreadcrumbList`, and `FAQPage` (where visible on-page).

## 3. Layer 3 — High-Intent Page Architecture & Programmatic SEO

Prioritize bottom-of-funnel (BoFu) revenue pages before top-of-funnel (ToFu) volume:
1. **Priority Build Order:**
   - **BoFu Commercial:** Category/Service Pillars → Competitor Comparisons (`[Brand] vs [Rival]`, `Best [Rival] Alternatives` using honest `● / ◐ / ○` capability matrices) → Persona × Use-Case pages (`[Product] for [Moroccan Fiduciaires / Multi-Site Restaurants]`).
   - **MoFu Authority:** Migration/Implementation Playbooks (e.g., *Sage 100 to Cloud PCGM Guide*), Regulatory Compliance Guides (e.g., *Law 69-21 Penalty Calculator & Guide*), Interactive ROI/TCO Tools.
   - **ToFu Hub-and-Spoke:** 1 comprehensive Pillar (`/guides/<topic>`) interlinked bidirectionally with 5–10 specific Spokes. Every spoke links back to the hub + 2 sibling spokes + 1 commercial BoFu page.
2. **Programmatic SEO (pSEO) Anti-Bloat Safeguards:**
   - Never ship `[Keyword] + [City]` mad-lib swaps. Require **≥ 40% unique structured data per page** (local regulations, verified directory entries, pricing benchmarks, inventory, or case proofs).
   - Gate indexation (`noindex` or hold back) on any generated URL lacking minimum data density; roll out in batches of 50–100 URLs while monitoring GSC `Crawled - currently not indexed`.
3. **Multilingual / `hreflang` Discipline:** Include self-referencing `hreflang` (`fr-MA`, `en`, `ar-MA`, plus `x-default`), reciprocal links across all language variants, and culturally native keyword targets (never literal word-for-word slug translations).

## Verification Checklist
- [ ] SSR HTML contains primary H1, answer blocks, internal links, and valid JSON-LD without JS execution.
- [ ] `robots.txt`, meta robots, and WAF allow `Googlebot`, `Bingbot`, `OAI-SearchBot`, `PerplexityBot`, and `Claude-SearchBot`.
- [ ] Every target page passes the Information-Gain Gate and links cleanly into a BoFu conversion path.
