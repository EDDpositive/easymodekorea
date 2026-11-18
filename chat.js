/* EasyModeKorea chat assistant. Loaded only when build.py has CHAT_ENDPOINT set.
   Config comes from window.EMK_CHAT (endpoint, lang, page, UI strings). Replies are rendered with
   textContent; only https://easymodekorea.com links become anchors. Nothing is stored. */
(function () {
  const C = window.EMK_CHAT; if (!C || !C.endpoint) return;
  const MAX_TURNS = 6, MAX_LEN = 500;
  const css = `
body{padding-bottom:72px}
.emk-fab{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom));z-index:60;border:0;border-radius:999px;padding:12px 18px;background:var(--brand,#2336e8);color:#fff;font:600 15px/1 var(--body,system-ui);box-shadow:0 6px 20px rgba(14,20,48,.25);cursor:pointer}
.emk-fab:focus-visible,.emk-chat button:focus-visible{outline:3px solid var(--easy,#ffd23f);outline-offset:2px}
.emk-chat{position:fixed;inset:auto 0 0 0;z-index:61;display:flex;flex-direction:column;max-height:85vh;background:var(--surface,#fff);color:var(--ink,#0e1430);border-radius:16px 16px 0 0;box-shadow:0 -8px 30px rgba(14,20,48,.25);font:15px/1.45 var(--body,system-ui)}
@media (min-width:640px){.emk-chat{inset:auto 16px 16px auto;width:380px;max-height:70vh;border-radius:16px}}
.emk-chat[hidden],.emk-fab[hidden]{display:none}
.emk-top{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid var(--line,#dfe3ee)}
.emk-top h2{margin:0;font-size:16px}
.emk-x{border:0;background:none;font:600 14px var(--body,system-ui);color:var(--brand,#2336e8);cursor:pointer;padding:6px}
.emk-log{flex:1;overflow:auto;padding:12px 14px;display:flex;flex-direction:column;gap:8px;min-height:120px}
.emk-m{padding:9px 12px;border-radius:12px;max-width:88%;white-space:pre-wrap;word-wrap:break-word}
.emk-u{align-self:flex-end;background:var(--brand,#2336e8);color:#fff}
.emk-a{align-self:flex-start;background:var(--bg,#f3f5fb)}
.emk-a a{color:var(--brand,#2336e8)}
.emk-note{margin:0;padding:0 14px 8px;font-size:12px;color:var(--muted,#444f6b)}
.emk-f{display:flex;gap:8px;padding:10px 14px calc(10px + env(safe-area-inset-bottom));border-top:1px solid var(--line,#dfe3ee)}
.emk-f textarea{flex:1;resize:none;min-height:44px;max-height:120px;padding:10px;border:1px solid var(--line,#dfe3ee);border-radius:10px;font:16px/1.3 var(--body,system-ui)}
.emk-f button{border:0;border-radius:10px;padding:0 16px;background:var(--brand,#2336e8);color:#fff;font:600 15px var(--body,system-ui);cursor:pointer}
.emk-f button[disabled]{opacity:.5}`;
  const st = document.createElement("style"); st.textContent = css; document.head.append(st);

  const mk = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; };
  const fab = mk("button", "emk-fab", "💬 " + C.open); fab.type = "button"; fab.setAttribute("aria-haspopup", "dialog");
  const box = mk("div", "emk-chat"); box.hidden = true; box.setAttribute("role", "dialog"); box.setAttribute("aria-label", C.title);
  const top = mk("div", "emk-top"); top.append(mk("h2", "", C.title));
  const x = mk("button", "emk-x", C.close); x.type = "button"; top.append(x);
  const log = mk("div", "emk-log"); log.setAttribute("aria-live", "polite");
  const note = mk("p", "emk-note", C.note);
  const form = mk("form", "emk-f");
  const ta = mk("textarea"); ta.maxLength = MAX_LEN; ta.rows = 1; ta.placeholder = C.ph; ta.setAttribute("aria-label", C.ph);
  const send = mk("button", "", C.send); send.type = "submit";
  form.append(ta, send); box.append(top, log, note, form);
  document.body.append(fab, box);

  const history = [];
  function bubble(role, text) {
    const b = mk("div", "emk-m " + (role === "user" ? "emk-u" : "emk-a"));
    if (role === "user") b.textContent = text;
    else text.split(/(https:\/\/easymodekorea\.com\/[^\s)\]]*)/).forEach((part, i) => {
      if (i % 2) { const a = mk("a", "", part.replace(/^https:\/\/easymodekorea\.com\//, "/")); a.href = part; b.append(a); }
      else b.append(document.createTextNode(part));
    });
    log.append(b); log.scrollTop = log.scrollHeight; return b;
  }
  function count(path) { try { window.goatcounter && window.goatcounter.count({ path, title: "chat", event: true }); } catch (e) {} }
  function openBox() { box.hidden = false; fab.hidden = true; ta.focus(); count("chat/open/" + C.lang); }
  function closeBox() { box.hidden = true; fab.hidden = false; fab.focus(); }
  fab.addEventListener("click", openBox); x.addEventListener("click", closeBox);
  document.addEventListener("keydown", ev => { if (ev.key === "Escape" && !box.hidden) closeBox(); });
  ta.addEventListener("keydown", ev => { if (ev.key === "Enter" && !ev.shiftKey && !ev.isComposing) { ev.preventDefault(); form.requestSubmit(); } });

  form.addEventListener("submit", async ev => {
    ev.preventDefault();
    const q = ta.value.trim().slice(0, MAX_LEN); if (!q || send.disabled) return;
    ta.value = ""; bubble("user", q); history.push({ role: "user", content: q });
    send.disabled = true; const wait = bubble("assistant", "…");
    try {
      const r = await fetch(C.endpoint, { method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ lang: C.lang, page: C.page, messages: history.slice(-MAX_TURNS * 2) }) });
      const d = await r.json().catch(() => ({}));
      wait.remove();
      if (!r.ok || !d.reply) { bubble("assistant", d.error || C.err); history.pop(); }
      else { bubble("assistant", d.reply); history.push({ role: "assistant", content: d.reply }); }
      count("chat/ask/" + C.lang);
    } catch (e) { wait.remove(); bubble("assistant", C.err); history.pop(); }
    send.disabled = false; ta.focus();
  });
})();
