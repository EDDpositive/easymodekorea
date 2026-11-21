/* What a reader has to read on a phone screen. first: words on the first screen; sentences: text pieces on the first
   screen longer than 8 words; all: words on the whole page with closed sections left closed. CJK: one word per two characters.
   Fixed bars (tabs, notices) are left out. Same counting is used for the benchmark apps in docs/critique.md 26차. */
(() => {
  const C = /[぀-ヿ㐀-鿿가-힯]/g;
  const words = s => Math.round((s.match(C) || []).length / 2) + s.replace(C, " ").split(/\s+/).filter(w => /[\p{L}\p{N}]/u.test(w)).length;
  const H = innerHeight, W = innerWidth;
  let first = 0, sentences = 0, all = 0;
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walk.nextNode(); n; n = walk.nextNode()) {
    const p = n.parentElement; if (!p || !n.textContent.trim() || p.closest("script,style,noscript,[hidden],svg,.tabbar,.sr,.skip")) continue;
    const cs = getComputedStyle(p); if (cs.display === "none" || cs.visibility === "hidden" || cs.position === "fixed") continue;
    const d = p.closest("details"); if (d && !d.open && !p.closest("summary")) continue;
    const r = document.createRange(); r.selectNodeContents(n); const b = r.getBoundingClientRect();
    if (!b.width || !b.height || b.left >= W || b.right <= 0) continue;
    const w = words(n.textContent); all += w;
    if (b.top + scrollY < H) { first += w; if (w > 8) sentences++; }
  }
  return { first, sentences, all };
})()
