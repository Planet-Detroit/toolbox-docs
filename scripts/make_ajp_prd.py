#!/usr/bin/env python3
"""Produce the AJP/partner-facing edition of the PRD.

Keeps the minimum a partner needs to advise us: what we're building and the
evidence, who it's for, requirements + acceptance criteria, how it's built
(condensed), risks, and how we'll measure success.

Removes: open questions (internal deliberation, incl. Sahan/AJP strategy),
out of scope, related documents, the tier-boundary deliberation, billing
internals, pricing/revenue figures, deep auth plumbing, brand-spec detail,
named people at other orgs, and unconfirmed newsrooms.

Every removal asserts its target exists — if a PRD edit breaks a redaction,
this script STOPS instead of silently leaking content.

Usage: make_ajp_prd.py <input PRD.md> <output md>
"""
import sys


def cut_between(text, start, end, label):
    i = text.find(start)
    if i == -1:
        sys.exit(f"REDACTION FAILED: start marker not found for {label}: {start[:60]!r}")
    j = text.find(end, i)
    if j == -1:
        sys.exit(f"REDACTION FAILED: end marker not found for {label}: {end[:60]!r}")
    if text.find(start, i + 1) != -1:
        sys.exit(f"REDACTION FAILED: start marker not unique for {label}")
    return text[:i] + text[j:]


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.exit(f"REDACTION FAILED: expected exactly 1 match for {label}, found {n}: {old[:60]!r}")
    return text.replace(old, new)


