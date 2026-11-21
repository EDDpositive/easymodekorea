const C='emk-ae3e82a1';const PRE=["./", "ja/", "zh-tw/", "zh-cn/", "vi/", "icon-192.png", "manifest.webmanifest", "style.css?v=6c51662a", "app.js?v=624a394b", "changes.html", "about.html", "contact.html", "mobile-data-sim.html", "incheon-airport-to-seoul.html", "maps.html", "taxi.html", "tmoney-subway-bus.html", "seoul-tourist-transit-pass.html", "ktx-train-booking.html", "seoul-to-busan-k-tour-pass.html", "kr-pass-korail-pass.html", "dmz-jsa-tour-booking.html", "jeju-getting-around.html", "restaurant-reservations.html", "food-delivery.html", "translation.html", "tax-free-shopping.html", "luggage-storage.html", "pharmacy-hospital.html", "k-eta-entry-requirements.html", "atm-foreign-card-cash.html", "korea-power-plug-voltage.html", "gimpo-airport-to-seoul.html", "phrases.html", "help.html", "privacy.html", "ja/changes.html", "ja/about.html", "ja/contact.html", "ja/mobile-data-sim.html", "ja/incheon-airport-to-seoul.html", "ja/maps.html", "ja/taxi.html", "ja/tmoney-subway-bus.html", "ja/seoul-tourist-transit-pass.html", "ja/ktx-train-booking.html", "ja/seoul-to-busan-k-tour-pass.html", "ja/kr-pass-korail-pass.html", "ja/dmz-jsa-tour-booking.html", "ja/jeju-getting-around.html", "ja/restaurant-reservations.html", "ja/food-delivery.html", "ja/translation.html", "ja/tax-free-shopping.html", "ja/luggage-storage.html", "ja/pharmacy-hospital.html", "ja/k-eta-entry-requirements.html", "ja/atm-foreign-card-cash.html", "ja/korea-power-plug-voltage.html", "ja/gimpo-airport-to-seoul.html", "ja/phrases.html", "ja/help.html", "ja/privacy.html", "zh-tw/changes.html", "zh-tw/about.html", "zh-tw/contact.html", "zh-tw/mobile-data-sim.html", "zh-tw/incheon-airport-to-seoul.html", "zh-tw/maps.html", "zh-tw/taxi.html", "zh-tw/tmoney-subway-bus.html", "zh-tw/seoul-tourist-transit-pass.html", "zh-tw/ktx-train-booking.html", "zh-tw/seoul-to-busan-k-tour-pass.html", "zh-tw/kr-pass-korail-pass.html", "zh-tw/dmz-jsa-tour-booking.html", "zh-tw/jeju-getting-around.html", "zh-tw/restaurant-reservations.html", "zh-tw/food-delivery.html", "zh-tw/translation.html", "zh-tw/tax-free-shopping.html", "zh-tw/luggage-storage.html", "zh-tw/pharmacy-hospital.html", "zh-tw/k-eta-entry-requirements.html", "zh-tw/atm-foreign-card-cash.html", "zh-tw/korea-power-plug-voltage.html", "zh-tw/gimpo-airport-to-seoul.html", "zh-tw/phrases.html", "zh-tw/help.html", "zh-tw/privacy.html", "zh-cn/changes.html", "zh-cn/about.html", "zh-cn/contact.html", "zh-cn/mobile-data-sim.html", "zh-cn/incheon-airport-to-seoul.html", "zh-cn/maps.html", "zh-cn/taxi.html", "zh-cn/tmoney-subway-bus.html", "zh-cn/seoul-tourist-transit-pass.html", "zh-cn/ktx-train-booking.html", "zh-cn/seoul-to-busan-k-tour-pass.html", "zh-cn/kr-pass-korail-pass.html", "zh-cn/dmz-jsa-tour-booking.html", "zh-cn/jeju-getting-around.html", "zh-cn/restaurant-reservations.html", "zh-cn/food-delivery.html", "zh-cn/translation.html", "zh-cn/tax-free-shopping.html", "zh-cn/luggage-storage.html", "zh-cn/pharmacy-hospital.html", "zh-cn/k-eta-entry-requirements.html", "zh-cn/atm-foreign-card-cash.html", "zh-cn/korea-power-plug-voltage.html", "zh-cn/gimpo-airport-to-seoul.html", "zh-cn/phrases.html", "zh-cn/help.html", "zh-cn/privacy.html", "vi/changes.html", "vi/about.html", "vi/contact.html", "vi/mobile-data-sim.html", "vi/incheon-airport-to-seoul.html", "vi/maps.html", "vi/taxi.html", "vi/tmoney-subway-bus.html", "vi/seoul-tourist-transit-pass.html", "vi/ktx-train-booking.html", "vi/seoul-to-busan-k-tour-pass.html", "vi/kr-pass-korail-pass.html", "vi/dmz-jsa-tour-booking.html", "vi/jeju-getting-around.html", "vi/restaurant-reservations.html", "vi/food-delivery.html", "vi/translation.html", "vi/tax-free-shopping.html", "vi/luggage-storage.html", "vi/pharmacy-hospital.html", "vi/k-eta-entry-requirements.html", "vi/atm-foreign-card-cash.html", "vi/korea-power-plug-voltage.html", "vi/gimpo-airport-to-seoul.html", "vi/phrases.html", "vi/help.html", "vi/privacy.html", "hosts.html", "saved.html", "search.json", "ja/saved.html", "ja/search.json", "zh-tw/saved.html", "zh-tw/search.json", "zh-cn/saved.html", "zh-cn/search.json", "vi/saved.html", "vi/search.json"];
/* EasyModeKorea offline worker. The line above is rewritten by src/build.py on every build.
   Pages: answer from the copy on the phone at once, fetch a fresh copy in the background, and tell
   the page when the fresh copy differs. Versioned files (?v=) never change, so the copy is final. */
