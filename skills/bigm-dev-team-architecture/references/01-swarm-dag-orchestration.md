# 01 — Swarm Wave Planning, File-Boundary DAGs & Cost Guardrails

Load this playbook before decomposing a multi-file feature, sprint, or full product build into parallel subagents.

## 1. Why `@cto` Direct Swarm Beats Middle-Management Chains

Production telemetry from Hermes Agent proved two structural failure modes in multi-agent engineering:
1. **Multi-Hop Latency:** Routing CEO → `@coo` → `@archon` → `@scrum-lead` → `@forge` created telephone-game spec drift and duplicate board edits. Having the main agent operate directly as **Hands-On `@cto`** collapses planning + architecture into **Wave 0** and cuts lead time in half.
2. **Uncached Frontier Burn:** Running Claude Sonnet/Opus in uncached loops or on routine UI tasks burned **20x input cost** (108.9M uncached tokens in a single build). Enforce strict tiering:
   - **T0 (`@cto`, `@veritas`, `@pixel` architecture):** Main model / `Model="inherit"` (~20% combined).
   - **T1 (Critical Security, Multi-Tenant RLS, Money/Checkout State Machines):** `scripts/claude_critical_run.py` (`--tier sonnet` tries unmetered `agy` first; `--tier opus` for P0 architecture deadlocks; verifies `cache_read_tokens > 0` on API fallback) (~10%).
   - **T2 (Parallel Volume Execution — `@forge-fe`, `@forge-be`, `@datum`, `@bastion`):** `Model="flash"` (~70%).

## 2. Disjoint File-Ownership Partitioning (Zero Git Collisions)

Parallel subagents sharing a repository (`Workspace="share"`) collide if two workers edit the same file, barrel export (`index.ts`), `package.json`, or migration timestamp.

### Partitioning Rules for `@cto`
1. **Lock Shared Barrels & Dependencies in Wave 0:** Install shared npm/pip packages, database types (`packages/shared`), design tokens (`packages/ui`), and route registries **before** Wave 2 fan-out. If a Wave 2 worker discovers a missing root dependency, it messages `@cto` rather than editing root `package.json` mid-wave.
2. **Assign Explicit `owned_globs` & `readonly_globs` per Worker:**
   - Worker A (`@forge-fe`, Issue #12): `apps/web/src/features/catalog/**`, `apps/web/src/app/(app)/catalog/**`
   - Worker B (`@forge-fe`, Issue #13): `apps/web/src/features/orders/**`, `apps/web/src/app/(app)/orders/**`
   - Worker C (`@forge-be`, Issue #14): `supabase/migrations/20261110_01_orders_rpc.sql`, `packages/api/src/orders/**`
3. **Deterministic Preflight Check (Mandatory Before `invoke_subagent`):**
   Write the wave manifest to scratch JSON and run:
   ```bash
   python scripts/swarm_preflight.py check-overlap scratch/wave2.json
   ```
   Do **not** invoke subagents until `check-overlap` exits `0` (`OVERLAP_CHECK: PASS`).

## 3. Dependency Graph Rules (Unlink Artificial User-Journey Chains)

- **Bad DAG (Serial Bottleneck):** `Login Screen → Dashboard → Catalog → Cart → Checkout → Admin` (6 sequential waves = 6x wall-clock time).
- **Good DAG (Star Fan-Out from Foundation Gate):**
  - **Wave 0:** `@cto` (`packages/shared` + auth contract + DB schema spec) ∥ `@pixel` (`DESIGN.md` + `packages/ui`) ∥ `@bastion` (CI + repo shell).
  - **Wave 1:** `@veritas` Foundation Gate (`VERDICT: PASS`).
  - **Wave 2 (All Parallel!):** `Auth UI` ∥ `Dashboard UI` ∥ `Catalog UI` ∥ `Orders API + RLS` ∥ `CSV Importer (@datum)`. Because typed contracts (`packages/shared`) and UI primitives (`packages/ui`) already exist on `main`, all 5 workers build simultaneously without blocking one another!
  - **Wave 3:** `@veritas` Integration, E2E & Visual Parity Gate.

## 4. Long-Running Commands & Worktree Hygiene

1. **Async Command Timeouts:** Heavy builds (`npm ci`, `next build`, Playwright E2E) get cut off if run with tiny foreground timeouts. Use generous `WaitMsBeforeAsync` (`5000`–`10000`) and let background tasks finish via reactive notification—never busy-poll with `sleep`.
2. **Ban Recursive `**` Globs Over Worktrees:** Worktrees and LSP caches contain nested `node_modules` and `.next` trees that freeze directory walks for 300s+. Scope all searches to explicit `src/`, `packages/`, `apps/`, or `docs/` subdirectories.
3. **Branch Discipline:** Every subagent works on `feat/<issue#>-<slug>` branched from verified `main`. Workers run `lint` + `typecheck` + unit tests locally before opening a PR (`Closes #<issue#>`).

## 5. 3-Tier Swarm Failure Recovery & Hard-Stop Protocol

| Tier | Trigger | `@cto` Action |
| :--- | :--- | :--- |
| **Tier 1 — Surgical Nudge** | Single lint/type/test failure or minor AC gap | Use `send_message(Recipient=<convId>, Message=...)` with exact error output + fix instruction. Preserves worker context at minimal token cost. |
| **Tier 2 — Kill & Re-Architect** | Worker fails twice on the same bug, violates file boundaries, or stalls | Call `manage_subagents(Action="kill", ConversationIds=[<convId>])`. `@cto` (or `claude_critical_run.py --tier opus`) updates the spec/contract and spawns a clean replacement worker. |
| **Tier 3 — Human / CEO Escalation** | Missing client credentials, physical SMS/device UAT, legal/CNDP question, or scope conflict | Tag `[HUMAN-GOONLINE]` / `[HUMAN-COPILOTE]` (1 batched Lark message) or escalate scope/budget decisions with numbered options + recommended default to CEO. |

### Emergency Stop Commands
- **`"stop updates"`:** Cancel any scheduled timers (`manage_task`), stop non-essential status chatter, and confirm in ≤3 lines.
- **`"stop build"`:** Immediately execute `manage_subagents(Action="kill_all")`, kill running background build tasks via `manage_task`, and output a concise status ledger of merged vs. aborted branches.
