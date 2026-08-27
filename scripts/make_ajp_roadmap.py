#!/usr/bin/env python3
"""Produce the AJP/partner-facing edition of the roadmap.

Keeps the forward plan, milestones, and data track. Removes internal-only
material: unconfirmed newsrooms and named people at other orgs, billing
internals, internal file paths and task numbers, and the completed-phases
record (internal identifiers). Fails loudly if a roadmap edit breaks a target.

Usage: make_ajp_roadmap.py <input ROADMAP.md> <output md>
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

    # Header meta.
    text = replace_once(text, "**Companion to:** `PRD.md`", "**Companion to:** the PRD above",
                        "companion line")
    text = replace_once(text, "Working rules (per CLAUDE.md):", "Working rules:", "CLAUDE.md ref")

    # The completed-phases record carries internal identifiers — the "Right now"
    # summary covers it for partners.
    i = text.find("\n---\n\n## The record — completed phases ✅")
    if i == -1:
        sys.exit("REDACTION FAILED: record section not found")
    text = text[:i] + "\n"

    # Right now.
    text = replace_once(
        text,
        " Production runs on the new platform: Michigan data migrated at full parity, 40 collectors running daily with health alerts that flag failures, per-newsroom AI analysis, first-party analytics proven end to end. Full detail in \"The record\" at the bottom.",
        " In production: full Michigan data, 40 collectors running daily with health alerts that flag failures, per-newsroom AI analysis, first-party analytics proven end to end.",
        "right-now phases bullet")
    text = replace_once(
        text,
        "Alpha onboarding runs through September: Planet Detroit live, Bridge Michigan confirmed, Sahan being offered an alpha spot, MinnPost interested — the emerging shape is a two-state alpha (Planet Detroit + Bridge in Michigan, Sahan + MinnPost in Minnesota); NHPR wants to push to the Dec–Jan pilot window.",
        "Alpha onboarding runs through September: Planet Detroit live, Bridge Michigan confirmed, additional newsrooms in conversation.",
        "right-now alpha bullet")
    text = replace_once(
        text,
        "the pack #3 state decision (New Hampshire vs. Minnesota — follows the NHPR and Sahan news). Stripe billing is deliberately deferred to January: nobody pays before the March launch, and gating/caps already work without it.",
        "the pack #3 state decision. Billing is deliberately deferred to January: nobody pays before the March launch, and feature gating already works without it.",
        "right-now waiting bullet")
    text = replace_once(
        text,
        "- The running narrative lives in `docs/SESSION-LOG.md`; scraper coverage and its gaps live in `cat-civic-data/scrapers/SCRAPER-ROADMAP.md`.\n",
        "", "internal paths bullet")

    # Billing internals.
    text = replace_once(
        text,
        "- Stripe is out of this phase (January build: Checkout, Customer Portal, the one webhook → `tenants.plan`; test-mode demo-able by Dec 3). Freed time flows to tester-facing polish: Phase 5 Dustin items (section reordering, article-text collapse, Setup page) can pull forward.",
        "- Billing is out of this phase (built in January). Freed time flows to tester-facing polish: Phase 5 items (section reordering, article-text collapse, Setup page) can pull forward.",
        "phase 4 billing")
    text = replace_once(text, "In-app upgrade flow follows the January Stripe build",
                        "In-app upgrade flow follows the January billing build", "Nov 5 billing")
    text = replace_once(
        text,
        "**Stripe billing built end-to-end** (Checkout, Customer Portal, webhook → plan, live mode — first real charges arrive with the March launch)",
        "**Billing built end-to-end** (first real charges arrive with the March launch)",
        "Mar 4 billing")
    text = replace_once(
        text,
        "· (Stripe webhook integrity joins this list when billing builds in January)",
        "· (billing integrity joins this list in January)", "never-cut billing")
    text = replace_once(
        text,
        "| Stripe account live mode | January (billing build; live before Mar 4) | Deferred by design | — |\n",
        "", "deps Stripe row")

    # Unconfirmed newsrooms and named people.
    text = replace_once(
        text,
        "- ⬜ **PD tenant goes live; Dustin uses the new platform for real work.** Old builder stays open in the next tab. Priority all week: fix what Dustin breaks.",
        "- ⬜ **Planet Detroit's newsroom uses the platform for real daily editorial work.** Priority all week: fix what real use surfaces.",
        "phase 5 old builder")
    text = replace_once(
        text,
        "Sahan is being offered an alpha spot and MinnPost has expressed interest (a possible Minnesota pair); NHPR may join the Dec–Jan pilot instead.",
        "Additional newsrooms may join as conversations firm up.",
        "Oct 15 alpha roster")
    text = replace_once(
        text,
        "| NHPR conversation (Daniela Allee) | Informs pack #2/#3 state choice | They want to push to Dec–Jan | Pack standard ships regardless; adjust after |\n",
        "", "deps NHPR row")
    text = replace_once(text, "Requested; in progress with Allan", "Requested; in progress",
                        "deps Allan mention")
    text = replace_once(
        text,
        "pressure-test priorities with Dustin, Ashley, Sahan, Bridge, and (if in) NHPR.",
        "pressure-test priorities with our editors and alpha partners.",
        "data track partners")
    text = replace_once(
        text,
        " The category map lives in `cat-civic-data/scrapers/SCRAPER-ROADMAP.md` (\"Beyond meetings\").",
        "", "data track category map path")
    text = replace_once(
        text,
        "⏸ **Pack #3.** Minnesota or New Hampshire — whichever pack #2 isn't; decision follows the NHPR and Sahan news.",
        "⏸ **Pack #3.** Minnesota or New Hampshire — whichever pack #2 isn't.",
        "pack 3 bullet")

    # Internal task numbers and file paths.
    text = replace_once(
        text,
        "the moment they hit a gap (\"I needed the Kalamazoo planning commission and it wasn't there\"). Suggestions land in a `data_source_suggestions` table, we review them, and they feed the prioritized build list in `SCRAPER-ROADMAP.md`.",
        "the moment they hit a gap. Suggestions land in a review queue and feed the prioritized build list.",
        "suggest intake internals")
    text = replace_once(text, " (PRD \"The tier boundary\", task #33)", "", "tier freeze task ref")
    text = replace_once(
        text,
        "**Decide the free-tier own-data integration method** (PRD Open questions, Q1) using early pilot conversations.",
        "**Decide the free-tier own-data integration method** using early pilot conversations.",
        "Q1 ref")
    text = replace_once(
        text,
        "⬜ **Michigan expansion** (demand-driven, priority order per `SCRAPER-ROADMAP.md`):",
        "⬜ **Michigan expansion** (demand-driven, in priority order):",
        "expansion path ref")
    text = replace_once(
        text,
        "the EJ-towns platform survey (task #28)",
        "the EJ-towns platform survey", "task 28 ref")

    for forbidden in ("Sahan", "NHPR", "MinnPost", "Daniela", "Allan", "Stripe",
                      "SESSION-LOG", "SCRAPER-ROADMAP", "Kalamazoo", "task #",
                      "The record", "CLAUDE.md", "fddojayfmrslkoddygqj", "/Users/user/"):
        if forbidden in text:
            sys.exit(f"REDACTION FAILED: forbidden phrase still present: {forbidden!r}")

    open(out_path, "w", encoding="utf-8").write(text)
    print(f"AJP roadmap written to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: make_ajp_roadmap.py <input ROADMAP.md> <output md>")
    main(sys.argv[1], sys.argv[2])
