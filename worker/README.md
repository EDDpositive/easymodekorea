# emk-chat: Claude chat Worker for easymodekorea.com

GitHub Pages can't run server code, so the chat runs as a small Cloudflare Worker (free plan is enough).
The site's widget (`/chat.js`) posts questions here; the Worker answers with `claude-sonnet-5-5` using the
site's own `chat-kb.txt` (built by `src/build.py`, so answers stay in sync with the guides).

## One-time setup (needs Node.js 20+)

```bash
cd worker
npm install
npx wrangler login
npx wrangler kv namespace create EMK_CHAT_KV     # paste the printed id into wrangler.toml
npx wrangler secret put ANTHROPIC_API_KEY        # paste the key when prompted; it is never stored in git
npx wrangler deploy                              # prints https://emk-chat.<you>.workers.dev
```

Then in `src/build.py` set `CHAT_ENDPOINT = "https://emk-chat.<you>.workers.dev/chat"`, run
`python src/build.py`, commit and push. The widget only appears when `CHAT_ENDPOINT` is set.

## Limits (wrangler.toml `[vars]`)

| Setting | Default | Meaning |
|---|---|---|
| `DAILY_BUDGET_USD` | 1 | Stops answering for the rest of the UTC day after about this much spend |
| `MONTHLY_BUDGET_USD` | 15 | Same, for the month |
| `PER_IP_PER_HOUR` / `PER_IP_PER_DAY` | 15 / 40 | Questions per visitor (IP is hashed, never stored raw) |
| `CHAT_ENABLED` | true | `"false"` turns the assistant off without a redeploy of the site |

Per request: questions up to 500 characters, at most 12 messages of history, at most 1024 output tokens,
effort `low`, and the knowledge base is prompt-cached. Rough cost: about $0.002-0.01 per answer.

The counters are approximate (KV is eventually consistent), so also set a **monthly spend limit in the
Anthropic Console** for a hard ceiling. On the Workers free plan KV allows 1,000 writes/day; the Worker
writes 2 per question, so it tops out near 500 questions/day.

## Local test

```bash
echo ANTHROPIC_API_KEY=... > .dev.vars   # .dev.vars is git-ignored
npx wrangler dev
```
Add `http://localhost:8000` to `ALLOWED_ORIGINS` while testing, and build the site with
`EMK_CHAT_ENDPOINT=http://localhost:8787/chat python src/build.py` (don't commit that build).
