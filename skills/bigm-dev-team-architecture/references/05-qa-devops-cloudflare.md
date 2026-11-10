# 05 — Independent QA (`@veritas`), GitHub Projects v2 & Cloudflare Shipping

Load this playbook when seeding/updating the `goonline-ma` GitHub Project v2 board, running `@veritas` Wave 1/Wave 3 QA gates, or deploying to Cloudflare.

## 1. GitHub Projects v2 (`goonline-ma`) — Single Source of Truth

- **Org Ground Truth:** Always target GitHub organization **`goonline-ma`** (authenticated as `BigMSolutions` with `repo, project, read:org, workflow` scopes). Never target `goonline` (unrelated third-party user account).
- **Card Lifecycle:** `Backlog` → `Ready` → `In progress` → `In review` → `Done`.
- **Labels:** `ai-execution`, `human-goonline`, `human-copilote`, `needs-decision`, `p0`, `p1`, `type:feat`, `type:fix`.
- **Mandatory Fresh `gh` Reads:** Never claim CI is green, a PR is conflict-free, or an issue is updated from memory. Run `scripts/board.py`:
  ```bash
  # List Project v2 items and statuses
  python scripts/board.py list --org goonline-ma --project <num>

  # Move issue card status
  python scripts/board.py status <issue#> "In progress" --org goonline-ma --project <num>

  # Post @veritas verdict or implementation evidence
  python scripts/board.py comment <issue#> "VERDICT: PASS ..." --org goonline-ma --repo <slug>

  # Fresh verification of PR checks + mergeability before squash-merging
  python scripts/board.py verify-pr <pr#> --org goonline-ma --repo <slug>
  ```

## 2. `@veritas` 3-Round Independent Acceptance Protocol

**Iron Law:** An implementer subagent (`@forge-fe`, `@forge-be`, `@datum`, `@synapse`, `@bastion`) **never** grades its own work or closes its own GitHub issue. `@veritas` (`Model="inherit"`, `Workspace="share"`) executes 3 cold rounds:

### Round 1 — Cold Diff & Contract Audit
1. Read the issue's Given/When/Then Acceptance Criteria (AC), `docs/DECISIONS.md`, and `DESIGN.md`.
2. Inspect `git diff main...HEAD`:
   - Did the worker stay strictly inside its `owned_globs`?
   - Are there any TODO stubs, mock arrays pretending to be DB calls, hardcoded hex colors bypassing `packages/ui`, or missing error/empty states?

### Round 2 — Live Execution, RLS Probes & Visual Browser QA
1. Run full workspace verification independently (`lint`, `typecheck`, unit + integration suites).
2. Run the cross-tenant SQL RLS matrix (`Tenant A ≠ Tenant B`, `anon` blocked) on any backend/DB change.
3. For any UI/frontend change, inspect the live rendered app via **`chrome-devtools-mcp`** (or Playwright):
   - Check `375×812` (mobile) and `1440×900` (desktop), plus `dir="rtl"` if multilingual.
   - Verify `list_console_messages` (zero uncaught errors/hydration mismatches) and `list_network_requests` (zero unexpected 4xx/5xx).
   - Compare rendered layout, spacing, typography, and focus rings against `@pixel`'s Figma screenshot / `DESIGN.md`.

### Round 3 — Secret & Bundle Scan + Verdict
1. Run `python scripts/swarm_preflight.py scan-secrets .` across working tree and build output (`dist/`, `.next/`).
2. Post structured comment via `board.py comment`:
   - **`VERDICT: PASS`** (includes exact commands run, exit codes, RLS count, and viewport check summary) → `@cto` squash-merges PR, closes issue, and sets status to `Done`.
   - **`VERDICT: FAIL`** (includes numbered `file:line` blockers and reproduction steps) → `@cto` moves card back to `In progress` and triggers Tier-1 `send_message` fix or Tier-2 respawn.

## 3. Cloudflare Deployment Protocol (`@bastion`)

> **MANDATORY GLOBAL RULE:** When interacting with Cloudflare, **always use the `cf` CLI** **unless** the project has a Wrangler configuration file (`wrangler.toml` or `wrangler.json` / `wrangler.jsonc`), in which case use `wrangler`.

### Pre-Deploy Checklist
- [ ] `@veritas` `VERDICT: PASS` recorded on milestone/release issues.
- [ ] `python scripts/swarm_preflight.py scan-secrets <dist_or_repo>` exits `0` (zero `service_role` JWTs, `.env` files, or private keys in client assets).
- [ ] `board.py verify-pr` / `main` CI checks (`verify`, `secret-scan`, `rls-policies`) are green.
- [ ] Forward/backward DB migrations verified on staging before production code cutover.

### Deploy & 120-Second Rollback Gate
1. **Check project root for `wrangler.toml` / `wrangler.json` / `wrangler.jsonc`:**
   - **Absent:** Execute Cloudflare Pages / Workers / DNS / Zero Trust operations via the **`cf` CLI**.
   - **Present:** Execute via **`wrangler`** (`npx wrangler pages deploy <dist> --project-name=<slug>` or `npx wrangler deploy --env staging|production`).
2. **Post-Deploy Smoke Check (≤120s):**
   - Verify HTTP `200`, security headers, auth flow, and primary API health endpoint on the live URL.
   - If any smoke check fails within **120 seconds**, `@bastion` rolls back immediately (`cf` rollback or `npx wrangler rollback`) before investigating root cause.

## 4. Human Pool Dispatch Hygiene (`[HUMAN-GOONLINE]` & `[HUMAN-COPILOTE]`)

- Create a well-scoped GitHub issue in French (context, exact deliverable, checkbox AC, due date, `--assignee`, label `human-goonline` or `human-copilote`) and add it to the Project v2 board.
- **Lark Quota Discipline (~10,000 API calls/month shared):** Send **at most one batched summary table per channel** (`#goonline-dispatch`, `#copilote-dispatch`), never per-task notification spam, and respect Moroccan working hours (Mon–Fri, `Africa/Casablanca`).
