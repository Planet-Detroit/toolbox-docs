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


def replace_span(text, start, end, new, label):
    """Replace from a unique start marker through the end marker (inclusive).
    Used where the internal text carries names that should not live in this
    public script either."""
    i = text.find(start)
    if i == -1 or text.find(start, i + 1) != -1:
        sys.exit(f"REDACTION FAILED: start marker missing or not unique for {label}: {start[:60]!r}")
    j = text.find(end, i)
    if j == -1:
        sys.exit(f"REDACTION FAILED: end marker not found for {label}: {end[:60]!r}")
    return text[:i] + new + text[j + len(end):]


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
    # Pack #2 decided (Sept 10): the state, the newsroom, and internal plan
    # paths stay internal on the partner page.
    text = replace_span(
        text,
        "- ✅ **Pack #2 decided Sept 10: ",
        "(today untagged rows read as national).",
        "- ✅ **Pack #2 decided Sept 10.** The third alpha newsroom confirmed; the pack build runs as its own track with every hour and surprise logged — the first measured cost of a state. **Sept 11:** the pack is redefined as the *standard state pack* (three layers, custom adds, the promote/pause ladder — PRD §3); a Michigan body-directory backfill starts with the SEMCOG counties. Prerequisite before the new newsroom's account: every Michigan row tagged with its state.",
        "right-now pack state")
    text = replace_span(
        text,
        "| **Sept 15–17** | **Minnesota standard collectors live — hard date** (",
        "the Legislature schedule)",
        "| **Sept 15–17** | **Pack #2 standard collectors live — hard date** (Layer C: the utility commission, the two largest cities and their counties, the environmental agency's comment periods, the Legislature schedule)",
        "sept 15-17 row")
    text = replace_once(text, " First instance and cost measurement: `docs/state-packs/mn-pack/BUILD-PLAN.md`.",
                        " The first instance is pack #2.", "standard pack plan path")
    text = replace_once(text, "organizations as in Minnesota since Sept 21", "organizations as in the second state since Sept 21", "pack 1 organizations footing")
    text = replace_once(text, "3. Minnesota standard collectors 7 → 4",
                        "3. Pack #2 standard collectors 7 → 4", "cut list pack 2")
    text = replace_once(text, "(Kat, 8/31)", "(RJI, 8/31)", "Kat name")
    text = replace_once(text, "(raised by Kat at RJI, 8/31)", "(raised by RJI, 8/31)", "Kat name 2")
    text = replace_once(text, "confirm with Allan what an org-less sign-in looks like",
                        "confirm with MuckRock what an org-less sign-in looks like", "Allan sign-in ref")
    text = replace_span(
        text,
        " *(v3.2: pack #2 is ",
        "`docs/prd-amendments-2026-09-allan-review.md`)*",
        "", "version note")
    text = replace_once(text, "; completed phases live in **The record** at the bottom", "", "how-to record ref")
    text = replace_once(text,
                        "*(September is sequenced in the build plan above. The former Phases 4–6 were folded into it on Sept 2 — one plan per time period, nothing tracked twice. Phases 1–3 history lives in \"The record\" at the bottom.)*",
                        "*(September is sequenced in the build plan above.)*", "from-oct intro")
    text = replace_once(text,
                        "Minnesota platform reconnaissance done (a Minnesota pack is template drops, not research).",
                        "pack #2 platform reconnaissance done (the pack is template drops, not research).", "right-now recon")
    text = replace_once(text, "· Minnesota platform reconnaissance |",
                        "· pack #2 platform reconnaissance |", "week1 recon cell")
    text = replace_once(text, "(✅ fully live and verified Sept 3 — Sentry on both services, three green UptimeRobot monitors; `MONITORING.md`)",
                        "(✅ fully live and verified Sept 3)", "monitoring ref 1")
    # Internal ops detail (migration ledger repair, deploy tooling rules)
    # stays internal.
    text = replace_once(text, " Also Sept 3: the production migration ledger was repaired (an August file-rename had desynced it), so `supabase db push` works normally again — schema changes go through migration files only, never the dashboard SQL editor.",
                        "", "monitoring ref 2 (internal ops sentence)")
    text = replace_once(text, "(email-safe HTML, Mailchimp-tested — Bridge's ESP; **verified Sept 8** through Mailchimp's preview and a real ActiveCampaign send, rows confirmed)",
                        "(email-safe HTML, tested against a partner newsroom's email platform; **verified Sept 8** through a real send, rows confirmed)", "mailchimp ref")
    text = replace_once(text, " · **Sept 14: pack #2 state decision** (needs MinnPost + Sahan confirmation)",
                        " · **Sept 14: pack #2 state decision**", "week2 confirmations")
    text = replace_span(
        text,
        "- 🔨 **Pack #2 — Minnesota — build before Oct 1",
        "Michigan's Layer C also lacks Grand Rapids and Kent County.",
        "- 🔨 **Pack #2 — the second state — build before Oct 1 (September plan; decided Sept 10).** Phases: two-state safety fix → the standard into the PRD → rosters → body directory v1 → standard collectors (Sept 15–17) → custom adds with the newsroom → accounts → verification → playbook and cost read-out (November).\n- ⬜ **Michigan body directory** (Layer B, backfill): SEMCOG's seven counties first, then an evaluation step before the other 76 counties. Read against the standard, Michigan's Layer C also lacks Grand Rapids and Kent County.",
        "pack status bullets")
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


    text = replace_once(text, "| A · Maintenance calendar | `maintenance.yaml` |",
                        "| A · Maintenance calendar | Internal calendar file |", "maintenance file cell")
    text = replace_once(text, "registered in registry.yaml with state, time zone, and health checks",
                        "registered in our scraper registry with state, time zone, and health checks", "registry file ref")
    text = replace_once(text, "broader beta cohort per the pilot testing plan).",
                        "broader beta cohort per our RJI testing plan, available on request).", "testing plan ref")

    text = replace_once(text, " (the 2028 support model in the prospectus depends on it)",
                        " (the support model depends on it)", "AI assistant prospectus ref")
    text = replace_once(text, "**Beta pilot asks (Dec–Feb, feeding the prospectus tests):**",
                        "**Beta pilot asks (Dec–Feb):**", "pilot asks prospectus ref")

    for forbidden in ("Sahan", "NHPR", "MinnPost", "Haugen", "Minneapolis", "docs/state-packs", "mn-pack", "docs/handoffs", "Daniela", "Allan", "Stripe", "Hampshire", "Minnesota", "Mailchimp", "MONITORING.md", "Kat,", "Kat at",
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
