# EasyModeKorea

Source for https://easymodekorea.com: which Korean apps work for visitors, by setup, checked and dated.

- Content: `src/data.py` (answers) and `src/data_extra.py` (labels, plan, help, phrases).
- Build: `python3 src/build.py` writes every page, the sitemap and the offline cache list from the repo root.
- `hosts.html` is hand-written (Korean host link maker).
- Dates: `src/page_dates.json` keeps a content hash and last-changed date per page; the build updates it, so commit it with the pages.
