#!/usr/bin/env python3
"""Produce the AJP/partner-facing version of the PRD.

Reads the internal PRD.md and removes content that must not reach AJP:
  - Open questions Q4 (Sahan Journal partnership strategy, incl. AJP-portfolio analysis)
  - Open questions Q7 (internal license housekeeping)
  - Internal file paths and call-notes references
Everything else is left intact. Every removal asserts its target text exists,
so if the PRD is edited in a way that breaks a redaction, this script STOPS
with an error instead of silently leaking content.

Usage: make_ajp_prd.py <input PRD.md> <output md>
"""
import re
import sys


def cut_between(text, start, end, label):
    """Remove everything from `start` up to (not including) `end`. Exactly once."""
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

    # The Sahan/AJP partnership strategy must never reach AJP.
    text = cut_between(text, "**Q4 — Sahan Journal as founding design partner",
                       "**Q5 — Topic boxes", "Q4 Sahan/AJP strategy")
    # Internal legal housekeeping, irrelevant to partners.
    text = cut_between(text, "**Q7 — License posture on public repos.**",
                       "\n---\n\n## 6. What's out of scope", "Q7 license posture")
    # Renumber the surviving questions so there is no visible gap.
    text = replace_once(text, "**Q5 — Topic boxes", "**Q4 — Topic boxes", "renumber Q5")
    text = replace_once(text, "**Q6 — Custom reader questions", "**Q5 — Custom reader questions", "renumber Q6")

    # Internal call notes and file paths.
    text = replace_once(
        text,
        " (Allan's fuller advice — including the per-newsroom-SQLite storage pattern and the deliberate no-LLM-column-mapping constraint — is in `docs/calls/2026-08-20-muckrock-allan.md`.)",
        "", "Q1 call-notes reference")
    # Pricing and revenue targets stay internal; the AJP edition names tiers only.
    text = replace_once(
        text,
        "Pricing comes from the operating financial model (`CAB_Financial_Model_Updated.xlsx`). Year 1 targets: 15 Pro + 5 Partner + 10 institutional seats ≈ $33K earned revenue, alongside the $100K RJI fellowship and foundation support.",
        "Pricing is set in the operating financial model — details available on request. The build is funded by the $100K RJI fellowship alongside foundation support.",
        "pricing intro + Year 1 targets")
    text = replace_once(text, "#### Free — $0", "#### Free", "free tier price")
    text = replace_once(text, "#### Pro — $150/month", "#### Pro", "pro tier price")
    text = replace_once(text, "#### Newsroom Partner — $300/month ($200/seat institutional bulk)",
                        "#### Newsroom Partner", "partner tier price")
    text = replace_once(text, "**Q3 — Institutional cohorts.** The $200/seat bulk tier",
                        "**Q3 — Institutional cohorts.** The institutional bulk tier", "Q3 seat price")
    text = cut_between(text, "**Business (Year 1, from the financial model):**",
                       "**Mission:**", "business metrics block")
    text = replace_once(
        text,
        "— source of truth is the splash repo at `/Users/user/projects/civic-action-toolbox` (`styles.css` tokens + `assets/`):",
        "— source of truth is the splash-site repo's design tokens:", "splash repo local path")

    # Replace the Related documents section (local paths) with a partner-facing note.
    i = text.find("## 9. Related documents")
    if i == -1:
        sys.exit("REDACTION FAILED: Related documents heading not found")
    text = text[:i] + (
        "## 9. Related documents\n\n"
        "The development roadmap, pilot testing plan, and operating financial model "
        "are companion documents — available from Planet Detroit on request.\n"
    )

    # Adjust the header meta for the partner edition.
    text = replace_once(
        text,
        "**Status:** Approved founding document — the working spec\n**Companion:** `ROADMAP.md` (phase-by-phase development plan)",
        "**Status:** Partner edition of the working product spec", "header meta")
    text = replace_once(
        text,
        "**Authors:** Nina Ignaczak (product owner) + Claude (development lead)",
        "**Author:** Nina Ignaczak (product owner), Planet Detroit", "author line")

    # Partner-facing docs state alpha status simply; the internal wavering/pack
    # logic stays internal.
    text = replace_once(
        text,
        "**Alpha testers: Planet Detroit and Bridge Michigan confirmed.** Bridge uses the existing Michigan pack, so it onboards nearly free. Sahan Journal (Minnesota, Twin Cities) is up in the air but still possible. New Hampshire Public Radio wants to push to the Dec–Jan pilot window, so they are up in the air too. Pack #3 may therefore be Minnesota rather than New Hampshire — decision follows the NHPR and Sahan news. The broader RJI pilot cohort for Dec–Jan stays managed in the pilot testing plan.",
        "**Alpha testers: Planet Detroit and Bridge Michigan confirmed, with additional newsrooms in conversation.** The broader RJI pilot cohort runs Dec–Jan.",
        "alpha tester status")

    # MuckRock's unannounced billing plans were shared in a private call — not ours to publish.
    text = cut_between(text,
                       "**New option to evaluate in January (from the 2026-08-20 MuckRock call):**",
                       "- Stripe Checkout for signup", "MuckRock billing plans")
    # Named people and wavering partners stay internal.
    text = replace_once(text, "(Allan/MuckRock rec, 2026-08-20 call)", "", "Q1 call attribution")
    text = replace_once(text, "e.g., Daniela Allee (NHPR)", "RJI pilot cohort newsrooms", "NHPR editor name")
    text = replace_once(text, "(Sahan's mobile critique, Dustin's", "(a partner newsroom's mobile critique, Dustin's",
                        "Q2 Sahan mention")
    text = replace_once(text,
                        "(Planet Detroit, Bridge Michigan, and possibly Sahan and NHPR)",
                        "(Planet Detroit, Bridge Michigan, and possibly others)", "deadlines alpha roster")
    text = replace_once(text, "Any later-joining alpha newsroom (Sahan, NHPR)",
                        "Any later-joining alpha newsroom", "alpha goals roster")
    text = replace_once(text, "(to be adjusted with NHPR input as that relationship develops)",
                        "(to be adjusted with partner input)", "pack 2 NHPR mention")
    text = replace_once(text, "Requested P1 (Allan Lasser relationship); ToS/Privacy drafted",
                        "Requested P1; ToS/Privacy drafted", "risk table Allan mention")

    # Belt and braces: nothing from the redacted strategy may survive.
    for forbidden in ("AJP-portfolio", "fork risk", "poster-child", "claimable story",
                      "Ownership guardrails", "License posture", "/Users/user/",
                      "$150/month", "$300/month", "$200/seat", "$33K", "5–8%",
                      "Sahan", "NHPR", "Daniela", "Allan"):
        if forbidden in text:
            sys.exit(f"REDACTION FAILED: forbidden phrase still present: {forbidden!r}")

    open(out_path, "w", encoding="utf-8").write(text)
    print(f"AJP PRD written to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: make_ajp_prd.py <input PRD.md> <output md>")
    main(sys.argv[1], sys.argv[2])