def main(src_path, out_path):
    text = open(src_path, encoding="utf-8").read()

    # ---- whole sections that stay internal ----
    text = cut_between(text, "## 5. Open questions",
                       "## 6. What's out of scope", "open questions section")
    text = cut_between(text, "## 6. What's out of scope (through Mar 4)",
                       "## 7. Risks", "out of scope section")
    i = text.find("\n---\n\n## 9. Related documents")
    if i == -1:
        sys.exit("REDACTION FAILED: Related documents section not found")
    text = text[:i] + "\n"

    # ---- tier boundary: partners get the tiers, not the deliberation ----
    text = cut_between(text, "### The tier boundary — what's decided, what's open, and when it freezes",
                       "---\n\n## 3. Requirements", "tier boundary subsection")
    text = replace_once(
        text,
        "Alpha usage gives the Oct 15 tier-boundary freeze (see \"The tier boundary\" under Who it's for) real evidence to decide on",
        "Alpha usage gives the Oct 15 free-vs-paid decisions real evidence to decide on",
        "measure-success tier reference")

    # ---- pricing and revenue stay internal ----
    text = replace_once(
        text,
        "Pricing comes from the operating financial model (`CAB_Financial_Model_Updated.xlsx`). Year 1 targets: 15 Pro + 5 Partner + 10 institutional seats ≈ $33K earned revenue, alongside the $100K RJI fellowship and foundation support.\n\n",
        "", "pricing intro + Year 1 targets")
    # Evidence bullets condensed, numbers removed (RJI fellowship figure stays, below).
    text = replace_once(
        text,
        "- Planet Detroit has run this tool in production in Michigan since early 2026. Through late August: **66 reader responses submitted through the boxes' own form, across 20 articles** — many describing specific civic actions in their own words: attending a council meeting to ask for an emergency declaration during the wildfire smoke, writing to Michigan senators, co-hosting a lobby day with 33 organizations.\n- Measured interaction with the boxes (planetdetroit.org GA4, Feb–Aug 2026): readers checked an **\"I did / will do this\" box ~990 times** and **clicked out to officials, meetings, and organizations 265 times**. The top click destinations are the product working as designed: Detroit City Council Zoom meetings, michigan.gov, the Michigan Voter Information Center, and groups like the Sierra Club and the Citizens Utility Board. (GA4 undercounts — ad blockers — so these are floors, and one reason the Toolbox measures first-party.)\n- Each article analysis costs ~$0.03; daily monitoring of all government sources costs under $1/day.",
        "- Planet Detroit has run this tool in production in Michigan since early 2026. Readers use the boxes and report real actions in their own words — attending a council meeting to ask for an emergency declaration during wildfire smoke, writing to Michigan senators, co-hosting a lobby day with partner organizations. Click-throughs go where the product intends: city council meetings, michigan.gov, the state voter information center, and civic organizations. Every signal is measured first-party, so the same evidence will exist for every newsroom on the platform.\n- Analysis and daily monitoring of government sources cost pennies per article — cheap enough to support a meaningful free tier.",
        "evidence condensed")
    text = replace_once(text, "#### Free — $0", "#### Free", "free tier price")
    text = replace_once(text, "#### Pro — $150/month", "#### Pro", "pro tier price")
    text = replace_once(text, "#### Newsroom Partner — $300/month ($200/seat institutional bulk)",
                        "#### Newsroom Partner", "partner tier price")
    text = cut_between(text, "**Business (Year 1, from the financial model):**",
                       "**Mission:**", "business metrics block")

    # ---- auth: condense implementation detail to what it means for a newsroom ----
    text = cut_between(text, "MuckRock Accounts (Squarelet, the system behind DocumentCloud)",
                       "### Billing — Stripe, minimal surface", "auth implementation detail")
    text = replace_once(
        text,
        "### Billing — Stripe, minimal surface",
        "Newsrooms sign in with their MuckRock account (an OpenID Connect login already used across journalism via DocumentCloud); the newsroom's MuckRock organization becomes its Toolbox account, and organization admins become account admins. Until MuckRock completes our app registration, an email magic-link login fills in. All data access is tenant-scoped server-side, with automated cross-tenant isolation tests in CI.\n\n### Billing — Stripe, minimal surface",
        "auth condensed insert")

    # ---- billing internals (incl. MuckRock's unannounced plans) stay internal ----
    text = cut_between(text, "### Billing — Stripe, minimal surface",
                       "### Embed + measurement", "billing subsection")
    text = replace_once(
        text,
        " *(Stripe billing lands in January — see \"How it's built\" — since nobody pays before the March launch. Feature gating and usage caps are already live and don't depend on Stripe.)*",
        "", "deadlines Stripe note")
    text = replace_once(
        text,
        " — *Stripe itself deferred to January (no one pays before the March launch; test-mode checkout demo-able by the Dec 3 final beta; live billing well before Mar 4)*",
        "", "milestone A Stripe note")
    text = replace_once(
        text,
        "- [ ] *(moved to the January billing milestone)* A Stripe checkout provisions a Pro tenant whose gates open, and cancellation closes them — test-mode by Dec 3, live before Mar 4\n",
        "", "milestone A Stripe criterion")
    text = replace_once(text, "- Upgrade path: in-app upgrade to Pro via Stripe Checkout",
                        "- Upgrade path: in-app upgrade to Pro", "milestone B Stripe upgrade")
    text = replace_once(text, "MuckRock handles sign-in; Stripe handles payments.",
                        "MuckRock handles sign-in.", "architecture summary Stripe")

    # ---- header meta ----
    text = replace_once(
        text,
        "**Status:** Approved founding document — the working spec\n**Companion:** `ROADMAP.md` (phase-by-phase development plan)",
        "**Status:** Partner edition of the working product spec\n**Companion:** the development roadmap, below on this page", "header meta")
    text = replace_once(
        text,
        "**Authors:** Nina Ignaczak (product owner) + Claude (development lead)",
        "**Author:** Nina Ignaczak (product owner), Planet Detroit", "author line")

    # ---- named people, unconfirmed newsrooms, wavering partners stay internal ----
    text = replace_once(
        text,
        "**Alpha testers: Planet Detroit and Bridge Michigan confirmed.** Bridge uses the existing Michigan pack, so onboarding takes almost no extra work. We will offer Sahan Journal (Minnesota, Twin Cities) a spot in the alpha (decided with Ashley 8/27), and MinnPost has also expressed interest. The emerging shape: a two-state alpha — Planet Detroit + Bridge Michigan in Michigan, Sahan + MinnPost in Minnesota — complementary tests in two states, which would make the second data pack Minnesota. New Hampshire Public Radio wants to push to the Dec–Jan core/beta window, so they are up in the air. The broader RJI core/beta cohort for Dec–Jan stays managed in the pilot testing plan.",
        "**Alpha testers: Planet Detroit and Bridge Michigan confirmed, with additional newsrooms in conversation.** The broader RJI core/beta cohort runs Dec–Jan.",
        "alpha tester status")
    text = replace_once(text, "e.g., Daniela Allee (NHPR)", "RJI pilot cohort newsrooms", "NHPR editor name")
    text = replace_once(text,
                        "(Planet Detroit, Bridge Michigan, and possibly Sahan and MinnPost)",
                        "(Planet Detroit, Bridge Michigan, and possibly others)", "deadlines alpha roster")
    text = replace_once(text, "Any later-joining alpha newsroom (Sahan, MinnPost)",
                        "Any later-joining alpha newsroom", "alpha goals roster")
    text = replace_once(text, "Tiny News Collective member, Now Kalamazoo",
                        "Solo and small independent newsrooms", "persona newsroom examples")

    # ---- renumber the surviving sections ----
    text = replace_once(text, "## 7. Risks", "## 5. Risks", "renumber Risks")
    text = replace_once(text, "## 8. How we'll measure success", "## 6. How we'll measure success",
                        "renumber measure success")
    text = replace_once(text, "#8-how-well-measure-success", "#6-how-well-measure-success",
                        "renumber measure-success link")

    # ---- nothing redacted may survive ----
    for forbidden in ("AJP-portfolio", "fork risk", "poster-child", "claimable story",
                      "Ownership guardrails", "License posture", "/Users/user/",
                      "$150/month", "$300/month", "$200/seat", "$33K", "5–8%",
                      "Sahan", "NHPR", "MinnPost", "Daniela", "Allan", "Hampshire",
                      "Kalamazoo", "Tiny News Collective", "Deep South Today", "MTC",
                      "Stripe", "Open questions", "tier boundary", "Related documents"):
        if forbidden in text:
            sys.exit(f"REDACTION FAILED: forbidden phrase still present: {forbidden!r}")

    open(out_path, "w", encoding="utf-8").write(text)
    print(f"AJP PRD written to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: make_ajp_prd.py <input PRD.md> <output md>")
    main(sys.argv[1], sys.argv[2])
