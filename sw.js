// SyllaBot Service Worker
// Strategy: NetworkFirst for HTML/API, CacheFirst for static assets
// Auth exclusion: never cache Supabase auth responses

const CACHE_NAME = 'syllabot-v1';

const PRECACHE_URLS = [
  '/SyllabusMaster/index.html',
  '/SyllabusMaster/auth.html',
  '/SyllabusMaster/dashboard.html',
  '/SyllabusMaster/reset.html',
];

// ── Install: precache HTML pages ──
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

// ── Activate: clean up old caches ──
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

// ── Fetch: route requests to correct strategy ──
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Never cache Supabase auth responses
  if (url.hostname.includes('supabase.co') && url.pathname.includes('/auth/')) return;

  // Static assets: CacheFirst
  const isStaticAsset = /\.(js|css|woff2?|ttf|png|svg|jpg|jpeg|ico|webp)(\?.*)?$/.test(url.pathname);
  const isCrossOrigin = url.origin !== self.location.origin;

  if (isStaticAsset || isCrossOrigin) {
    event.respondWith(cacheFirst(request));
    return;
  }

  // HTML and same-origin API: NetworkFirst
  event.respondWith(networkFirst(request));
});

// ── NetworkFirst: try network, fall back to cache ──
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    const cached = await caches.match(request);
    if (cached) return cached;
    return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
  }
}

// ── CacheFirst: try cache, fall back to network ──
async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
  }
}
