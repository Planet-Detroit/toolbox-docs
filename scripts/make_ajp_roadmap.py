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
        "Sahan is being offered an alpha spot and MinnPost has expressed interest (a possible Minnesota pair); NHPR may join the Dec–Jan beta instead.",
        "Additional newsrooms may join as conversations firm up.",
        "Oct 15 alpha roster")
    text = replace_once(text, "the pack #2 state decision (New Hampshire vs. Minnesota — leaning Minnesota; needs MinnPost + Sahan confirmation) — **decide by Sept 14**",
                        "the pack #2 state decision — **decide by Sept 14**", "right-now pack state")
    text = replace_once(text, "(Kat, 8/31)", "(RJI, 8/31)", "Kat name")
    text = replace_once(text, "(raised by Kat at RJI, 8/31)", "(raised by RJI, 8/31)", "Kat name 2")
    text = replace_once(text, "confirm with Allan what an org-less sign-in looks like",
                        "confirm with MuckRock what an org-less sign-in looks like", "Allan sign-in ref")
    text = replace_once(
        text,
        " *(v3.1 applies the approved September amendments \u2014 `docs/prd-amendments-2026-09-allan-review.md`)*",
        "", "v3.1 version note")
    text = replace_once(text, "; completed phases live in **The record** at the bottom", "", "how-to record ref")
    text = replace_once(text,
                        "*(September is sequenced in the build plan above. The former Phases 4–6 were folded into it on Sept 2 — one plan per time period, nothing tracked twice. Phases 1–3 history lives in \"The record\" at the bottom.)*",
                        "*(September is sequenced in the build plan above.)*", "from-oct intro")
    text = replace_once(text,
                        "Minnesota platform reconnaissance done (a Minnesota pack is template drops, not research).",
                        "pack #2 platform reconnaissance done (the pack is template drops, not research).", "right-now recon")
    text = replace_once(text, "· Minnesota platform reconnaissance |",
                        "· pack #2 platform reconnaissance |", "week1 recon cell")
    text = replace_once(text, "(no-ops until Nina's 20-minute account setup — `MONITORING.md`)",
                        "(no-ops until account setup completes)", "monitoring ref 1")
    text = replace_once(text, "(code live; accounts are Nina's — `MONITORING.md`)",
                        "(code live; account setup pending)", "monitoring ref 2")
    text = replace_once(text, "(email-safe HTML, Mailchimp-tested — Bridge's ESP)",
                        "(email-safe HTML, tested against a partner newsroom's email platform)", "mailchimp ref")
    text = replace_once(text, " · **Sept 14: pack #2 state decision** (needs MinnPost + Sahan confirmation)",
                        " · **Sept 14: pack #2 state decision**", "week2 confirmations")
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
    text = replace_once(text, "**Billing (Stripe) built and tested end to end**", "**Billing built and tested end to end**",
                        "Jan-Feb Stripe")

    text = replace_once(
        text,
        " **Fits into build lulls:** Rochester Hills recheck \u00b7 EJ-towns platform survey.",
        "", "internal side tasks")
    # Internal file paths and internal examples.
    text = replace_once(
        text,
        "- The running narrative lives in `docs/SESSION-LOG.md`; scraper coverage and its gaps live in `cat-civic-data/scrapers/SCRAPER-ROADMAP.md`.\n",
        "", "internal paths bullet")


    text = replace_once(text, "| Maintenance calendar | `maintenance.yaml` |",
                        "| Maintenance calendar | Internal calendar file |", "maintenance file cell")
    text = replace_once(text, "registered in registry.yaml with health checks",
                        "registered in our scraper registry with health checks", "registry file ref")
    text = replace_once(text, "broader beta cohort per the pilot testing plan).",
                        "broader beta cohort per our RJI testing plan, available on request).", "testing plan ref")

    text = replace_once(text, " (the 2028 support model in the prospectus depends on it)",
                        " (the support model depends on it)", "AI assistant prospectus ref")
    text = replace_once(text, "**Beta pilot asks (Dec–Feb, feeding the prospectus tests):**",
                        "**Beta pilot asks (Dec–Feb):**", "pilot asks prospectus ref")

    for forbidden in ("Sahan", "NHPR", "MinnPost", "Daniela", "Allan", "Stripe", "Hampshire", "Minnesota", "Mailchimp", "MONITORING.md", "Kat,", "Kat at",
                      "SESSION-LOG", "SCRAPER-ROADMAP", "Kalamazoo", "task #", "maintenance.yaml", "registry.yaml", "cat-civic-data/",
                      "The record", "fddojayfmrslkoddygqj", "/Users/user/", "prospectus", "PROSPECTUS"):
        if forbidden in text:
            sys.exit(f"REDACTION FAILED: forbidden phrase still present: {forbidden!r}")

    open(out_path, "w", encoding="utf-8").write(text)
    print(f"AJP roadmap written to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: make_ajp_roadmap.py <input ROADMAP.md> <output md>")
    main(sys.argv[1], sys.argv[2])
