#!/usr/bin/env python3
"""Deterministic Growth & Unit Economics Calculator (Zero Mental Math).

Subcommands:
  economics  Compute LTV, LTV:CAC, CAC payback (months), and max allowable CPL/CPC.
  funnel     Reverse-engineer revenue goal into required deals, SQLs, leads, clicks, and budget.
  score      Rank growth experiments by RICE or ICE from JSON input or inline arguments.
"""
import argparse
import json
import math
import sys


def cmd_economics(args: argparse.Namespace) -> int:
    monthly_rev = args.arpu_monthly
    gross_margin_monthly = monthly_rev * args.gross_margin
    if args.churn_monthly <= 0 or args.churn_monthly >= 1:
        sys.exit("Error: --churn-monthly must be between 0 and 1 (e.g. 0.03 for 3%).")

    avg_lifetime_months = 1.0 / args.churn_monthly
    ltv = gross_margin_monthly * avg_lifetime_months
    ltv_cac = ltv / args.cac if args.cac > 0 else float("inf")
    payback_months = args.cac / gross_margin_monthly if gross_margin_monthly > 0 else float("inf")

    max_cac_for_target = ltv / args.target_ltv_cac
    max_cpl = max_cac_for_target * args.lead_to_close_rate
    max_cpc = max_cpl * args.click_to_lead_rate

    result = {
        "monthly_gross_profit": round(gross_margin_monthly, 2),
        "avg_lifetime_months": round(avg_lifetime_months, 1),
        "ltv": round(ltv, 2),
        "cac": round(args.cac, 2),
        "ltv_to_cac": round(ltv_cac, 2),
        "cac_payback_months": round(payback_months, 2),
        "max_allowable_cac": round(max_cac_for_target, 2),
        "max_allowable_cpl": round(max_cpl, 2),
        "max_allowable_cpc": round(max_cpc, 2),
        "healthy": ltv_cac >= args.target_ltv_cac and payback_months <= 12.0,
    }
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    status = "PASS" if result["healthy"] else "WARN (check LTV:CAC >= target & Payback <= 12m)"
    print(f"## Unit Economics Audit — {status}\n")
    print("| Metric | Value |")
    print("| :--- | ---: |")
    print(f"| Monthly Gross Profit / Account | {result['monthly_gross_profit']:,.2f} |")
    print(f"| Implied Lifetime (months) | {result['avg_lifetime_months']:,.1f} |")
    print(f"| Gross-Margin LTV | {result['ltv']:,.2f} |")
    print(f"| Current / Planned CAC | {result['cac']:,.2f} |")
    print(f"| **LTV : CAC Ratio** | **{result['ltv_to_cac']:.2f}x** (target >= {args.target_ltv_cac:.1f}x) |")
    print(f"| **CAC Payback Period** | **{result['cac_payback_months']:.1f} months** (target <= 12m) |")
    print(f"| Max Allowable CAC (@ {args.target_ltv_cac:.1f}x) | {result['max_allowable_cac']:,.2f} |")
    print(f"| Max Allowable CPL (@ {args.lead_to_close_rate*100:.1f}% L->Close) | {result['max_allowable_cpl']:,.2f} |")
    print(f"| Max Allowable CPC (@ {args.click_to_lead_rate*100:.1f}% Click->L) | {result['max_allowable_cpc']:,.2f} |")
    return 0


