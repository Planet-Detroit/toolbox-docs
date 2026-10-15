# Toolbox Product Docs (password-protected site)

Publishes the Civic Action Toolbox PRD and roadmap as a single password-protected web page on GitHub Pages.

- **Live page:** https://planet-detroit.github.io/toolbox-docs/
- **Password:** stored in `.password` in this folder on Nina's Mac (never committed). Share it only with people who should see internal product strategy.
- **How the protection works:** the published file is encrypted with StatiCrypt (AES-256). The repo is public, but without the password the content is unreadable scrambled text — there is nothing to "view source" on.

## Updating the site after the PRD or roadmap changes

```sh
cd ~/projects/toolbox-docs
./build.sh
git add docs && git commit -m "Update docs site" && git push
```

Or just ask Claude: "rebuild and publish the toolbox docs site."

## What's in here

- `build.sh` — converts `../civic-action-toolbox-app/PRD.md` + `ROADMAP.md` to styled HTML (Toolbox brand), then encrypts it
- `template/` — page header, divider, and footer HTML around the converted docs
- `docs/` — the encrypted page that GitHub Pages serves (the only content published)
- `build/` — plaintext intermediate files, ignored by git so they never reach the public repo
- `.staticrypt.json` — encryption salt (not secret; it's embedded in the page anyway). Committed so "remember me" keeps working across rebuilds.

## Changing the password

Edit `.password`, run `./build.sh`, commit and push `docs/`.

## Partner edition

A second, separately-passworded page at https://planet-detroit.github.io/toolbox-docs/partner/ serves a redacted PRD and roadmap for sharing with outside partners. `scripts/make_partner_prd.py` removes the internal strategy (open questions, license housekeeping, local file paths) and STOPS with an error if a PRD edit ever breaks a redaction — it cannot silently leak. Its password is in `.password-partner` (never committed, different from the internal one). Rebuild with `./build-partner.sh`; the internal `./build.sh` does not touch it, so rebuild BOTH after PRD edits.
