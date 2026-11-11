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

## Partner edition (removed Nov 11, 2026)

There was a second page at `/partner/` with a shortened PRD and roadmap for outside partners. Nina had it deleted on Nov 11, 2026: the page, its build script and its scripts are gone from this repo. Only the internal page is published now. Do not rebuild a partner page unless Nina asks for one.