def cmd_funnel(args: argparse.Namespace) -> int:
    if args.acv <= 0:
        sys.exit("Error: --acv must be > 0.")
    for name, val in [
        ("sql-to-close", args.sql_to_close),
        ("lead-to-sql", args.lead_to_sql),
        ("visit-to-lead", args.visit_to_lead),
    ]:
        if val <= 0 or val > 1:
            sys.exit(f"Error: --{name} must be in (0, 1].")

    deals = math.ceil(args.revenue_goal / args.acv)
    sqls = math.ceil(deals / args.sql_to_close)
    leads = math.ceil(sqls / args.lead_to_sql)
    visits = math.ceil(leads / args.visit_to_lead)
    budget = visits * args.cpc if args.cpc > 0 else leads * args.cpl
    implied_cac = budget / deals if deals > 0 else 0.0

    result = {
        "revenue_goal": round(args.revenue_goal, 2),
        "acv": round(args.acv, 2),
        "required_deals": deals,
        "required_sqls": sqls,
        "required_leads": leads,
        "required_visits": visits,
        "estimated_budget": round(budget, 2),
        "implied_cac": round(implied_cac, 2),
    }
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("## Reverse-Engineered GTM Funnel\n")
    print("| Funnel Stage | Required Volume | Conversion Assumption |")
    print("| :--- | ---: | :--- |")
    print(f"| Target Revenue | {result['revenue_goal']:,.2f} | ACV = {result['acv']:,.2f} |")
    print(f"| Closed-Won Deals | {deals:,} | {args.sql_to_close*100:.1f}% SQL -> Close |")
    print(f"| Qualified SQLs / Demos | {sqls:,} | {args.lead_to_sql*100:.1f}% Lead -> SQL |")
    print(f"| Captured Leads / Signups | {leads:,} | {args.visit_to_lead*100:.1f}% Visit -> Lead |")
    print(f"| Qualified Visits / Clicks | {visits:,} | Top-of-funnel traffic |")
    if budget > 0:
        print(f"| **Estimated Media/Outbound Budget** | **{result['estimated_budget']:,.2f}** | **Implied CAC = {result['implied_cac']:,.2f}** |")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    raw = open(args.input, encoding="utf-8").read() if args.input != "-" else sys.stdin.read()
    items = json.loads(raw)
    if not isinstance(items, list) or not items:
        sys.exit("Error: input JSON must be a non-empty array of experiment objects.")

    mode = args.mode.upper()
    scored = []
    for it in items:
        name = it.get("name", "Unnamed")
        if mode == "RICE":
            reach = float(it["reach"])
            impact = float(it["impact"])
            confidence = float(it["confidence"])
            effort = max(float(it["effort"]), 0.1)
            val = (reach * impact * confidence) / effort
            scored.append({**it, "score": round(val, 2)})
        else:
            impact = float(it["impact"])
            confidence = float(it["confidence"])
            ease = float(it["ease"])
            val = impact * confidence * ease
            scored.append({**it, "score": round(val, 1)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    if args.json:
        print(json.dumps(scored, indent=2))
        return 0

    print(f"## Prioritized Experiment Backlog ({mode})\n")
    if mode == "RICE":
        print("| Rank | Experiment | Reach | Impact | Conf. | Effort | RICE Score |")
        print("| :---: | :--- | ---: | ---: | ---: | ---: | ---: |")
        for idx, s in enumerate(scored, 1):
            print(f"| {idx} | {s['name']} | {s['reach']} | {s['impact']} | {s['confidence']} | {s['effort']} | **{s['score']}** |")
    else:
        print("| Rank | Experiment | Impact | Conf. | Ease | ICE Score |")
        print("| :---: | :--- | ---: | ---: | ---: | ---: |")
        for idx, s in enumerate(scored, 1):
            print(f"| {idx} | {s['name']} | {s['impact']} | {s['confidence']} | {s['ease']} | **{s['score']}** |")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Deterministic Growth & Unit Economics Calculator")
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("economics", help="Audit LTV, CAC, payback, and max allowable CPL/CPC")
    pe.add_argument("--arpu-monthly", type=float, required=True, help="Monthly revenue per account")
    pe.add_argument("--gross-margin", type=float, default=0.80, help="Gross margin fraction (default 0.80)")
    pe.add_argument("--churn-monthly", type=float, required=True, help="Monthly logo/revenue churn fraction (e.g. 0.025)")
    pe.add_argument("--cac", type=float, required=True, help="Current or target Customer Acquisition Cost")
    pe.add_argument("--target-ltv-cac", type=float, default=3.0, help="Minimum healthy LTV:CAC ratio (default 3.0)")
    pe.add_argument("--lead-to-close-rate", type=float, default=0.05, help="Lead-to-customer conversion fraction")
    pe.add_argument("--click-to-lead-rate", type=float, default=0.04, help="Landing page click-to-lead fraction")
    pe.add_argument("--json", action="store_true")
    pe.set_defaults(func=cmd_economics)

    pf = sub.add_parser("funnel", help="Reverse-engineer revenue target into funnel volumes & budget")
    pf.add_argument("--revenue-goal", type=float, required=True)
    pf.add_argument("--acv", type=float, required=True, help="Average annual/contract deal value")
    pf.add_argument("--sql-to-close", type=float, default=0.25)
    pf.add_argument("--lead-to-sql", type=float, default=0.25)
    pf.add_argument("--visit-to-lead", type=float, default=0.03)
    pf.add_argument("--cpc", type=float, default=0.0, help="Average cost per click (optional)")
    pf.add_argument("--cpl", type=float, default=0.0, help="Average cost per lead (optional if --cpc not set)")
    pf.add_argument("--json", action="store_true")
    pf.set_defaults(func=cmd_funnel)

    ps = sub.add_parser("score", help="Score experiments via RICE or ICE from JSON file or '-' stdin")
    ps.add_argument("input", help="Path to JSON list of experiments, or '-' for stdin")
    ps.add_argument("--mode", choices=["rice", "ice", "RICE", "ICE"], default="rice")
    ps.add_argument("--json", action="store_true")
    ps.set_defaults(func=cmd_score)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
