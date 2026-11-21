# EasyModeKorea

Source for https://easymodekorea.com: which Korean apps work for visitors, by setup, checked and dated.

- Content: `src/data.py` (answers) and `src/data_extra.py` (labels, plan, help, phrases).
- Build: `python3 src/build.py` writes every page, the sitemap and the offline cache list from the repo root.
- `hosts.html` is hand-written (Korean host link maker).
- Dates: `src/page_dates.json` keeps a content hash and last-changed date per page; the build updates it, so commit it with the pages.
- App shell: `src/app_shell.py` holds the bottom tabs, save and share, install prompt, offline worker (`sw.js`), web manifest, and the text for the Korean cards, My trip, help and privacy pages in all five languages. The build writes `app.js`, `sw.js`, `manifest.webmanifest`, `search.json` and `.well-known/assetlinks.json`.
- Checks: `python tools/check_site.py` (no browser) and `python tools/browser_check.py` (headless Edge or Chrome: installable, offline with the server off, 375px width, app mode). Both run on every pull request.
- Android: see `android/README.md` for the build path and `store/listing.md` for the Play listing. `docs/play-console-checklist.md` lists the steps only the owner can do.
