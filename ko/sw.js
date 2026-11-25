/* Offline copy of one page, japan-tax-refund.html. Newest first: the rules are new, so a phone with data always gets the fresh page. */
const C='jpr-12afda06',F='japan-tax-refund.html';
const key=()=>new URL(F,self.registration.scope).href;
self.addEventListener('install',e=>e.waitUntil(caches.open(C).then(c=>c.add(new Request(key(),{cache:'reload'}))).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('jpr-')&&x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin+u.pathname!==key())return;
  e.respondWith((async()=>{const c=await caches.open(C),old=()=>c.match(key());
    const net=fetch(e.request).then(async r=>{if(r.ok)await c.put(key(),r.clone());return r});
    const slow=new Promise(r=>setTimeout(async()=>{const h=await old();if(h)r(h)},3000));
    try{return await Promise.race([net,slow])}catch(err){const h=await old();if(h)return h;throw err}})())});
