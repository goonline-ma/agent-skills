# 04 — Architecture, Typed Contracts, Multi-Tenant RLS & T1 Security Gate

Load this playbook during Wave 0 (`@cto` architecture & contracts) and whenever a task touches authentication, multi-tenant data isolation, financial/voucher transactions, or critical security.

## 1. Wave 0 Baseline Artifacts (`@cto` Commits Before Fan-Out)

Before spawning parallel Wave 2 coding subagents, `@cto` ensures `main` contains:
1. **`docs/SCOPE.md` & `docs/DECISIONS.md`:**
   - Ground scope in the signed SOW/CdCF (never unverified pitch claims).
   - Number every architectural/product decision `D-01..D-NN` and every open assumption `Q-01..Q-NN` (with a proposed default so the CEO can approve/override in one line).
2. **`docs/adr/NNNN-<slug>.md` (Architecture Decision Record):**
   ```markdown
   # NNNN. <Decision Title>
   Status: Accepted | Date: YYYY-MM-DD
   Context: Forces, constraints (latency, budget, CNDP Law 09-08, team skills).
   Decision: Exact stack, data boundary, and contract pattern chosen.
   Consequences: Trade-offs accepted + follow-on verification required.
   Alternatives Rejected: Options ruled out and why.
   ```
3. **`packages/shared` (Contract-First Source of Truth):**
   - Shared TypeScript interfaces, Zod/Valibot request/response schemas, error codes, RBAC permission enums, and generated DB types.
   - Once locked in Wave 0, `@forge-fe` and `@forge-be` build simultaneously against `packages/shared` with zero integration guesswork.

## 2. Multi-Tenant Database & RLS Non-Negotiables

1. **Database-Enforced Tenant Isolation:**
   - Every tenant-owned PostgreSQL table **must** have `ALTER TABLE <t> ENABLE ROW LEVEL SECURITY;` and `FORCE ROW LEVEL SECURITY;` with explicit `SELECT`, `INSERT`, `UPDATE`, and `DELETE` policies tied to `auth.uid()` / verified tenant membership helper (`SECURITY DEFINER` with locked `search_path = public`).
   - Application-layer `WHERE org_id = ?` filters are **never** sufficient on their own.
   - If using Cloud Firestore, **mandatory rule**: delegate authoring/editing `firestore.rules` to the specialist `firestore-rules-author` subagent and audit with `firebase-security-rules-auditor`.
2. **Idempotent & Atomic Money / Inventory / Voucher RPCs:**
   - Multi-step balance, stock, split-order, or voucher mutations must execute inside a **single transactional SQL RPC / serializable or `SELECT ... FOR UPDATE` lock** keyed by a client-supplied `idempotency_key` (`UNIQUE (tenant_id, idempotency_key)`).
   - Never compute totals, discounts, or VAT (`TVA 20%`) only on the client; server RPC recomputes from authoritative catalog rows.
3. **Migration Safety:**
   - Plan forward + backward migrations. Never run `DROP TABLE`, `DROP COLUMN`, or `TRUNCATE` on production schemas without an expand-migrate-contract cycle and CEO sign-off.
4. **Cross-Tenant Penetration Test Matrix (Required for `@veritas`):**
   - Every RLS migration ships with automated SQL/integration tests proving:
     - Tenant A **can** read/mutate Tenant A rows per role (`owner`, `admin`, `member`, `viewer`).
     - Tenant A gets **0 rows / permission denied** reading or updating Tenant B rows.
     - Anonymous (`anon`) callers get **0 rows / 401** on protected tables and RPCs.

## 3. T1 Critical Execution Gate (`claude_critical_run.py`)

Reserve **T1 (`~10%` of tasks)** strictly for:
- Multi-tenant SQL RLS policies & auth/RBAC middleware
- Financial checkout, split-order, ledger, or voucher state machines
- Cryptography, webhook signature verification (Stripe/CMI/Cloudflare Turnstile), and anti-abuse
- Tier-2 architectural deadlocks where two standard attempts failed

### Execution Protocol
1. Write a self-contained spec file (`scratch/t1_<slug>.md`) including exact schema DDL, invariants, edge cases, and test requirements.
2. Run:
   ```bash
   # Critical code / RLS / RPCs (attempts unmetered `agy` claude-sonnet-5-5-high first, then Nous):
   python scripts/claude_critical_run.py scratch/t1_<slug>.md --tier sonnet --cwd <worktree_path>

   # Deadlocked P0 architecture / security threat model:
   python scripts/claude_critical_run.py scratch/t1_<slug>.md --tier opus --out scratch/t1_adr.md
   ```
3. **Secret & Cache Guardrails Inside `claude_critical_run.py`:**
   - Automatically refuses execution (`exit 3`) if real `.env*` files exist in `--cwd`.
   - Routes API fallback to `nous` first so Anthropic prompt caching stays active, and prints `cache_read_tokens` telemetry so uncached loops are caught on Run #1.

## 4. Secret, Bundle & Privacy Hygiene (GDPR + Moroccan Law 09-08)

- **Zero Client Secret Leakage:** `SUPABASE_SERVICE_ROLE_KEY`, database URLs, webhook signing secrets, and private API keys must never carry `NEXT_PUBLIC_` / `VITE_` prefixes or appear in `dist/` bundles (`python scripts/swarm_preflight.py scan-secrets .`).
- **`.gitleaks.toml` Discipline:** Remember that CI scans full git history—a single fake-looking high-entropy key committed on one feature branch turns `secret-scan` red repo-wide. Use clearly labeled dummy fixtures (`test_placeholder_not_a_secret`) or narrow line-scoped `.gitleaks.toml` allowlists on `main`.
- **Law 09-08 (CNDP) & GDPR:** Log zero raw PII/passwords/tokens; include explicit consent + purpose notices on lead/auth forms; flag biometric, health, or cross-border personal data transfers for `[HUMAN-COPILOTE]` CNDP declaration review.
