/* Offline copy of the daily price game, separate from the rest of the site. Newest first; the saved copy answers without a connection or after three seconds.
   Only the languages opened on this phone are kept. */
const C='won-d9e2e450',S=self.registration.scope;
const key=u=>{u=new URL(u);return u.origin+u.pathname.replace(/index\.html$/,'')};
const fresh=u=>new Request(u,{cache:'reload'});
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil((async()=>{
  const c=await caches.open(C),old=(await caches.keys()).filter(k=>k.startsWith('won-')&&k!==C),want=new Map();
  for(const k of old){const o=await caches.open(k);for(const r of await o.keys())want.set(r.url,await o.match(r))}
  for(const w of await self.clients.matchAll({includeUncontrolled:true,type:'window'}))if(w.url.startsWith(S)&&!want.has(key(w.url)))want.set(key(w.url),null);
  for(const[u,was]of want){try{await c.add(fresh(u))}catch(x){if(was)await c.put(u,was)}}
  await Promise.all(old.map(k=>caches.delete(k)));await self.clients.claim()})()));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||!r.url.startsWith(S))return;const k=key(r.url);
  e.respondWith((async()=>{const c=await caches.open(C),old=()=>c.match(k);
    const net=fetch(r).then(async x=>{if(x.ok)await c.put(k,x.clone());return x});
    const slow=new Promise(y=>setTimeout(async()=>{const h=await old();if(h)y(h)},3000));
    try{return await Promise.race([net,slow])}catch(x){const h=await old();if(h)return h;if(r.mode==='navigate'){const any=(await c.keys()).find(q=>q.url.endsWith('/'));if(any)return c.match(any)}throw x}})())});
