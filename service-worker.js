// NGIS Service Worker (v1.0.0)
// Provides clean lifecycle hooks and cache management without blocking navigation
self.addEventListener('install', function (event) {
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', function (event) {
  // Let browser handle requests normally
  return;
});
