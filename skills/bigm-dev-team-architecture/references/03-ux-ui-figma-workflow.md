# 03 — UX/UI Design System & Figma-to-Code Workflow (`@pixel`)

Load this playbook whenever a build includes frontend screens, dashboards, mobile apps, landing pages, design systems, or Figma files.

## 1. Figma Plugin & Skill Stack Check

1. **Figma MCP Integration:**
   - Check whether the official **Figma** plugin (`antigravity-plugins-partners/plugin/figma`) is installed and signed in (`list_plugin_accounts`).
   - If the user provides a `figma.com` URL (or asks for Figma sync / Code Connect) and the Figma plugin is **not** yet installed, surface the official Marketplace card on its own line (`<plugin-card catalog-id="antigravity-plugins-partners/plugin/figma"></plugin-card>`) so they can add it in one click.
   - If Stitch MCP (`StitchMCP`) is active and no Figma file exists yet, `@pixel` can also prototype rapid screen variants or upload `DESIGN.md` via `StitchMCP` tools (`create_design_system_from_design_md`, `generate_screen_from_text`).
2. **Design Craft Skills:** Pair `@pixel` with installed `ui-ux-pro-max`, `frontend-design`, and `emil-design-eng` for typography pairing, tactile micro-interactions, and non-generic visual hierarchy.

## 2. Exact Figma-to-Production Pipeline (When Figma URL Is Provided)

Never eyeball a screenshot when node metadata and variables are available:
1. **Parse URL → `fileKey` & `nodeId`:**
   - Format `https://www.figma.com/design/<fileKey>/<fileName>?node-id=12-34` → `fileKey="<fileKey>"`, `nodeId="12:34"` (convert `-` to `:`).
2. **Pull Ground-Truth Structure & Tokens via Figma MCP:**
   - Call **`get_design_context`** (`fileKey`, `nodeId`) to extract auto-layout hierarchy, exact spacing/padding, typography scales, component instances, and Code Connect hints.
   - Call **`get_variable_defs`** (`fileKey`, `nodeId`) to extract Figma Variables (primitive & semantic color modes, radius, spacing tokens) rather than hardcoding raw hex strings.
   - Call **`get_screenshot`** (`fileKey`, `nodeId`) to capture the visual reference frame into the conversation scratch/artifact folder so both `@pixel` and `@veritas` compare live renders against the exact frame.
   - Call **`get_code_connect_map`** / **`add_code_connect_map`** so Figma components map 1:1 to `packages/ui` exports (`<Button>`, `<DataTable>`, `<StatCard>`) instead of regenerating duplicate bespoke markup per screen.
3. **Fallback When No Figma File Exists (Greenfield / Reference Brand):**
   - Inspect live client website/brand guidelines first (real logos, brand palette, domain tone).
   - Author **`DESIGN.md`** at the repo root **before** any `@forge-fe` worker writes JSX.

## 3. `DESIGN.md` & `packages/ui` Token Contract (Wave 0 Deliverable)

`@pixel` must ship `DESIGN.md` + `packages/ui` tokens covering:
1. **Semantic CSS Variables (Light/Dark + Brand Surface Hierarchy):**
   - Define `--bg-canvas`, `--bg-surface`, `--bg-elevated`, `--fg-primary`, `--fg-muted`, `--border-subtle`, `--brand-primary`, `--status-success/warn/danger` (using `oklch()` or HSL variables wired into Tailwind).
   - **Ban raw utility soup** (`bg-[#3b82f6]`) inside `apps/**` feature code; `@forge-fe` may only reference semantic tokens (`bg-surface`, `text-fg-primary`, `border-subtle`).
2. **Typography & Tabular Data:**
   - Intentional display + body + mono pairing; fluid scale with clear hierarchy; `font-variant-numeric: tabular-nums` (`tabular-nums`) mandatory on all prices, KPIs, counters, tables, and timestamps so digits never jitter.
3. **5-State Component Completeness Matrix:**
   Every reusable view/widget spec must define:
   - **Default (Populated):** Realistic domain copy & edge-case text truncation (`line-clamp`, overflow handling for 40-char French/Arabic labels).
   - **Loading:** Layout-matched skeleton (zero Cumulative Layout Shift `CLS < 0.1`).
   - **Empty:** Clear explanation + primary creation/import CTA.
   - **Error / Validation:** Inline field-level guidance (`aria-invalid`, `aria-describedby`) + non-destructive retry (preserve user form input!).
   - **Pending / Optimistic / Offline:** Immediate button feedback (`disabled` + spinner within `100ms`, prevent double-submit).

## 4. Accessibility (WCAG 2.2 AA), Mobile-First & Bilingual/RTL Rules

1. **Responsive Viewports:** Design mobile-first (`375px` × `812px`), tablet (`768px`), and desktop (`1440px`). Primary actions on mobile belong in thumb-reachable bottom bars/sheets with **`>= 44×44px`** hit targets.
2. **Bilingual LTR (`fr`, `en`) + RTL (`ar` / Darija) Native Support:**
   - Use **CSS Logical Properties exclusively**: `ps-*`/`pe-*`, `ms-*`/`me-*`, `start-*`/`end-*`, `text-start`/`text-end`, `border-s`/`border-e` (never `pl-*`/`pr-*`/`ml-*`/`mr-*`/`left-*`/`right-*` on directional chrome).
   - Flip directional chevrons/arrows in `dir="rtl"` (`rtl:rotate-180`), while keeping phone numbers, IBANs, code snippets, and math LTR (`dir="ltr"`).
3. **Motion Discipline (Emil Kowalski Standard):**
   - Animate **only `transform` and `opacity`** (`150ms–220ms` crisp ease-out `cubic-bezier(0.23, 1, 0.32, 1)` for UI micro-interactions; never bouncy springs on enterprise tables/forms).
   - Always include `@media (prefers-reduced-motion: reduce)` fallbacks.

## 5. `@pixel` → `@forge-fe` → `@veritas` Visual Parity Handoff

1. `@pixel` commits `DESIGN.md` + `packages/ui` primitives + component mapping table in Wave 0.
2. `@forge-fe` builds feature routes in Wave 2 strictly importing `packages/ui`.
3. `@veritas` opens the running app in `chrome-devtools-mcp` (`resize_page` at `375x812` and `1440x900`, plus `dir="rtl"` toggle), captures screenshots, checks `get_css_styles` & `lighthouse_audit` accessibility, and rejects (`VERDICT: FAIL`) any spacing drift, clipped French/Arabic strings, contrast failures, or raw hex overrides.
