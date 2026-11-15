const CACHE = "trivianaut-v34";
const QUESTION_CACHE = "trivianaut-questions";
const PROFILE_CACHE = "trivianaut-profile";
const SHELL = [
  "./",
  "./index.html",
  "./style.css",
  "./app.js",
  "./briefings.js",
  "./fonts/fredoka-latin.woff2",
  "./fonts/fredoka-latin-ext.woff2",
  "./fonts/lilita-latin.woff2",
  "./fonts/lilita-latin-ext.woff2",
  "./manifest.webmanifest",
  "./icon-180.png",
  "./icon-192.png",
  "./icon-512.png",
];

function isQuestions(url) {
  return url.pathname.endsWith("/questions.json") || url.pathname.endsWith("questions.json");
}

function freshFetch(request) {
  if (request.mode === "navigate") {
    return fetch(request.url, { cache: "no-store", credentials: "same-origin", redirect: "follow" });
  }
  return fetch(new Request(request, { cache: "no-store" }));
}

function fromNetwork(request, cacheName) {
  return freshFetch(request).then((response) => {
    if (response.ok) {
      const copy = response.clone();
      caches.open(cacheName).then((cache) => cache.put(request, copy));
    }
    return response;
  }).catch(() => caches.match(request));
}

async function storeFresh(cache, path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(path);
  }
  await cache.put(path, response);
}

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const shell = await caches.open(CACHE);
    await Promise.all(SHELL.map((path) => storeFresh(shell, path)));
    const questions = await caches.open(QUESTION_CACHE);
    const already = await questions.match("./questions.json");
    if (!already) {
      const found = await caches.match("./questions.json");
      if (found) {
        await questions.put("./questions.json", found.clone());
      }
    }
  })());
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys
          .filter((key) => key !== CACHE && key !== QUESTION_CACHE && key !== PROFILE_CACHE)
          .map((key) => caches.delete(key)),
      ))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") {
    return;
  }
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) {
    return;
  }
  event.respondWith(fromNetwork(event.request, isQuestions(url) ? QUESTION_CACHE : CACHE));
});
