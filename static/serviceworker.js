// // static/serviceworker.js
// self.addEventListener("install", function (event) {
//     console.log("Service Worker installed");
//   });
  
//   self.addEventListener("fetch", function (event) {
//     // Basic fetch handler
//   });
  
self.addEventListener('install', function(e) {
    console.log('Service Worker installed');
    e.waitUntil(
      caches.open('v1').then(function(cache) {
        return cache.addAll([
          '/',  // cache home page
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', function(e) {
    e.respondWith(
      caches.match(e.request).then(function(response) {
        return response || fetch(e.request);
      })
    );
  });
  