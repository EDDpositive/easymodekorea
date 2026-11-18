# EasyModeKorea

Source for https://easymodekorea.com: which Korean apps work for visitors, by setup, checked and dated.

- Content: `src/data.py` (answers) and `src/data_extra.py` (labels, plan, help, phrases).
- Build: `python3 src/build.py` writes every page, the sitemap and the offline cache list from the repo root.
- `hosts.html` is hand-written (Korean host link maker).
- `chat-kb.txt` is built too: the plain-text knowledge base the chat assistant answers from.
- Chat assistant: `chat.js` (widget) + `worker/` (Cloudflare Worker calling Claude). Off until `CHAT_ENDPOINT` in `src/build.py` is set; see `worker/README.md`.
