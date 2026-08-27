#!/usr/bin/env python3
"""Produce the AJP/partner-facing edition of the roadmap.

Keeps the forward plan, milestones, timeline graphic, and data-pack standard.
Removes internal-only material: unconfirmed newsrooms, named people at other
orgs, billing internals, internal file paths, and the completed-phases record.
Fails loudly if a roadmap edit breaks a target.

Usage: make_ajp_roadmap.py <input ROADMAP.md> <output md>
"""
import sys


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.exit(f"REDACTION FAILED: expected exactly 1 match for {label}, found {n}: {old[:70]!r}")
    return text.replace(old, new)


def main(src_path, out_path):
    text = open(src_path, encoding="utf-8").read()

    text = replace_once(text, "**Companion to:** `PRD.md`", "**Companion to:** the PRD above",
                        "companion line")

    # The completed-phases record carries internal identifiers; "Right now" covers it.
    i = text.find("\n---\n\n## The record — completed phases ✅")
    if i == -1:
        sys.exit("REDACTION FAILED: record section not found")
    text = text[:i] + "\n"
    text = replace_once(text, " Full detail in \"The record\" at the bottom.", "",
                        "record pointer")

    # Unconfirmed newsrooms and named people stay internal.
    text = replace_once(
        text,
        "Alpha onboarding runs through September: Planet Detroit live, Bridge Michigan confirmed, Sahan being offered an alpha spot, MinnPost interested — the emerging shape is a two-state alpha (Planet Detroit + Bridge in Michigan, Sahan + MinnPost in Minnesota); NHPR wants to push to the Dec–Jan beta window.",
        "Alpha onboarding runs through September: Planet Detroit live, Bridge Michigan confirmed, additional newsrooms in conversation.",
        "right-now alpha roster")
    text = replace_once(
        text,
        "Sahan is being offered an alpha spot and MinnPost has expressed interest (a possible Minnesota pair); NHPR may join the Dec–Jan beta instead.",
        "Additional newsrooms may join as conversations firm up.",
        "Oct 15 alpha roster")
    text = replace_once(
        text,
        "pressure-test priorities with our editors, Ashley, Sahan, Bridge, and (if in) NHPR.",
        "pressure-test priorities with our editors and alpha partners.",
        "scoping partners")
    text = replace_once(text, "the pack #2 state decision (New Hampshire vs. Minnesota).",
                        "the pack #2 state decision.", "right-now pack state")
    text = replace_once(text, "**Decide the pack #2 state** (New Hampshire vs. Minnesota) — this gates everything below.",
                        "**Decide the pack #2 state** — this gates everything below.", "phase 5 pack state")
    text = replace_once(
        text,
        "State TBD (New Hampshire vs. Minnesota; a Sahan + MinnPost alpha pair would make it Minnesota).",
        "State being decided now.",
        "pack 2 state note")
    text = replace_once(
        text,
        "| NHPR conversation (Daniela Allee) | Informs pack #2 state choice | They want to push to Dec–Jan | Pack standard ships regardless; adjust after |\n",
        "", "deps NHPR row")

    # Billing internals.
    text = replace_once(text, "Billing (Stripe) built and tested end to end", "Billing built and tested end to end",
                        "Jan-Feb Stripe")

    text = replace_once(
        text,
        "- \u2b1c Rochester Hills recheck \u00b7 the EJ-towns platform survey (both fit into build lulls).\n",
        "", "internal side tasks bullet")
    # Internal file paths and internal examples.
    text = replace_once(
        text,
        "- The running narrative lives in `docs/SESSION-LOG.md`; scraper coverage and its gaps live in `cat-civic-data/scrapers/SCRAPER-ROADMAP.md`.\n",
        "", "internal paths bullet")
    text = replace_once(
        text,
        " The category map lives in `cat-civic-data/scrapers/SCRAPER-ROADMAP.md` (\"Beyond meetings\").",
        "", "category map path")
    text = replace_once(
        text,
        "the moment they hit a gap (\"I needed the Kalamazoo planning commission and it wasn't there\"). Suggestions land in a `data_source_suggestions` table, we review them, and they feed the prioritized build list in `SCRAPER-ROADMAP.md`.",
        "the moment they hit a gap. Suggestions land in a review queue and feed the prioritized build list.",
        "suggest intake internals")
    text = replace_once(
        text,
        "**Decide the free-tier own-data integration method** (PRD Open questions, Q1) using early partner conversations.",
        "**Decide the free-tier own-data integration method** using early pilot conversations.",
        "Q1 ref")

    for forbidden in ("Sahan", "NHPR", "MinnPost", "Daniela", "Allan", "Stripe", "Hampshire",
                      "SESSION-LOG", "SCRAPER-ROADMAP", "Kalamazoo", "task #",
                      "The record", "fddojayfmrslkoddygqj", "/Users/user/"):
        if forbidden in text:
            sys.exit(f"REDACTION FAILED: forbidden phrase still present: {forbidden!r}")

    open(out_path, "w", encoding="utf-8").write(text)
    print(f"AJP roadmap written to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: make_ajp_roadmap.py <input ROADMAP.md> <output md>")
    main(sys.argv[1], sys.argv[2])
