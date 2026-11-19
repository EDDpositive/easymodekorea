"""Shared helpers for the Claude API jobs (batch, prompt caching, token cap).

The key is read ONLY from the ANTHROPIC_API_KEY environment variable, which the
GitHub workflows fill from the repository secret of the same name. Never put it in
a file. Every job supports --dry-run, which builds the requests and prints the
size without touching the API (no key needed, nothing billed).
"""
import json
import os
import re
import sys
import time

MODEL = "claude-opus-5-5"


def make_request(custom_id, system, user, max_tokens):
    """One Batch API request. The system prompt is cached (shared across requests)."""
    assert re.fullmatch(r"[A-Za-z0-9_-]{1,64}", custom_id), custom_id
    return {
        "custom_id": custom_id,
        "params": {
            "model": MODEL,
            "max_tokens": max_tokens,
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": user}],
        },
    }


def check_cap(requests, max_total_tokens):
    """Refuse to run when the summed output cap is above the per-run budget."""
    total = sum(r["params"]["max_tokens"] for r in requests)
    print(f"{len(requests)} requests, output cap {total} tokens (run limit {max_total_tokens}).")
    if total > max_total_tokens:
        sys.exit(f"Refusing to run: {total} > {max_total_tokens}. Lower the scope or raise the limit on purpose.")
    return total


def get_client():
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        sys.exit("ANTHROPIC_API_KEY is not set. It must come from the GitHub Secret; do not set it locally.")
    import anthropic  # imported late so --dry-run needs nothing installed
    return anthropic.Anthropic(api_key=key)


def run_batch(requests, resume=None, poll_seconds=60, timeout_minutes=300):
    """Submit (or resume) a batch, wait for it, return ({custom_id: text}, {custom_id: error})."""
    client = get_client()
    if resume:
        batch_id = resume
    else:
        batch_id = client.messages.batches.create(requests=requests).id
    print(f"Batch id: {batch_id} (re-run with --resume {batch_id} if this job times out)")
    deadline = time.time() + timeout_minutes * 60
    while True:
        b = client.messages.batches.retrieve(batch_id)
        if b.processing_status == "ended":
            break
        if time.time() > deadline:
            sys.exit(f"Timed out waiting. Batch {batch_id} keeps running; resume it later.")
        time.sleep(poll_seconds)
    out, errors = {}, {}
    usage = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
    for r in client.messages.batches.results(batch_id):
        if r.result.type != "succeeded":
            errors[r.custom_id] = r.result.type
            continue
        m = r.result.message
        out[r.custom_id] = "".join(c.text for c in m.content if c.type == "text")
        u = m.usage
        usage["input"] += u.input_tokens or 0
        usage["output"] += u.output_tokens or 0
        usage["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
        usage["cache_write"] += getattr(u, "cache_creation_input_tokens", 0) or 0
    print("Usage:", json.dumps(usage), "| failed:", errors or "none")
    return out, errors


def parse_json(text):
    """Model output -> JSON, tolerating a code fence around it."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    return json.loads(t)