const L=new URL(self.location).searchParams.get('l')||'en',D=L==='en'?'':L+'/',LD=['ja/','zh-tw/','zh-cn/','vi/'];
const ROOT=self.registration.scope;
const own=p=>D?p.startsWith(D):!LD.some(x=>p.startsWith(x));
/* Keep the reader's own language (pages and search index), every language's home page, and shared files. */
const MINE=PRE.filter(p=>p.endsWith('/')||!/\.(html|json)$/.test(p)||own(p));
const isPage=u=>u.pathname.endsWith('/')||u.pathname.endsWith('.html');
const keyOf=u=>isPage(u)?u.origin+u.pathname:u.href;
const clean=r=>r.redirected?new Response(r.body,{status:r.status,statusText:r.statusText,headers:r.headers}):r;
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>Promise.all(MINE.map(p=>{const u=new URL(p,ROOT);
  return fetch(new Request(u.href,{cache:'reload'})).then(r=>r.ok?c.put(keyOf(u),clean(r)):null).catch(()=>null)}))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
/* Only what the reader sees counts as newer info: a new stylesheet or script name in the head does not. */
const body=t=>t.slice(Math.max(0,t.indexOf('<body')));
const tell=p=>new Promise(r=>setTimeout(r,1500)).then(()=>self.clients.matchAll({type:'window'})).then(cs=>cs.forEach(cl=>{if(new URL(cl.url).pathname===p)cl.postMessage({t:'upd',p})}));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);if(u.origin!==location.origin||u.pathname.endsWith('/sw.js'))return;
  const nav=r.mode==='navigate',k=nav?u.origin+u.pathname:u.href;
  e.respondWith((async()=>{
    const c=await caches.open(C),hit=await c.match(k);
    if(hit&&u.search.startsWith('?v='))return hit;
    const old=hit&&nav?hit.clone():null;
    const net=fetch(r).then(async res=>{
      if(res.ok&&res.type==='basic'){const fresh=clean(res.clone());
        if(old){const a=await old.text(),b=await fresh.clone().text();await c.put(k,fresh);if(body(a)!==body(b))await tell(u.pathname)}
        else await c.put(k,fresh)}
      return res});
    if(hit){e.waitUntil(net.catch(()=>{}));return hit}
    try{return clean(await net)}catch(err){
      if(nav){const home=await c.match(new URL(D||'./',ROOT).href)||await c.match(ROOT);if(home)return home}
      throw err}
  })())});
