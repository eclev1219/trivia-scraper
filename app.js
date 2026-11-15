const STATS_KEY = "trivia-stats";
const SETTINGS_KEY = "trivia-settings";
const FLIGHT_KEY = "trivia-flight-speed";

const DAILY_KEY = "trivia-daily";
const DAILY_DUST = 5;

const screens = {
  home: document.querySelector("#home"),
  trivia: document.querySelector("#trivia"),
  daily: document.querySelector("#daily"),
  stats: document.querySelector("#stats"),
  species: document.querySelector("#species"),
  shop: document.querySelector("#shop"),
  hangar: document.querySelector("#hangar"),
  settings: document.querySelector("#settings"),
};

let questions = [];
let deck = [];
let lastQuestion = null;
let current = null;
let sessionCorrect = 0;
let answeredThisCard = false;

let stats = loadJson(STATS_KEY, {
  answered: 0,
  correct: 0,
  currentStreak: 0,
  longestStreak: 0,
  sessions: 0,
  bestSession: 0,
  furthestCheckpoint: 0,
  categories: {},
  dust: 0,
  aliens: [],
  ships: ["dart"],
  ship: "dart",
});

const BOX_COST = 100;
const DUPLICATE_REFUND = 40;

const ALIENS = [
  { id: "blobby", name: "Blobby McFloat", rarity: "common", note: "A polite sphere who apologizes to asteroids." },
  { id: "noodle", name: "Noodle Neck", rarity: "common", note: "The neck arrived three weeks before the rest of him." },
  { id: "whiskers", name: "Captain Whiskers", rarity: "uncommon", note: "Claims to be a captain. The helmet is a yogurt lid." },
  { id: "square", name: "Square Dad", rarity: "uncommon", note: "Says he is a rectangle, actually, then laughs too long." },
  { id: "honk", name: "The Honk", rarity: "rare", note: "Honks in Morse code. Nobody has translated one." },
  { id: "dave", name: "Orbit Dave", rarity: "rare", note: "His head is a tiny planet. The moon is a freeloader." },
  { id: "glitter", name: "Glitter Goblin", rarity: "legendary", note: "Leaves sparkles in the airlock and denies everything." },
  { id: "gloop", name: "Empress Gloop", rarity: "legendary", note: "Rules a damp moon. The crown keeps sliding off." },
  { id: "pip", name: "Pip", rarity: "common", note: "A triangle who insists triangles are the friendly shape." },
  { id: "moth", name: "Marge the Moth", rarity: "common", note: "Flew into a station porch light and never left." },
  { id: "beak", name: "Professor Beak", rarity: "uncommon", note: "The lecture slides are just the word HONK." },
  { id: "sock", name: "Sock Steve", rarity: "uncommon", note: "Steve is a sock. Steve has dreams." },
  { id: "croissant", name: "Count Croissant", rarity: "rare", note: "A pastry count. The crumbs are a navigation hazard." },
  { id: "lantern", name: "Lady Lantern", rarity: "rare", note: "Lights the way, then asks if you brought snacks." },
  { id: "shedeur", name: "Shedeur", rarity: "rare", note: "Browns No. 2, an AP on the wrist, and a smile wider than the end zone." },
  { id: "kevin", name: "Kevin", rarity: "rare", note: "Two eyes, blue overalls, and a grin that survives reentry." },
  { id: "chewie", name: "Chewbacca", rarity: "rare", note: "A tall walk of brown fur and a bandolier. The roar is a full sentence." },
  { id: "grogu", name: "Grogu", rarity: "rare", note: "Green ears, a brown robe, and a very serious snack policy." },
  { id: "rocket", name: "Rocket", rarity: "rare", note: "A small raccoon in an orange flight suit. The attitude is extra." },
  { id: "groot", name: "Groot", rarity: "rare", note: "A sapling with a three-word vocabulary and excellent posture." },
  { id: "wobble", name: "King Wobble", rarity: "legendary", note: "Three blobs in a trench coat, and a crown." },
  { id: "quiet", name: "The Quiet Comet", rarity: "legendary", note: "Says nothing. The silence is very loud." },
];

const SHIPS = [
  { id: "dart", name: "Dart", rarity: "common", note: "The first ship. Pointy, proud, slightly used." },
  { id: "saucer", name: "Saucer Scout", rarity: "common", note: "A rental saucer with one cup holder." },
  { id: "pencil", name: "Pencil Rocket", rarity: "uncommon", note: "Writes its name on the sky. The eraser still works." },
  { id: "teapot", name: "Teapot", rarity: "uncommon", note: "Short trips only. The spout whistles at light speed." },
  { id: "fish", name: "Fish Ship", rarity: "rare", note: "Swims through vacuum out of sheer confidence." },
  { id: "boot", name: "Boot", rarity: "rare", note: "Left behind by a giant. Surprisingly aerodynamic." },
  { id: "crown", name: "Crown Cruiser", rarity: "legendary", note: "Every window has a tiny curtain." },
  { id: "potato", name: "Comet Potato", rarity: "legendary", note: "It is a potato. It is also, somehow, very fast." },
  { id: "plane", name: "Paper Plane", rarity: "common", note: "Folded during a boring briefing. It escaped." },
  { id: "thimble", name: "Thimble", rarity: "common", note: "Sews through asteroid fields. Very brave for its size." },
  { id: "accordion", name: "Accordion", rarity: "uncommon", note: "Every note is also a course correction." },
  { id: "porch", name: "Porch Light", rarity: "uncommon", note: "A porch light with ambitions and a little door." },
  { id: "sub", name: "Vacuum Sub", rarity: "rare", note: "Still checks for water. There is no water." },
  { id: "hat", name: "Top Hat", rarity: "rare", note: "Tips itself when it passes a planet." },
  { id: "biscotti", name: "Biscotti", rarity: "rare", note: "A purple brontosaurus with a green belly. The neck is the antenna." },
  { id: "gru", name: "Gru's Ship", rarity: "rare", note: "A tall silver rocket with a red stripe. The fins mean business." },
  { id: "falcon", name: "Millennium Falcon", rarity: "rare", note: "A round freighter with a side cockpit and two front mandibles." },
  { id: "iron", name: "Iron Suit", rarity: "rare", note: "Red and gold, flying without a ship. The chest light is the engine." },
  { id: "whale", name: "Choir Whale", rarity: "legendary", note: "Sings directions. The chorus lasts four hours." },
  { id: "disco", name: "Disco Ball", rarity: "legendary", note: "The dance floor is the engine. Please hold on." },
];

const RARITY_WEIGHT = [
  ["common", 55],
  ["uncommon", 28],
  ["rare", 13],
  ["legendary", 4],
];

function normalizeStats() {
  if (!Array.isArray(stats.aliens)) {
    stats.aliens = [];
  }
  if (!Array.isArray(stats.ships) || stats.ships.length === 0) {
    stats.ships = ["dart"];
  }
  if (!stats.ships.includes("dart")) {
    stats.ships.unshift("dart");
  }
  if (!stats.ship || !stats.ships.includes(stats.ship)) {
    stats.ship = "dart";
  }
  if (typeof stats.rider !== "string" || !stats.aliens.includes(stats.rider)) {
    stats.rider = "";
  }
  if (!Number.isFinite(stats.dust)) {
    stats.dust = 0;
  }
  if (!stats.categories || typeof stats.categories !== "object") {
    stats.categories = {};
  }
}

normalizeStats();

let settings = loadJson(SETTINGS_KEY, {
  theme: "ink",
  music: "off",
});

const PREFERRED_CATEGORIES = new Set([
  "History",
  "Geography",
  "Animals",
  "General Knowledge",
  "Science & Nature",
]);

let audioContext = null;
let musicMaster = null;
let musicHums = [];
let musicBeds = [];
let musicNoise = null;
let musicGeneration = 0;

function loadJson(key, fallback) {
  try {
    const saved = localStorage.getItem(key);
    if (!saved) {
      return fallback;
    }
    return { ...fallback, ...JSON.parse(saved) };
  } catch {
    return fallback;
  }
}

const SAVE_DB = "trivianaut-save";
const SAVE_STORE = "kv";
let saveDbPromise = null;

function openSaveDb() {
  if (saveDbPromise) {
    return saveDbPromise;
  }
  saveDbPromise = new Promise((resolve, reject) => {
    if (!("indexedDB" in window)) {
      reject(new Error("indexedDB unavailable"));
      return;
    }
    const request = indexedDB.open(SAVE_DB, 1);
    request.onupgradeneeded = () => {
      if (!request.result.objectStoreNames.contains(SAVE_STORE)) {
        request.result.createObjectStore(SAVE_STORE);
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  }).catch((error) => {
    saveDbPromise = null;
    throw error;
  });
  return saveDbPromise;
}

function idbGet(key) {
  return openSaveDb().then((db) => new Promise((resolve, reject) => {
    const request = db.transaction(SAVE_STORE, "readonly").objectStore(SAVE_STORE).get(key);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  }));
}

function idbSet(key, value) {
  return openSaveDb().then((db) => new Promise((resolve, reject) => {
    const tx = db.transaction(SAVE_STORE, "readwrite");
    tx.objectStore(SAVE_STORE).put(value, key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  }));
}

const PROFILE_CACHE = "trivianaut-profile";

function profileRequest(key) {
  return new Request(`./save/${key}`);
}

function cacheSave(key, record) {
  if (!("caches" in window)) {
    return Promise.resolve();
  }
  return caches.open(PROFILE_CACHE).then((cache) => cache.put(
    profileRequest(key),
    new Response(JSON.stringify(record), { headers: { "Content-Type": "application/json" } }),
  ));
}

function cacheLoad(key) {
  if (!("caches" in window)) {
    return Promise.resolve(null);
  }
  return caches.open(PROFILE_CACHE).then((cache) => cache.match(profileRequest(key))).then((response) => {
    if (!response) {
      return null;
    }
    return response.json();
  }).catch(() => null);
}

function saveJson(key, value) {
  const record = { ...value, savedAt: Date.now() };
  try {
    localStorage.setItem(key, JSON.stringify(record));
  } catch {
    // The phone can refuse localStorage when storage is full. The other copies still get the save.
  }
  idbSet(key, record).catch(() => {});
  cacheSave(key, record).catch(() => {});
}

function readDaily() {
  try {
    return JSON.parse(localStorage.getItem(DAILY_KEY) || "null");
  } catch {
    return null;
  }
}

function progressScore(record) {
  if (!record || typeof record !== "object") {
    return -1;
  }
  const ships = Array.isArray(record.ships) ? record.ships.length : 0;
  const aliens = Array.isArray(record.aliens) ? record.aliens.length : 0;
  return (Number(record.answered) || 0) * 1000
    + (Number(record.dust) || 0)
    + (Number(record.longestStreak) || 0)
    + ships * 50
    + aliens * 50;
}

function restoreSaves() {
  if (navigator.storage && navigator.storage.persist) {
    navigator.storage.persist().catch(() => {});
  }
  return Promise.all([
    idbGet(STATS_KEY).catch(() => null),
    cacheLoad(STATS_KEY),
    idbGet(SETTINGS_KEY).catch(() => null),
    cacheLoad(SETTINGS_KEY),
    idbGet(DAILY_KEY).catch(() => null),
    cacheLoad(DAILY_KEY),
    idbGet(FLIGHT_KEY).catch(() => null),
    cacheLoad(FLIGHT_KEY),
  ]).then(([idbStats, cachedStats, idbSettings, cachedSettings, idbDaily, cachedDaily, idbFlight, cachedFlight]) => {
    const savedStats = progressScore(cachedStats) > progressScore(idbStats) ? cachedStats : idbStats;
    const savedSettings = (cachedSettings && (Number(cachedSettings.savedAt) || 0) > (idbSettings ? Number(idbSettings.savedAt) || 0 : 0))
      ? cachedSettings
      : idbSettings;
    const savedDaily = (cachedDaily && cachedDaily.date && !(idbDaily && idbDaily.date)) ? cachedDaily : (idbDaily || cachedDaily);
    const savedFlight = idbFlight || cachedFlight;
    const localScore = progressScore(stats);
    const savedScore = progressScore(savedStats);
    if (savedScore > localScore) {
      Object.assign(stats, savedStats);
      normalizeStats();
      try {
        localStorage.setItem(STATS_KEY, JSON.stringify(stats));
      } catch {
        // Keep the other copies if the phone will not accept localStorage.
      }
      noteCheckpoint(stats.currentStreak);
    }
    idbSet(STATS_KEY, { ...stats, savedAt: stats.savedAt || Date.now() }).catch(() => {});
    cacheSave(STATS_KEY, { ...stats, savedAt: stats.savedAt || Date.now() }).catch(() => {});

    const localSettingsAt = Number(settings.savedAt) || 0;
    const savedSettingsAt = savedSettings ? Number(savedSettings.savedAt) || 0 : 0;
    if (savedSettings && savedSettingsAt > localSettingsAt) {
      settings.theme = savedSettings.theme || settings.theme;
      settings.music = savedSettings.music || settings.music;
      settings.savedAt = savedSettingsAt;
      try {
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
      } catch {
        // The backup copies still have the theme and music.
      }
      applyTheme(settings.theme);
    }
    const settingsRecord = { ...settings, savedAt: settings.savedAt || Date.now() };
    idbSet(SETTINGS_KEY, settingsRecord).catch(() => {});
    cacheSave(SETTINGS_KEY, settingsRecord).catch(() => {});
    for (const button of document.querySelectorAll("[data-music-choice]")) {
      button.classList.toggle("selected", button.dataset.musicChoice === settings.music);
    }

    let localDaily = readDaily();
    if (savedDaily && savedDaily.date && !(localDaily && localDaily.date)) {
      localDaily = savedDaily;
      try {
        localStorage.setItem(DAILY_KEY, JSON.stringify(savedDaily));
      } catch {
        // The backup copies still know today's challenge is done.
      }
    }
    if (localDaily && localDaily.date) {
      const dailyRecord = { ...localDaily, savedAt: localDaily.savedAt || Date.now() };
      idbSet(DAILY_KEY, dailyRecord).catch(() => {});
      cacheSave(DAILY_KEY, dailyRecord).catch(() => {});
    }

    const savedSpeed = savedFlight && Number(savedFlight.value);
    if ((!Number.isFinite(flightSpeed) || flightSpeed <= 1) && Number.isFinite(savedSpeed) && savedSpeed > 1) {
      flightSpeed = savedSpeed;
      try {
        localStorage.setItem(FLIGHT_KEY, String(flightSpeed));
      } catch {
        // Speed is also stored with the other backups.
      }
    }
    if (Number.isFinite(flightSpeed) && flightSpeed > 0) {
      const speedRecord = { value: flightSpeed, savedAt: Date.now() };
      idbSet(FLIGHT_KEY, speedRecord).catch(() => {});
      cacheSave(FLIGHT_KEY, speedRecord).catch(() => {});
    }
    showDust();
  }).catch(() => {});
}

let currentScreen = "home";

function show(name) {
  currentScreen = name;
  for (const screen of Object.values(screens)) {
    screen.classList.add("hidden");
  }
  screens[name].classList.remove("hidden");
}

function shuffle(items) {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swap = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[swap]] = [copy[swap], copy[index]];
  }
  return copy;
}

function isBirthYear(question) {
  return /(?:in which year was|what year was|when was).+ born/i.test(question.question);
}

const FUN_CATEGORIES = new Set([
  "General Knowledge",
  "Food & Drink",
  "Film & TV",
  "Music",
  "Sports",
  "Sport & Leisure",
  "Entertainment: Film",
  "Entertainment: Television",
  "Entertainment: Music",
  "Entertainment: Books",
  "Mythology",
  "Art",
  "Animals",
]);

function buildDeck() {
  const fun = [];
  const preferred = [];
  const births = [];
  const others = [];
  for (const question of questions) {
    if (isBirthYear(question)) {
      births.push(question);
      continue;
    }
    if (question.source === "original" || FUN_CATEGORIES.has(question.category)) {
      fun.push(question);
    } else if (PREFERRED_CATEGORIES.has(question.category)) {
      preferred.push(question);
    } else {
      others.push(question);
    }
  }
  // Fun general-knowledge questions come up most. Only a small handful of birth years stay in rotation.
  const rareBirths = shuffle(births).slice(0, 80);
  return shuffle([...fun, ...fun, ...fun, ...preferred, ...preferred, ...others, ...rareBirths]);
}

function drawQuestion() {
  if (deck.length === 0) {
    deck = buildDeck();
    if (deck.length > 1 && deck[deck.length - 1] === lastQuestion) {
      [deck[0], deck[deck.length - 1]] = [deck[deck.length - 1], deck[0]];
    }
  }
  lastQuestion = deck.pop();
  return lastQuestion;
}

function showQuestion() {
  current = drawQuestion();
  answeredThisCard = false;
  document.querySelector("#question-meta").textContent = current.category;
  document.querySelector("#question-text").textContent = current.question;

  const choices = document.querySelector("#choices");
  choices.replaceChildren();
  const answers = shuffle([current.correct_answer, ...current.incorrect_answers]);
  for (const answer of answers) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = answer;
    button.addEventListener("click", () => grade(button, answer));
    choices.appendChild(button);
  }
  document.querySelector("#next-question").classList.add("hidden");
  document.querySelector("#reward").classList.add("hidden");
  hideBriefing();
}

function grade(button, answer) {
  if (answeredThisCard) {
    return;
  }
  answeredThisCard = true;

  const correct = answer === current.correct_answer;
  stats.answered += 1;
  noteCategory(current.category, correct);

  if (correct) {
    stats.correct += 1;
    stats.currentStreak += 1;
    sessionCorrect += 1;
    stats.longestStreak = Math.max(stats.longestStreak, stats.currentStreak);
    stats.bestSession = Math.max(stats.bestSession, sessionCorrect);
    noteCheckpoint(stats.currentStreak);
    const gained = stats.currentStreak;
    stats.dust += gained;
    riderCheer = performance.now();
    const alien = discoverAlien(current.difficulty);
    showReward(gained, alien);
    button.classList.add("correct");
    changeFlightSpeed(true);
  } else {
    stats.currentStreak = 0;
    clearCheckpoint();
    changeFlightSpeed(false);
    button.classList.add("wrong");
    for (const choice of document.querySelectorAll("#choices button")) {
      if (choice.textContent === current.correct_answer) {
        choice.classList.add("correct");
      }
    }
  }

  for (const choice of document.querySelectorAll("#choices button")) {
    choice.disabled = true;
  }
  saveJson(STATS_KEY, stats);
  showBriefing(current);
  document.querySelector("#next-question").classList.remove("hidden");
}

function briefingKey(text) {
  return text
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function findBriefing(question) {
  if (!question || question.difficulty === "easy" || typeof BRIEFINGS === "undefined") {
    return "";
  }
  const answerKey = briefingKey(question.correct_answer);
  if (BRIEFINGS.has(answerKey)) {
    return BRIEFINGS.get(answerKey);
  }
  const text = ` ${briefingKey(question.question)} `;
  let bestKey = "";
  let note = "";
  for (const [key, value] of BRIEFINGS) {
    if (key.length < 3 || key.length <= bestKey.length) {
      continue;
    }
    if (text.includes(` ${key} `)) {
      bestKey = key;
      note = value;
    }
  }
  return note;
}

function hideBriefing() {
  const note = document.querySelector("#briefing");
  note.textContent = "";
  note.classList.add("hidden");
}

function showBriefing(question) {
  const note = document.querySelector("#briefing");
  const text = findBriefing(question);
  note.textContent = text;
  note.classList.toggle("hidden", text === "");
}

function accuracy() {
  if (stats.answered === 0) {
    return "—";
  }
  return `${Math.round((stats.correct / stats.answered) * 1000) / 10}%`;
}

const CHECKPOINTS = [
  "Mars",
  "Saturn",
  "Pluto",
  "Moon",
  "Jupiter",
  "Venus",
  "Mercury",
  "Neptune",
  "Uranus",
  "Sun",
  "Asteroid",
  "Comet",
  "Eclipse",
  "Nebula",
  "Supernova",
  "Black hole",
  "Galaxy",
  "Pulsar",
  "Constellation",
  "Quasar",
];

function checkpointName(level) {
  if (!level || level < 1) {
    return "—";
  }
  return CHECKPOINTS[Math.min(level, CHECKPOINTS.length) - 1];
}

function categoryPlays(record) {
  if (typeof record === "number") {
    return record;
  }
  if (!record || typeof record !== "object") {
    return 0;
  }
  return record.played || 0;
}

function noteCategory(name, wasCorrect) {
  const current = stats.categories[name];
  const record = current && typeof current === "object"
    ? current
    : { played: Number(current) || 0, tracked: 0, correct: 0 };
  record.played += 1;
  record.tracked += 1;
  if (wasCorrect) {
    record.correct += 1;
  }
  stats.categories[name] = record;
}

function favoriteCategory() {
  const entries = Object.entries(stats.categories);
  if (entries.length === 0) {
    return "—";
  }
  entries.sort((a, b) => categoryPlays(b[1]) - categoryPlays(a[1]));
  return entries[0][0];
}

function bestAccuracyCategory() {
  const ranked = [];
  for (const [name, record] of Object.entries(stats.categories)) {
    if (!record || typeof record !== "object" || record.tracked < 3) {
      continue;
    }
    ranked.push({
      name,
      rate: record.correct / record.tracked,
      tracked: record.tracked,
    });
  }
  if (ranked.length === 0) {
    return "—";
  }
  ranked.sort((a, b) => b.rate - a.rate || b.tracked - a.tracked);
  const best = ranked[0];
  const percent = Math.round(best.rate * 1000) / 10;
  return `${best.name} · ${percent}%`;
}

function renderStats() {
  const rows = [
    ["Longest streak", stats.longestStreak],
    ["Lifetime correct", accuracy()],
    ["Answered", stats.answered],
    ["Current streak", stats.currentStreak],
    ["Sessions", stats.sessions],
    ["Best session", stats.bestSession],
    ["Most played", favoriteCategory()],
    ["Best accuracy", bestAccuracyCategory()],
    ["Furthest checkpoint", checkpointName(stats.furthestCheckpoint)],
    ["Space dust", stats.dust],
    ["Aliens met", `${stats.aliens.length} / ${ALIENS.length}`],
    ["Ships", `${stats.ships.length} / ${SHIPS.length}`],
  ];
  const list = document.querySelector("#stat-list");
  list.replaceChildren();
  for (const [label, value] of rows) {
    const item = document.createElement("div");
    const term = document.createElement("dt");
    const detail = document.createElement("dd");
    term.textContent = label;
    detail.textContent = value;
    item.append(term, detail);
    list.appendChild(item);
  }
  showDust();
}

function findById(list, id) {
  return list.find((item) => item.id === id);
}

function weightedPick(pool) {
  const weights = { common: 10, uncommon: 5, rare: 2, legendary: 1 };
  const total = pool.reduce((sum, item) => sum + weights[item.rarity], 0);
  let roll = Math.random() * total;
  for (const item of pool) {
    roll -= weights[item.rarity];
    if (roll <= 0) {
      return item;
    }
  }
  return pool[pool.length - 1];
}

function discoverAlien(difficulty) {
  const chance = difficulty === "hard" ? 0.22 : difficulty === "medium" ? 0.08 : 0;
  if (Math.random() >= chance) {
    return null;
  }
  const missing = ALIENS.filter((alien) => !stats.aliens.includes(alien.id));
  if (missing.length === 0) {
    return null;
  }
  const alien = weightedPick(missing);
  stats.aliens.push(alien.id);
  spawnGuest(alien.id);
  openReveal("alien", alien.id, alien.name, alien.note);
  return alien;
}

function showReward(gained, alien) {
  const note = document.querySelector("#reward");
  const dust = `+${gained} space dust`;
  note.textContent = alien ? `${dust}. ${alien.name} waved from the stars.` : dust;
  note.classList.remove("hidden");
  showDust();
}

function showDust() {
  const label = `${stats.dust} space dust`;
  document.querySelector("#dust-home").textContent = label;
  document.querySelector("#dust-shop").textContent = label;
  const button = document.querySelector("#buy-box");
  button.disabled = stats.dust < BOX_COST;
  const savedDaily = readDaily();
  const dailyButton = document.querySelector("#open-daily");
  dailyButton.textContent = savedDaily && savedDaily.date === dailyDate() && savedDaily.done
    ? "Daily challenge · done"
    : "Daily challenge";
}

function rollRarity() {
  const roll = Math.random() * 100;
  let cursor = 0;
  for (const [name, weight] of RARITY_WEIGHT) {
    cursor += weight;
    if (roll < cursor) {
      return name;
    }
  }
  return "common";
}

function pickMysteryShip() {
  const rarity = rollRarity();
  const ofRarity = SHIPS.filter((ship) => ship.rarity === rarity);
  const fresh = ofRarity.filter((ship) => !stats.ships.includes(ship.id));
  const repeats = ofRarity.filter((ship) => stats.ships.includes(ship.id));
  const repeatRoll = Math.random() < 0.32;
  if (fresh.length > 0 && !(repeatRoll && repeats.length > 0)) {
    return { ship: fresh[Math.floor(Math.random() * fresh.length)], duplicate: false };
  }
  if (repeats.length > 0) {
    return { ship: repeats[Math.floor(Math.random() * repeats.length)], duplicate: true };
  }
  const anyFresh = SHIPS.filter((ship) => !stats.ships.includes(ship.id));
  if (anyFresh.length > 0) {
    return { ship: anyFresh[Math.floor(Math.random() * anyFresh.length)], duplicate: false };
  }
  const owned = SHIPS.filter((ship) => stats.ships.includes(ship.id));
  return { ship: owned[Math.floor(Math.random() * owned.length)], duplicate: true };
}

function buyMysteryBox() {
  if (stats.dust < BOX_COST || revealState) {
    return;
  }
  stats.dust -= BOX_COST;
  const { ship, duplicate } = pickMysteryShip();
  const note = document.querySelector("#shop-note");
  note.classList.remove("hidden");
  if (duplicate) {
    stats.dust += DUPLICATE_REFUND;
    note.textContent = `The ${ship.name} was already in the hangar. ${DUPLICATE_REFUND} dust drifted back.`;
    openReveal(
      "duplicate",
      ship.id,
      ship.name,
      `Already in the hangar. ${DUPLICATE_REFUND} dust drifted back.`,
    );
  } else {
    stats.ships.push(ship.id);
    const article = "aeiou".includes(ship.rarity[0]) ? "an" : "a";
    note.textContent = `The box popped open: ${ship.name}, ${article} ${ship.rarity} ship.`;
    openReveal("ship", ship.id, ship.name, `${article} ${ship.rarity} ship`);
  }
  saveJson(STATS_KEY, stats);
  renderShop();
}

let revealState = null;
let revealFrame = 0;

function easeOutBack(amount) {
  const overshoot = 1.70158;
  const scaled = overshoot + 1;
  return 1 + scaled * (amount - 1) ** 3 + overshoot * (amount - 1) ** 2;
}

function openReveal(kind, id, title, note) {
  const celebrate = kind !== "duplicate";
  const sparks = Array.from({ length: celebrate ? 18 : 8 }, (_, index) => ({
    angle: (index / (celebrate ? 18 : 8)) * Math.PI * 2 + Math.random() * 0.4,
    speed: celebrate ? 46 + Math.random() * 70 : 18 + Math.random() * 22,
    size: 1.6 + Math.random() * 2.2,
    color: celebrate
      ? ["#f4d35e", "#f7f4ee", "#9fd0ff", "#8fd0a8"][index % 4]
      : "#8d8478",
  }));
  revealState = { kind, id, title, started: performance.now(), sparks };
  const root = document.querySelector("#reveal");
  root.classList.remove("hidden", "celebrate", "shrug");
  root.classList.add(celebrate ? "celebrate" : "shrug");
  document.querySelector("#reveal-kicker").textContent = kind === "alien"
    ? "New alien"
    : kind === "ship"
      ? "New ship"
      : "Repeat ship";
  document.querySelector("#reveal-title").textContent = title;
  document.querySelector("#reveal-note").textContent = note;
  cancelAnimationFrame(revealFrame);
  const loop = (now) => {
    paintReveal(now);
    if (revealState) {
      revealFrame = requestAnimationFrame(loop);
    }
  };
  revealFrame = requestAnimationFrame(loop);
}

function closeReveal() {
  revealState = null;
  cancelAnimationFrame(revealFrame);
  document.querySelector("#reveal").classList.add("hidden");
}

function paintCrate(ctx, open, shrug) {
  ctx.fillStyle = shrug ? "#b7aa9a" : "#c9843a";
  ctx.fillRect(-28, -16, 56, 38);
  ctx.strokeStyle = shrug ? "#7d7468" : "#8a5420";
  ctx.lineWidth = 2;
  ctx.strokeRect(-28, -16, 56, 38);
  ctx.beginPath();
  ctx.moveTo(-28, 3);
  ctx.lineTo(28, 3);
  ctx.moveTo(0, -16);
  ctx.lineTo(0, 22);
  ctx.stroke();
  ctx.save();
  ctx.translate(0, -16);
  ctx.rotate(-(shrug ? open * 0.28 : open * 1.2));
  ctx.fillStyle = shrug ? "#cfc6b8" : "#e0a45a";
  ctx.fillRect(-30, -11, 60, 12);
  ctx.restore();
  if (open < 0.35) {
    ctx.fillStyle = "#1b1916";
    ctx.font = "700 18px Fredoka, sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("?", 0, 2);
  }
}

function paintReveal(now) {
  if (!revealState) {
    return;
  }
  const canvas = document.querySelector("#reveal-stage");
  const ctx = canvas.getContext("2d");
  const width = 280;
  const height = 180;
  const ratio = window.devicePixelRatio || 1;
  if (canvas.width !== Math.floor(width * ratio) || canvas.height !== Math.floor(height * ratio)) {
    canvas.width = Math.floor(width * ratio);
    canvas.height = Math.floor(height * ratio);
  }
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.clearRect(0, 0, width, height);
  const elapsed = (now - revealState.started) / 1000;
  const shrug = revealState.kind === "duplicate";
  const opened = revealState.kind === "alien"
    ? Math.min(1, elapsed / 0.34)
    : Math.min(1, Math.max(0, (elapsed - 0.42) / 0.38));
  const accent = getComputedStyle(document.body).getPropertyValue("--accent").trim() || "#e07a3d";
  const shake = elapsed < 0.5 ? Math.sin(elapsed * 46) * (1 - elapsed / 0.5) * (shrug ? 2 : 5) : 0;

  if (revealState.kind !== "alien") {
    ctx.save();
    ctx.translate(width / 2 + shake, height * 0.76);
    ctx.globalAlpha = 1 - opened * (shrug ? 0.55 : 0.85);
    paintCrate(ctx, opened, shrug);
    ctx.restore();
  }

  if (opened > 0) {
    const pop = easeOutBack(opened);
    ctx.save();
    ctx.translate(width / 2, height * 0.34);
    if (shrug) {
      ctx.rotate(0.08);
      ctx.globalAlpha = 0.8;
    } else {
      ctx.rotate(Math.sin(elapsed * 7) * 0.06 * (1 - Math.min(1, elapsed)));
    }
    const scale = (revealState.kind === "alien" ? 2.35 : 2.15) * (0.15 + 0.85 * pop);
    ctx.scale(scale, scale);
    if (revealState.kind === "alien") {
      ctx.rotate(Math.sin(elapsed * 8) * 0.18);
      ctx.translate(0, Math.sin(elapsed * 8) * -1.4);
      paintAlien(ctx, revealState.id);
    } else {
      paintShip(ctx, revealState.id, accent);
    }
    ctx.restore();

    const travel = Math.max(0, revealState.kind === "alien" ? elapsed * 0.85 : elapsed - 0.55);
    for (const spark of revealState.sparks) {
      const distance = spark.speed * travel;
      const drop = shrug ? travel * travel * 36 : 0;
      const x = width / 2 + Math.cos(spark.angle) * distance;
      const y = height * 0.42 + Math.sin(spark.angle) * distance * (shrug ? 0.35 : 1) + drop;
      ctx.globalAlpha = Math.max(0, 1 - travel / (shrug ? 0.8 : 1.35));
      ctx.fillStyle = spark.color;
      ctx.beginPath();
      ctx.arc(x, y, spark.size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }
}

function paintPreview(canvas, painter) {
  const ctx = canvas.getContext("2d");
  const width = 160;
  const height = 72;
  const ratio = window.devicePixelRatio || 1;
  canvas.width = width * ratio;
  canvas.height = height * ratio;
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.clearRect(0, 0, width, height);
  ctx.translate(width / 2, height / 2);
  ctx.scale(1.7, 1.7);
  painter(ctx);
}

function renderCards(container, items, ownedIds, selectedId, paint, onPick, lockedLabel, lockedNote) {
  container.replaceChildren();
  const accent = getComputedStyle(document.body).getPropertyValue("--accent").trim();
  for (const item of items) {
    const owned = ownedIds.includes(item.id);
    const card = document.createElement(owned && onPick ? "button" : "article");
    if (owned && onPick) {
      card.type = "button";
      card.className = `card${item.id === selectedId ? " selected" : ""}`;
      card.addEventListener("click", () => onPick(item.id));
    } else if (!owned) {
      card.className = "locked";
    }
    const canvas = document.createElement("canvas");
    const title = document.createElement("h3");
    const rarity = document.createElement("p");
    const detail = document.createElement("p");
    title.textContent = owned ? item.name : "Unknown";
    rarity.textContent = owned ? item.rarity : lockedLabel;
    detail.textContent = owned ? item.note : lockedNote;
    card.append(canvas, title, rarity, detail);
    container.appendChild(card);
    if (owned) {
      paintPreview(canvas, (ctx) => paint(ctx, item.id, accent));
    }
  }
}

function renderAlienBook() {
  const owned = stats.aliens.length;
  document.querySelector("#alien-count").textContent = owned
    ? `${owned} of ${ALIENS.length} species. Tap one to ride along.`
    : `${owned} of ${ALIENS.length} species`;
  renderCards(
    document.querySelector("#alien-book"),
    ALIENS,
    stats.aliens,
    stats.rider,
    (ctx, id) => paintAlien(ctx, id),
    (id) => {
      stats.rider = stats.rider === id ? "" : id;
      saveJson(STATS_KEY, stats);
      renderAlienBook();
    },
    "Not met yet",
    "Keep exploring.",
  );
}

function renderShop() {
  showDust();
}

function renderHangar() {
  renderCards(
    document.querySelector("#ship-book"),
    SHIPS,
    stats.ships,
    stats.ship,
    paintShip,
    (id) => {
      stats.ship = id;
      saveJson(STATS_KEY, stats);
      renderHangar();
    },
    "Still boxed",
    "Open a mystery box.",
  );
}

function applyTheme(theme) {
  document.body.dataset.theme = theme;
  for (const button of document.querySelectorAll("[data-theme-choice]")) {
    button.classList.toggle("selected", button.dataset.themeChoice === theme);
  }
}

function midi(note) {
  return 440 * 2 ** ((note - 69) / 12);
}

function stopMusic() {
  musicGeneration += 1;
  for (const oscillator of musicHums) {
    oscillator.stop();
  }
  for (const bed of musicBeds) {
    bed.stop();
  }
  musicHums = [];
  musicBeds = [];
  if (musicMaster) {
    musicMaster.disconnect();
    musicMaster = null;
  }
}

function noiseBuffer() {
  if (musicNoise) {
    return musicNoise;
  }
  const length = audioContext.sampleRate * 2;
  const buffer = audioContext.createBuffer(1, length, audioContext.sampleRate);
  const data = buffer.getChannelData(0);
  for (let index = 0; index < length; index += 1) {
    data[index] = Math.random() * 2 - 1;
  }
  musicNoise = buffer;
  return buffer;
}

function playTone(note, time, duration, wave, volume, slide) {
  const oscillator = audioContext.createOscillator();
  const gain = audioContext.createGain();
  const attack = Math.min(0.03, duration * 0.2);
  const release = Math.min(0.22, duration * 0.4);
  oscillator.type = wave;
  oscillator.frequency.setValueAtTime(midi(note), time);
  if (slide) {
    oscillator.frequency.exponentialRampToValueAtTime(Math.max(20, midi(note + slide)), time + duration * 0.8);
  }
  gain.gain.setValueAtTime(0.0001, time);
  gain.gain.exponentialRampToValueAtTime(volume, time + attack);
  gain.gain.setValueAtTime(volume, time + Math.max(attack, duration - release));
  gain.gain.exponentialRampToValueAtTime(0.0001, time + duration);
  oscillator.connect(gain);
  gain.connect(musicMaster);
  oscillator.start(time);
  oscillator.stop(time + duration + 0.05);
}

function playNoise(time, duration, frequency, volume) {
  const source = audioContext.createBufferSource();
  const filter = audioContext.createBiquadFilter();
  const gain = audioContext.createGain();
  source.buffer = noiseBuffer();
  filter.type = "highpass";
  filter.frequency.value = frequency;
  gain.gain.setValueAtTime(0.0001, time);
  gain.gain.exponentialRampToValueAtTime(volume, time + 0.01);
  gain.gain.exponentialRampToValueAtTime(0.0001, time + duration);
  source.connect(filter);
  filter.connect(gain);
  gain.connect(musicMaster);
  source.start(time);
  source.stop(time + duration + 0.02);
}

function scheduleLoop(source, loopSeconds, generation) {
  if (generation !== musicGeneration) {
    return;
  }
  const events = typeof source === "function" ? source() : source;
  const start = audioContext.currentTime + 0.06;
  for (const event of events) {
    if (generation !== musicGeneration) {
      return;
    }
    if (event.noise) {
      playNoise(start + event.time, event.duration, event.frequency, event.volume);
    } else {
      playTone(event.note, start + event.time, event.duration, event.wave, event.volume, event.slide || 0);
    }
  }
  window.setTimeout(() => scheduleLoop(source, loopSeconds, generation), loopSeconds * 1000);
}

function classicalTune() {
  // Erik Satie, Gymnopédie No. 1 (1888). The piece is in the public domain.
  const beat = 0.62;
  const bars = [
    { bass: 43, chord: [59, 62, 66], melody: [78, 76, 74] },
    { bass: 38, chord: [57, 62, 66], melody: [73, 71, 69] },
    { bass: 43, chord: [59, 62, 66], melody: [74, 73, 71] },
    { bass: 38, chord: [57, 61, 66], melody: [69, 67, 66] },
    { bass: 38, chord: [61, 66, 69], melody: [78, 76, 74] },
    { bass: 43, chord: [59, 62, 66], melody: [73, 76, 78] },
    { bass: 38, chord: [57, 62, 66], melody: [81, 78, 76] },
    { bass: 43, chord: [59, 62, 66], melody: [74, 73, 71] },
  ];
  const events = [];
  bars.forEach((bar, index) => {
    const start = index * beat * 3;
    events.push({ note: bar.bass, time: start, duration: beat * 2.7, wave: "triangle", volume: 0.09 });
    for (const note of bar.chord) {
      events.push({ note, time: start + beat, duration: beat * 1.85, wave: "sine", volume: 0.045 });
    }
    bar.melody.forEach((note, step) => {
      events.push({
        note,
        time: start + step * beat,
        duration: beat * 0.92,
        wave: "triangle",
        volume: 0.1,
      });
    });
  });
  return { events, loopSeconds: bars.length * beat * 3 + 0.2 };
}

function spaceTune() {
  // An original chiptune loop: square-wave lead, arpeggio, and a short bass.
  const events = [];
  const bass = [33, 33, 40, 36, 33, 31, 29, 31];
  bass.forEach((note, index) => {
    events.push({ note, time: index * 0.5, duration: 0.28, wave: "square", volume: 0.07 });
  });
  const arp = [57, 60, 64, 67];
  for (let step = 0; step < 16; step += 1) {
    events.push({
      note: arp[step % 4] + (step >= 8 ? 12 : 0),
      time: step * 0.25,
      duration: 0.11,
      wave: "square",
      volume: 0.04,
    });
  }
  const melody = [
    [0, 76], [0.5, 79], [1, 81], [1.5, 84],
    [2.25, 81], [2.75, 79], [3.25, 76], [3.75, 72],
  ];
  for (const [time, note] of melody) {
    events.push({ note, time, duration: 0.32, wave: "square", volume: 0.055 });
  }
  return { events, loopSeconds: 4 };
}

function jazzTune() {
  // An original swing phrase: a short walking bass under a simple melody.
  const events = [];
  const bass = [50, 53, 55, 57, 43, 47, 50, 52, 48, 52, 55, 59, 48, 45, 43, 40];
  bass.forEach((note, index) => {
    events.push({ note, time: index * 0.45, duration: 0.32, wave: "sine", volume: 0.14 });
  });
  const melody = [
    [0, 72], [0.7, 76], [1.35, 74], [1.8, 72],
    [2.25, 71], [2.9, 74], [3.6, 72], [4.2, 69],
    [4.95, 67], [5.6, 69], [6.3, 72], [6.9, 71],
  ];
  for (const [time, note] of melody) {
    events.push({ note, time, duration: 0.34, wave: "triangle", volume: 0.12 });
  }
  return { events, loopSeconds: 7.2 };
}

function lofiTune() {
  const events = [];
  const chords = [
    [50, 57, 60, 65],
    [43, 50, 55, 59],
    [48, 55, 60, 64],
    [45, 52, 57, 60],
  ];
  chords.forEach((chord, index) => {
    const start = index * 2;
    for (const note of chord) {
      events.push({ note, time: start, duration: 1.7, wave: "sine", volume: 0.05 });
      events.push({ note: note + 12, time: start + 0.04, duration: 1.4, wave: "triangle", volume: 0.03 });
    }
    events.push({ note: 36, time: start, duration: 0.16, wave: "sine", volume: 0.16 });
    events.push({ note: 36, time: start + 1.35, duration: 0.1, wave: "sine", volume: 0.08 });
    events.push({ noise: true, time: start + 1, duration: 0.12, frequency: 1800, volume: 0.05 });
  });
  for (let step = 0; step < 16; step += 1) {
    events.push({
      noise: true,
      time: step * 0.5 + 0.26,
      duration: 0.04,
      frequency: 5000,
      volume: step % 2 === 0 ? 0.02 : 0.012,
    });
  }
  const melody = [[0.2, 72], [1.1, 74], [2.15, 76], [3.4, 74], [4.2, 72], [5.5, 69], [6.3, 67], [7.2, 69]];
  for (const [time, note] of melody) {
    events.push({ note, time, duration: 0.55, wave: "triangle", volume: 0.07 });
  }
  return { events, loopSeconds: 8 };
}

function rainDrips() {
  const events = [];
  const drops = 7 + Math.floor(Math.random() * 5);
  for (let index = 0; index < drops; index += 1) {
    events.push({
      note: 84 + Math.floor(Math.random() * 14),
      time: Math.random() * 3.7,
      duration: 0.04 + Math.random() * 0.07,
      wave: "sine",
      volume: 0.025 + Math.random() * 0.04,
    });
  }
  return events;
}

function startRainBed() {
  const source = audioContext.createBufferSource();
  const low = audioContext.createBiquadFilter();
  const gain = audioContext.createGain();
  source.buffer = noiseBuffer();
  source.loop = true;
  low.type = "lowpass";
  low.frequency.value = 780;
  gain.gain.value = 0.2;
  source.connect(low);
  low.connect(gain);
  gain.connect(musicMaster);
  source.start();
  musicBeds.push(source);

  const hiss = audioContext.createBufferSource();
  const high = audioContext.createBiquadFilter();
  const hissGain = audioContext.createGain();
  hiss.buffer = noiseBuffer();
  hiss.loop = true;
  high.type = "highpass";
  high.frequency.value = 2400;
  hissGain.gain.value = 0.035;
  hiss.connect(high);
  high.connect(hissGain);
  hissGain.connect(musicMaster);
  hiss.start();
  musicBeds.push(hiss);
}

function bossaTune() {
  const events = [];
  const pattern = [
    { bass: 38, chord: [50, 57, 62], time: 0 },
    { bass: 45, chord: [52, 57, 64], time: 2 },
    { bass: 43, chord: [50, 55, 62], time: 4 },
    { bass: 41, chord: [48, 53, 60], time: 6 },
  ];
  for (const bar of pattern) {
    events.push({ note: bar.bass, time: bar.time, duration: 0.28, wave: "sine", volume: 0.12 });
    events.push({ note: bar.bass + 12, time: bar.time + 0.75, duration: 0.18, wave: "sine", volume: 0.07 });
    events.push({ note: bar.bass, time: bar.time + 1.25, duration: 0.22, wave: "sine", volume: 0.09 });
    for (const note of bar.chord) {
      events.push({ note, time: bar.time + 0.35, duration: 0.28, wave: "triangle", volume: 0.045 });
      events.push({ note, time: bar.time + 1.05, duration: 0.22, wave: "triangle", volume: 0.035 });
    }
  }
  const melody = [[0.4, 69], [1.3, 74], [2.4, 72], [3.5, 69], [4.4, 67], [5.6, 69], [6.5, 65], [7.3, 62]];
  for (const [time, note] of melody) {
    events.push({ note, time, duration: 0.42, wave: "triangle", volume: 0.08 });
  }
  return { events, loopSeconds: 8 };
}

function trapTune() {
  // Original half-time beat: sliding 808s, hat rolls, and a short minor loop.
  const step = 0.1;
  const events = [];
  const kicks = [0, 6, 10, 16, 22, 26, 32, 38, 42, 48, 54, 58];
  const bass = [29, 24, 32, 29, 27, 24, 29, 36, 32, 29, 27, 24];
  kicks.forEach((hit, index) => {
    events.push({
      note: bass[index],
      time: hit * step,
      duration: hit % 16 === 0 ? 0.55 : 0.28,
      wave: "sine",
      volume: 0.2,
      slide: hit % 16 === 0 ? -2 : -7,
    });
    events.push({
      note: bass[index] + 12,
      time: hit * step,
      duration: 0.06,
      wave: "triangle",
      volume: 0.05,
    });
  });
  for (const snare of [8, 24, 40, 56]) {
    events.push({ noise: true, time: snare * step, duration: 0.09, frequency: 1400, volume: 0.09 });
    events.push({ noise: true, time: snare * step + 0.012, duration: 0.05, frequency: 3200, volume: 0.04 });
  }
  for (let hit = 0; hit < 64; hit += 1) {
    const roll = hit % 16 >= 13;
    events.push({
      noise: true,
      time: hit * step,
      duration: roll ? 0.03 : 0.025,
      frequency: hit % 2 === 0 ? 7200 : 5400,
      volume: roll ? 0.045 : hit % 2 === 0 ? 0.028 : 0.014,
    });
    if (roll) {
      events.push({
        noise: true,
        time: hit * step + step * 0.5,
        duration: 0.02,
        frequency: 8000,
        volume: 0.03,
      });
    }
  }
  const melody = [
    [0, 75], [0.2, 72], [0.4, 68], [0.8, 72], [1.2, 75], [1.4, 77],
    [2.0, 72], [2.2, 68], [2.6, 65], [3.0, 68], [3.4, 72],
    [4.0, 75], [4.2, 72], [4.6, 68], [5.0, 72], [5.4, 75], [5.8, 77],
  ];
  for (const [time, note] of melody) {
    events.push({ note, time, duration: 0.18, wave: "square", volume: 0.045 });
    events.push({ note: note + 12, time: time + 0.012, duration: 0.12, wave: "triangle", volume: 0.03 });
  }
  return { events, loopSeconds: 6.4 };
}

function oceanTune() {
  // Original slow R&B loop: soft electric-piano chords, a quiet pocket, and a short airy line.
  const events = [];
  const bars = [
    { bass: 46, chord: [58, 62, 65, 69], time: 0 },
    { bass: 43, chord: [55, 58, 62, 65], time: 2 },
    { bass: 51, chord: [58, 63, 67, 70], time: 4 },
    { bass: 41, chord: [53, 57, 60, 65], time: 6 },
  ];
  for (const bar of bars) {
    events.push({ note: bar.bass, time: bar.time, duration: 1.6, wave: "sine", volume: 0.11 });
    events.push({ note: bar.bass, time: bar.time + 1.25, duration: 0.4, wave: "sine", volume: 0.06 });
    for (const note of bar.chord) {
      events.push({ note, time: bar.time + 0.03, duration: 1.85, wave: "sine", volume: 0.04 });
      events.push({ note: note + 12, time: bar.time + 0.08, duration: 1.5, wave: "triangle", volume: 0.018 });
    }
    events.push({ noise: true, time: bar.time + 1, duration: 0.08, frequency: 1600, volume: 0.035 });
  }
  for (let step = 0; step < 16; step += 1) {
    events.push({
      noise: true,
      time: step * 0.5,
      duration: 0.03,
      frequency: 6200,
      volume: step % 2 === 0 ? 0.012 : 0.007,
    });
  }
  const melody = [
    [0.35, 77], [1.15, 74], [1.9, 72], [2.7, 74],
    [3.55, 70], [4.45, 72], [5.3, 77], [6.15, 74], [7.05, 72],
  ];
  for (const [time, note] of melody) {
    events.push({ note, time, duration: 0.7, wave: "triangle", volume: 0.07 });
    events.push({ note: note + 12, time: time + 0.02, duration: 0.45, wave: "sine", volume: 0.025 });
  }
  return { events, loopSeconds: 8 };
}

function nightTune() {
  const events = [];
  const chords = [
    [48, 55, 60, 63],
    [46, 53, 58, 62],
  ];
  chords.forEach((chord, index) => {
    for (const note of chord) {
      events.push({ note, time: index * 5, duration: 5.4, wave: "sine", volume: 0.05 });
      events.push({ note: note + 12, time: index * 5 + 0.4, duration: 4.6, wave: "sine", volume: 0.02 });
    }
  });
  return { events, loopSeconds: 10 };
}

function startMusic(kind) {
  stopMusic();
  for (const button of document.querySelectorAll("[data-music-choice]")) {
    button.classList.toggle("selected", button.dataset.musicChoice === kind);
  }
  if (kind === "off") {
    return;
  }
  if (!audioContext) {
    audioContext = new AudioContext();
  }
  audioContext.resume();

  musicMaster = audioContext.createGain();
  musicMaster.connect(audioContext.destination);

  const tunes = {
    jazz: jazzTune,
    classical: classicalTune,
    space: spaceTune,
    lofi: lofiTune,
    bossa: bossaTune,
    night: nightTune,
    trap: trapTune,
    ocean: oceanTune,
  };
  if (kind === "rain") {
    musicMaster.gain.value = 0.9;
    startRainBed();
    scheduleLoop(rainDrips, 4, musicGeneration);
    return;
  }
  if (tunes[kind]) {
    musicMaster.gain.value = kind === "space" || kind === "trap" ? 0.8 : 0.85;
    const tune = tunes[kind]();
    scheduleLoop(tune.events, tune.loopSeconds, musicGeneration);
    return;
  }

  musicMaster.gain.value = kind === "soft" ? 0.08 : 0.12;
  const notes = kind === "soft" ? [55, 59, 62] : [64, 68, 71];
  for (const note of notes) {
    const oscillator = audioContext.createOscillator();
    oscillator.type = kind === "soft" ? "sine" : "triangle";
    oscillator.frequency.value = midi(note);
    oscillator.connect(musicMaster);
    oscillator.start();
    musicHums.push(oscillator);
  }
}

const DAILY_BANKS = [
  {
    id: "events",
    prompt: "Put these events in order, earliest first. 5 space dust for each correct spot.",
    items: [
      { id: "olympics", label: "First ancient Olympic Games", value: -776 },
      { id: "magna", label: "Magna Carta is sealed", value: 1215 },
      { id: "press", label: "Gutenberg's printing press", value: 1440 },
      { id: "columbus", label: "Columbus reaches the Americas", value: 1492 },
      { id: "independence", label: "United States Declaration of Independence", value: 1776 },
      { id: "revolution", label: "French Revolution begins", value: 1789 },
      { id: "civil", label: "American Civil War begins", value: 1861 },
      { id: "flight", label: "Wright brothers' first flight", value: 1903 },
      { id: "titanic", label: "Titanic sinks", value: 1912 },
      { id: "vote", label: "U.S. women win the vote", value: 1920 },
      { id: "ww2", label: "World War II begins in Europe", value: 1939 },
      { id: "sputnik", label: "Sputnik orbits Earth", value: 1957 },
      { id: "moon", label: "Apollo 11 lands on the Moon", value: 1969 },
      { id: "wall", label: "Berlin Wall falls", value: 1989 },
      { id: "web", label: "The World Wide Web is opened to the public", value: 1991 },
      { id: "phones", label: "Apple announces the iPhone", value: 2007 },
    ],
  },
  {
    id: "ages",
    prompt: "Put these people in order, youngest first. 5 space dust for each correct spot.",
    items: [
      { id: "confucius", label: "Confucius", value: -551 },
      { id: "cleopatra", label: "Cleopatra", value: -69 },
      { id: "joan", label: "Joan of Arc", value: 1412 },
      { id: "leonardo", label: "Leonardo da Vinci", value: 1452 },
      { id: "shakespeare", label: "William Shakespeare", value: 1564 },
      { id: "newton", label: "Isaac Newton", value: 1643 },
      { id: "mozart", label: "Wolfgang Amadeus Mozart", value: 1756 },
      { id: "austen", label: "Jane Austen", value: 1775 },
      { id: "lincoln", label: "Abraham Lincoln", value: 1809 },
      { id: "lovelace", label: "Ada Lovelace", value: 1815 },
      { id: "curie", label: "Marie Curie", value: 1867 },
      { id: "gandhi", label: "Mahatma Gandhi", value: 1869 },
      { id: "einstein", label: "Albert Einstein", value: 1879 },
      { id: "picasso", label: "Pablo Picasso", value: 1881 },
      { id: "earhart", label: "Amelia Earhart", value: 1897 },
      { id: "kahlo", label: "Frida Kahlo", value: 1907 },
      { id: "parks", label: "Rosa Parks", value: 1913 },
      { id: "elizabeth", label: "Queen Elizabeth II", value: 1926 },
      { id: "king", label: "Martin Luther King Jr.", value: 1929 },
      { id: "armstrong", label: "Neil Armstrong", value: 1930 },
      { id: "gagarin", label: "Yuri Gagarin", value: 1934 },
      { id: "ali", label: "Muhammad Ali", value: 1942 },
      { id: "mercury", label: "Freddie Mercury", value: 1946 },
      { id: "oprah", label: "Oprah Winfrey", value: 1954 },
      { id: "jackson", label: "Michael Jackson", value: 1958 },
      { id: "obama", label: "Barack Obama", value: 1961 },
      { id: "serena", label: "Serena Williams", value: 1981 },
      { id: "bolt", label: "Usain Bolt", value: 1986 },
      { id: "swift", label: "Taylor Swift", value: 1989 },
      { id: "malala", label: "Malala Yousafzai", value: 1997 },
      { id: "greta", label: "Greta Thunberg", value: 2003 },
    ],
  },
  {
    id: "prices",
    prompt: "Put these in order, cheapest first. 5 space dust for each correct spot.",
    items: [
      { id: "comic", label: "Action Comics #1, cover price, 1938", value: 0.1 },
      { id: "burger", label: "A McDonald's hamburger, 1948", value: 0.15 },
      { id: "disney", label: "Disneyland adult admission, 1955", value: 1 },
      { id: "woodstock", label: "A Woodstock advance ticket, 1969", value: 18 },
      { id: "iphone", label: "The first iPhone, 4GB, 2007", value: 499 },
      { id: "modelt", label: "A Ford Model T, 1908", value: 850 },
      { id: "apple2", label: "An Apple II computer, 1977", value: 1298 },
      { id: "mac", label: "The original Macintosh, 1984", value: 2495 },
      { id: "dynatac", label: "A Motorola DynaTAC phone, 1983", value: 3995 },
      { id: "alaska", label: "The Alaska Purchase, 1867", value: 7200000 },
      { id: "louisiana", label: "The Louisiana Purchase, 1803", value: 15000000 },
    ],
  },
];

let dailyPlay = null;

function hashString(text) {
  let hash = 2166136261;
  for (const char of text) {
    hash ^= char.charCodeAt(0);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function mulberry32(seed) {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6D2B79F5) >>> 0;
    let value = state;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffleWith(items, random) {
  const copy = items.slice();
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swap = Math.floor(random() * (index + 1));
    [copy[index], copy[swap]] = [copy[swap], copy[index]];
  }
  return copy;
}

function dailyDate() {
  const now = new Date();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${now.getFullYear()}-${month}-${day}`;
}

function dailyBank(id) {
  return DAILY_BANKS.find((bank) => bank.id === id);
}

function dailyAnswer(bank, items) {
  const copy = items.slice();
  copy.sort((left, right) => (bank.id === "ages" ? right.value - left.value : left.value - right.value));
  return copy;
}

function dailyFact(bank, item) {
  if (bank.id === "prices") {
    if (item.value < 1) {
      return `${Math.round(item.value * 100)}¢`;
    }
    return `$${item.value.toLocaleString("en-US")}`;
  }
  if (item.value < 0) {
    return bank.id === "ages" ? `Born ${Math.abs(item.value)} BCE` : `${Math.abs(item.value)} BCE`;
  }
  return bank.id === "ages" ? `Born ${item.value}` : String(item.value);
}

function buildDaily(date) {
  const random = mulberry32(hashString(`trivianaut-daily-${date}`));
  const bank = DAILY_BANKS[Math.floor(random() * DAILY_BANKS.length)];
  const chosen = shuffleWith(bank.items, random).slice(0, 5);
  const answer = dailyAnswer(bank, chosen);
  let order = shuffleWith(chosen, random);
  if (order.every((item, index) => item.id === answer[index].id)) {
    [order[0], order[1]] = [order[1], order[0]];
  }
  return { date, bank, answer, order, done: false, earned: 0 };
}

function renderDaily() {
  const bank = dailyPlay.bank;
  const when = new Date(`${dailyPlay.date}T12:00:00`);
  document.querySelector("#daily-date").textContent = when.toLocaleDateString(undefined, {
    month: "long",
    day: "numeric",
  });
  document.querySelector("#daily-prompt").textContent = bank.prompt;
  const list = document.querySelector("#daily-rank");
  list.replaceChildren();
  dailyPlay.order.forEach((item, index) => {
    const row = document.createElement("li");
    const spot = document.createElement("span");
    const label = document.createElement("span");
    const name = document.createElement("span");
    spot.className = "spot";
    spot.textContent = String(index + 1);
    name.textContent = item.label;
    label.append(name);
    if (dailyPlay.done) {
      const fact = document.createElement("span");
      fact.className = "fact";
      fact.textContent = dailyFact(bank, item);
      label.append(fact);
      row.classList.add(item.id === dailyPlay.answer[index].id ? "correct" : "wrong");
    }
    row.append(spot, label);
    if (!dailyPlay.done) {
      const moves = document.createElement("span");
      moves.className = "moves";
      for (const direction of [-1, 1]) {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = direction < 0 ? "↑" : "↓";
        button.setAttribute("aria-label", direction < 0 ? `Move ${item.label} up` : `Move ${item.label} down`);
        button.disabled = direction < 0 ? index === 0 : index === dailyPlay.order.length - 1;
        button.addEventListener("click", () => moveDaily(index, direction));
        moves.append(button);
      }
      row.append(moves);
    }
    list.appendChild(row);
  });
  const note = document.querySelector("#daily-note");
  const submit = document.querySelector("#daily-submit");
  note.classList.toggle("hidden", !dailyPlay.done);
  submit.hidden = dailyPlay.done;
  if (dailyPlay.done) {
    const correct = dailyPlay.order.filter((item, index) => item.id === dailyPlay.answer[index].id).length;
    const spots = correct === 1 ? "spot" : "spots";
    if (correct === 0) {
      note.textContent = "None in the right spot. +0 space dust.";
    } else if (correct === dailyPlay.order.length) {
      note.textContent = `Perfect order. +${dailyPlay.earned} space dust.`;
    } else {
      note.textContent = `${correct} in the right ${spots}. +${dailyPlay.earned} space dust.`;
    }
  }
}

function moveDaily(index, direction) {
  const next = index + direction;
  if (dailyPlay.done || next < 0 || next >= dailyPlay.order.length) {
    return;
  }
  const order = dailyPlay.order;
  [order[index], order[next]] = [order[next], order[index]];
  renderDaily();
}

function openDaily() {
  const date = dailyDate();
  const saved = readDaily();
  dailyPlay = buildDaily(date);
  if (saved && saved.date === date && saved.done) {
    const byId = new Map(dailyPlay.answer.map((item) => [item.id, item]));
    dailyPlay.order = saved.order.map((id) => byId.get(id));
    dailyPlay.done = true;
    dailyPlay.earned = saved.earned;
  }
  renderDaily();
  show("daily");
}

function submitDaily() {
  if (!dailyPlay || dailyPlay.done) {
    return;
  }
  const correct = dailyPlay.order.filter((item, index) => item.id === dailyPlay.answer[index].id).length;
  dailyPlay.done = true;
  dailyPlay.earned = correct * DAILY_DUST;
  stats.dust += dailyPlay.earned;
  saveJson(STATS_KEY, stats);
  saveJson(DAILY_KEY, {
    date: dailyPlay.date,
    done: true,
    earned: dailyPlay.earned,
    order: dailyPlay.order.map((item) => item.id),
  });
  renderDaily();
  showDust();
}

function openTrivia() {
  if (questions.length === 0) {
    return;
  }
  sessionCorrect = 0;
  stats.sessions += 1;
  saveJson(STATS_KEY, stats);
  show("trivia");
  showQuestion();
}

function goHome() {
  stats.bestSession = Math.max(stats.bestSession, sessionCorrect);
  saveJson(STATS_KEY, stats);
  showDust();
  show("home");
}

document.querySelector("#open-stats").addEventListener("click", () => {
  renderStats();
  show("stats");
});
document.querySelector("#open-trivia").addEventListener("click", openTrivia);
document.querySelector("#open-daily").addEventListener("click", openDaily);
document.querySelector("#daily-home").addEventListener("click", () => {
  showDust();
  show("home");
});
document.querySelector("#daily-submit").addEventListener("click", submitDaily);
document.querySelector("#open-shop").addEventListener("click", () => {
  document.querySelector("#shop-note").classList.add("hidden");
  renderShop();
  show("shop");
});
document.querySelector("#open-hangar").addEventListener("click", () => {
  renderHangar();
  show("hangar");
});
document.querySelector("#open-species").addEventListener("click", () => {
  renderAlienBook();
  show("species");
});
document.querySelector("#open-settings").addEventListener("click", () => show("settings"));
document.querySelector("#buy-box").addEventListener("click", buyMysteryBox);
document.querySelector("#reveal-close").addEventListener("click", closeReveal);
document.querySelector("#trivia-home").addEventListener("click", goHome);
document.querySelector("#stats-home").addEventListener("click", goHome);
document.querySelector("#shop-home").addEventListener("click", goHome);
document.querySelector("#hangar-home").addEventListener("click", goHome);
document.querySelector("#species-home").addEventListener("click", goHome);
document.querySelector("#settings-home").addEventListener("click", () => show("home"));
document.querySelector("#next-question").addEventListener("click", showQuestion);

for (const button of document.querySelectorAll("[data-theme-choice]")) {
  button.addEventListener("click", () => {
    settings.theme = button.dataset.themeChoice;
    saveJson(SETTINGS_KEY, settings);
    applyTheme(settings.theme);
  });
}

const musicBox = document.querySelector("#music-choices");
const musicOptions = [
  ["off", "Off"],
  ["soft", "Soft hum"],
  ["bright", "Bright hum"],
  ["jazz", "Jazz"],
  ["space", "Retro space"],
  ["classical", "Classical"],
  ["lofi", "Lofi"],
  ["rain", "Rain"],
  ["bossa", "Bossa"],
  ["night", "Night"],
  ["trap", "Trap"],
  ["ocean", "Ocean"],
];
if (musicBox) {
  for (const [id, label] of musicOptions) {
    if (musicBox.querySelector(`[data-music-choice="${id}"]`)) {
      continue;
    }
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.musicChoice = id;
    button.textContent = label;
    musicBox.append(button);
  }
}

for (const button of document.querySelectorAll("[data-music-choice]")) {
  button.addEventListener("click", () => {
    settings.music = button.dataset.musicChoice;
    saveJson(SETTINGS_KEY, settings);
    startMusic(settings.music);
  });
}

function refreshMusicChoice() {
  for (const button of document.querySelectorAll("[data-music-choice]")) {
    button.classList.toggle("selected", button.dataset.musicChoice === settings.music);
  }
}

applyTheme(settings.theme);
showDust();
startMusic("off");
refreshMusicChoice();

const flightCanvas = document.querySelector("#flight");
const flightCtx = flightCanvas.getContext("2d");
const insetProbe = document.createElement("div");
insetProbe.style.cssText = "position:fixed;visibility:hidden;pointer-events:none;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)";
document.body.append(insetProbe);

function safeInsets() {
  const style = getComputedStyle(insetProbe);
  return {
    top: parseFloat(style.paddingTop) || 0,
    right: parseFloat(style.paddingRight) || 0,
  };
}
let flightSpeed = Number(localStorage.getItem(FLIGHT_KEY));
if (!Number.isFinite(flightSpeed) || flightSpeed <= 0) {
  flightSpeed = 1;
}

function changeFlightSpeed(correct) {
  if (correct) {
    flightSpeed = Math.min(8, flightSpeed + 0.5);
  } else {
    flightSpeed = 1;
  }
  try {
    localStorage.setItem(FLIGHT_KEY, String(flightSpeed));
  } catch {
    // IndexedDB keeps the speed if localStorage is full.
  }
  const speedRecord = { value: flightSpeed, savedAt: Date.now() };
  idbSet(FLIGHT_KEY, speedRecord).catch(() => {});
  cacheSave(FLIGHT_KEY, speedRecord).catch(() => {});
}

restoreSaves();

function makeComet(anywhere) {
  const width = flightCanvas.clientWidth || window.innerWidth;
  const height = flightCanvas.clientHeight || window.innerHeight;
  return {
    x: anywhere ? Math.random() * width : width + 30,
    y: 20 + Math.random() * Math.max(40, height - 40),
    size: 1.4 + Math.random() * 2.4,
    drift: 36 + Math.random() * 70,
  };
}

const comets = Array.from({ length: 18 }, () => makeComet(true));
const ufos = [];
const guests = [];
let nextUfoAt = performance.now() + 6000;
let activeCheckpoint = null;
let flightClock = 0;
let flightLast = performance.now();
let riderCheer = 0;

function launchUfoVisit(width, height) {
  const fromLeft = Math.random() < 0.5;
  const direction = fromLeft ? 1 : -1;
  for (let index = 0; index < 2; index += 1) {
    ufos.push({
      x: (fromLeft ? -110 : width + 110) - direction * index * 120,
      y: Math.max(120, height * 0.22) + Math.random() * Math.max(50, height * 0.36),
      speed: direction * (62 + Math.random() * 28),
      wobble: Math.random() * Math.PI * 2,
    });
  }
}

function drawUfo(ufo) {
  const bob = Math.sin(flightClock * 2.4 + ufo.wobble) * 5;
  const x = ufo.x;
  const y = ufo.y + bob;
  flightCtx.save();
  flightCtx.fillStyle = "#c5d0de";
  flightCtx.beginPath();
  flightCtx.ellipse(x, y + 8, 30, 10, 0, 0, Math.PI * 2);
  flightCtx.fill();
  flightCtx.fillStyle = "#8ea0b8";
  flightCtx.beginPath();
  flightCtx.ellipse(x, y + 11, 18, 5, 0, 0, Math.PI);
  flightCtx.fill();
  flightCtx.fillStyle = "rgba(186, 230, 255, 0.62)";
  flightCtx.beginPath();
  flightCtx.arc(x, y + 2, 13, Math.PI, 0);
  flightCtx.fill();
  flightCtx.fillStyle = "#73c45d";
  flightCtx.beginPath();
  flightCtx.arc(x, y - 2, 6, 0, Math.PI * 2);
  flightCtx.fill();
  flightCtx.fillRect(x - 4, y + 2, 8, 6);
  flightCtx.strokeStyle = "#73c45d";
  flightCtx.lineWidth = 1.5;
  flightCtx.beginPath();
  flightCtx.moveTo(x - 3, y - 7);
  flightCtx.lineTo(x - 5, y - 12);
  flightCtx.moveTo(x + 3, y - 7);
  flightCtx.lineTo(x + 5, y - 12);
  flightCtx.stroke();
  flightCtx.fillStyle = "#162016";
  flightCtx.beginPath();
  flightCtx.arc(x - 2.2, y - 3, 1.2, 0, Math.PI * 2);
  flightCtx.arc(x + 2.2, y - 3, 1.2, 0, Math.PI * 2);
  flightCtx.fill();
  const blink = 0.45 + Math.sin(flightClock * 6 + ufo.wobble) * 0.55;
  flightCtx.globalAlpha = blink;
  flightCtx.fillStyle = "#f6d36b";
  for (const dx of [-16, 0, 16]) {
    flightCtx.beginPath();
    flightCtx.arc(x + dx, y + 10, 1.8, 0, Math.PI * 2);
    flightCtx.fill();
  }
  flightCtx.restore();
}

function noteCheckpoint(streak) {
  if (streak < 1) {
    activeCheckpoint = null;
    return;
  }
  const level = Math.min(streak, CHECKPOINTS.length);
  stats.furthestCheckpoint = Math.max(stats.furthestCheckpoint || 0, level);
  activeCheckpoint = {
    name: CHECKPOINTS[level - 1],
    x: (flightCanvas.clientWidth || window.innerWidth) + 80,
    y: Math.max(160, (flightCanvas.clientHeight || window.innerHeight) * 0.22),
  };
}

function clearCheckpoint() {
  activeCheckpoint = null;
}

function fillCircle(x, y, radius, color) {
  flightCtx.fillStyle = color;
  flightCtx.beginPath();
  flightCtx.arc(x, y, radius, 0, Math.PI * 2);
  flightCtx.fill();
}

function drawCheckpointGraphic(name, x, y, scale) {
  flightCtx.save();
  flightCtx.translate(x, y);
  flightCtx.scale(scale, scale);
  flightCtx.translate(-x, -y);
  if (name === "Mars") {
    fillCircle(x, y, 14, "#c4553a");
    fillCircle(x - 4, y + 2, 3, "#a3432d");
  } else if (name === "Saturn") {
    fillCircle(x, y, 12, "#e6c98a");
    flightCtx.strokeStyle = "#f0ddb0";
    flightCtx.lineWidth = 2;
    flightCtx.beginPath();
    flightCtx.ellipse(x, y, 22, 7, -0.4, 0, Math.PI * 2);
    flightCtx.stroke();
  } else if (name === "Pluto") {
    fillCircle(x, y, 8, "#c8c2b4");
    fillCircle(x + 14, y - 6, 3, "#eeeae2");
  } else if (name === "Moon") {
    fillCircle(x, y, 13, "#f4efe4");
    fillCircle(x - 4, y - 2, 3, "#d5ccbe");
  } else if (name === "Jupiter") {
    fillCircle(x, y, 16, "#d7a15a");
    flightCtx.strokeStyle = "#f0d2a0";
    flightCtx.lineWidth = 2;
    flightCtx.beginPath();
    flightCtx.moveTo(x - 12, y - 3);
    flightCtx.lineTo(x + 12, y - 3);
    flightCtx.moveTo(x - 14, y + 4);
    flightCtx.lineTo(x + 13, y + 4);
    flightCtx.stroke();
  } else if (name === "Venus") {
    fillCircle(x, y, 13, "#f0d58a");
  } else if (name === "Mercury") {
    fillCircle(x, y, 9, "#b7b1a8");
    fillCircle(x + 2, y - 2, 2, "#8e8982");
  } else if (name === "Neptune") {
    fillCircle(x, y, 13, "#3d6fbf");
  } else if (name === "Uranus") {
    fillCircle(x, y, 12, "#b7e0e4");
  } else if (name === "Sun") {
    flightCtx.strokeStyle = "#f6d36b";
    flightCtx.lineWidth = 2;
    for (let ray = 0; ray < 8; ray += 1) {
      const angle = (ray / 8) * Math.PI * 2;
      flightCtx.beginPath();
      flightCtx.moveTo(x + Math.cos(angle) * 12, y + Math.sin(angle) * 12);
      flightCtx.lineTo(x + Math.cos(angle) * 20, y + Math.sin(angle) * 20);
      flightCtx.stroke();
    }
    fillCircle(x, y, 10, "#ffe08a");
  } else if (name === "Asteroid") {
    flightCtx.fillStyle = "#9a8f84";
    flightCtx.beginPath();
    flightCtx.moveTo(x - 12, y);
    flightCtx.lineTo(x - 4, y - 8);
    flightCtx.lineTo(x + 10, y - 3);
    flightCtx.lineTo(x + 6, y + 8);
    flightCtx.lineTo(x - 8, y + 6);
    flightCtx.closePath();
    flightCtx.fill();
  } else if (name === "Comet") {
    flightCtx.strokeStyle = "#f4efe4";
    flightCtx.lineWidth = 2;
    flightCtx.beginPath();
    flightCtx.moveTo(x, y);
    flightCtx.lineTo(x + 28, y + 4);
    flightCtx.stroke();
    fillCircle(x, y, 5, "#fffaf0");
  } else if (name === "Eclipse") {
    fillCircle(x, y, 12, "#f6d36b");
    fillCircle(x + 5, y, 11, "#1b1916");
  } else if (name === "Nebula") {
    flightCtx.globalAlpha = 0.45;
    fillCircle(x - 6, y, 12, "#c47ad4");
    fillCircle(x + 8, y - 2, 10, "#6aa8e8");
    fillCircle(x, y + 4, 8, "#f0a0c0");
    flightCtx.globalAlpha = 1;
  } else if (name === "Supernova") {
    flightCtx.strokeStyle = "#fff4c2";
    flightCtx.lineWidth = 2;
    flightCtx.beginPath();
    flightCtx.moveTo(x - 16, y);
    flightCtx.lineTo(x + 16, y);
    flightCtx.moveTo(x, y - 16);
    flightCtx.lineTo(x, y + 16);
    flightCtx.moveTo(x - 11, y - 11);
    flightCtx.lineTo(x + 11, y + 11);
    flightCtx.stroke();
    fillCircle(x, y, 4, "#fffaf0");
  } else if (name === "Black hole") {
    flightCtx.strokeStyle = "#f0b45a";
    flightCtx.lineWidth = 3;
    flightCtx.beginPath();
    flightCtx.ellipse(x, y, 18, 6, 0.5, 0, Math.PI * 2);
    flightCtx.stroke();
    fillCircle(x, y, 7, "#120f0e");
  } else if (name === "Galaxy") {
    flightCtx.strokeStyle = "#d7c6ef";
    flightCtx.lineWidth = 2;
    flightCtx.beginPath();
    flightCtx.ellipse(x, y, 18, 7, 0.6, 0, Math.PI * 2);
    flightCtx.stroke();
    fillCircle(x, y, 3, "#fffaf0");
  } else if (name === "Pulsar") {
    fillCircle(x, y, 4, "#fffaf0");
    flightCtx.strokeStyle = "#9fd0ff";
    flightCtx.lineWidth = 2;
    flightCtx.beginPath();
    flightCtx.moveTo(x - 20, y - 6);
    flightCtx.lineTo(x + 20, y + 6);
    flightCtx.moveTo(x - 20, y + 6);
    flightCtx.lineTo(x + 20, y - 6);
    flightCtx.stroke();
  } else if (name === "Constellation") {
    const stars = [[0, 0], [16, -8], [30, 2], [46, -4], [40, 14], [22, 16]];
    flightCtx.strokeStyle = "#f7f1e4";
    flightCtx.lineWidth = 1;
    flightCtx.beginPath();
    stars.forEach(([dx, dy], index) => {
      if (index === 0) {
        flightCtx.moveTo(x + dx, y + dy);
      } else {
        flightCtx.lineTo(x + dx, y + dy);
      }
    });
    flightCtx.stroke();
    for (const [dx, dy] of stars) {
      fillCircle(x + dx, y + dy, 2, "#fffaf0");
    }
  } else if (name === "Quasar") {
    fillCircle(x, y, 5, "#fff6d0");
    flightCtx.strokeStyle = "#8fd0ff";
    flightCtx.lineWidth = 2;
    flightCtx.beginPath();
    flightCtx.moveTo(x, y - 18);
    flightCtx.lineTo(x, y + 18);
    flightCtx.stroke();
  }
  flightCtx.restore();
}

function paintShip(ctx, id, color) {
  ctx.save();
  ctx.fillStyle = color;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  if (id === "saucer") {
    ctx.beginPath();
    ctx.ellipse(0, 4, 18, 7, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 0.55;
    ctx.beginPath();
    ctx.arc(0, 0, 8, Math.PI, 0);
    ctx.fill();
  } else if (id === "pencil") {
    ctx.fillRect(-16, -4, 26, 8);
    ctx.beginPath();
    ctx.moveTo(10, -4);
    ctx.lineTo(20, 0);
    ctx.lineTo(10, 4);
    ctx.fill();
    ctx.fillStyle = "#f4efe4";
    ctx.fillRect(-18, -4, 4, 8);
  } else if (id === "teapot") {
    ctx.beginPath();
    ctx.arc(-2, 2, 9, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(6, 0);
    ctx.quadraticCurveTo(16, -2, 14, 6);
    ctx.lineTo(8, 4);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(-12, 2, 5, Math.PI * 0.6, Math.PI * 1.5);
    ctx.stroke();
    ctx.fillRect(-6, -10, 8, 3);
  } else if (id === "fish") {
    ctx.beginPath();
    ctx.ellipse(2, 0, 14, 7, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(-12, 0);
    ctx.lineTo(-20, -7);
    ctx.lineTo(-20, 7);
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(8, -1, 1.4, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "boot") {
    ctx.beginPath();
    ctx.moveTo(-8, -12);
    ctx.lineTo(2, -12);
    ctx.lineTo(2, 2);
    ctx.lineTo(14, 2);
    ctx.lineTo(14, 8);
    ctx.lineTo(-8, 8);
    ctx.closePath();
    ctx.fill();
  } else if (id === "crown") {
    ctx.beginPath();
    ctx.moveTo(16, 2);
    ctx.lineTo(-8, -5);
    ctx.lineTo(-4, 0);
    ctx.lineTo(-14, 5);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(-6, -8);
    ctx.lineTo(-2, -14);
    ctx.lineTo(2, -8);
    ctx.lineTo(6, -14);
    ctx.lineTo(10, -8);
    ctx.lineTo(-6, -8);
    ctx.fill();
  } else if (id === "potato") {
    ctx.beginPath();
    ctx.ellipse(0, 1, 15, 9, 0.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#9fd0ff";
    ctx.beginPath();
    ctx.arc(4, 0, 3, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#7dce6a";
    ctx.beginPath();
    ctx.moveTo(-4, -8);
    ctx.lineTo(-6, -14);
    ctx.stroke();
  } else if (id === "plane") {
    ctx.beginPath();
    ctx.moveTo(16, 0);
    ctx.lineTo(-14, -8);
    ctx.lineTo(-6, 0);
    ctx.lineTo(-14, 8);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(-2, 0);
    ctx.lineTo(4, 9);
    ctx.lineTo(2, 0);
    ctx.fill();
  } else if (id === "thimble") {
    ctx.beginPath();
    ctx.moveTo(-8, 8);
    ctx.lineTo(8, 8);
    ctx.lineTo(6, -4);
    ctx.quadraticCurveTo(0, -14, -6, -4);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    for (const y of [-2, 2, 6]) {
      ctx.fillRect(-5, y, 10, 1);
    }
  } else if (id === "accordion") {
    ctx.fillRect(-16, -6, 32, 12);
    ctx.fillStyle = "#1b1916";
    for (const x of [-10, -4, 2, 8]) {
      ctx.fillRect(x, -6, 2, 12);
    }
  } else if (id === "porch") {
    ctx.fillRect(-7, -2, 14, 12);
    ctx.beginPath();
    ctx.moveTo(-9, -2);
    ctx.lineTo(0, -12);
    ctx.lineTo(9, -2);
    ctx.fill();
    ctx.fillStyle = "#fff6d0";
    ctx.fillRect(-3, 2, 6, 6);
  } else if (id === "sub") {
    ctx.beginPath();
    ctx.ellipse(0, 2, 16, 7, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillRect(4, -10, 3, 8);
    ctx.fillRect(-2, -12, 12, 3);
  } else if (id === "hat") {
    ctx.fillRect(-8, -8, 16, 12);
    ctx.fillRect(-14, 4, 28, 4);
    ctx.strokeStyle = "#f4efe4";
    ctx.beginPath();
    ctx.moveTo(0, -8);
    ctx.lineTo(0, -14);
    ctx.moveTo(-4, -14);
    ctx.lineTo(4, -14);
    ctx.stroke();
  } else if (id === "whale") {
    ctx.beginPath();
    ctx.ellipse(0, 2, 16, 8, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(-14, 0);
    ctx.lineTo(-22, -6);
    ctx.lineTo(-22, 8);
    ctx.fill();
    ctx.fillStyle = "#f4efe4";
    ctx.beginPath();
    ctx.arc(8, 0, 1.5, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "biscotti") {
    const purple = "#7a3eaf";
    ctx.fillStyle = purple;
    ctx.beginPath();
    ctx.moveTo(-4, 1);
    ctx.quadraticCurveTo(-16, 0, -22, -5);
    ctx.quadraticCurveTo(-14, 6, -4, 7);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(-1, 3, 11, 6.5, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(6, 1);
    ctx.quadraticCurveTo(8, -6, 14, -12);
    ctx.quadraticCurveTo(19, -17, 23, -13);
    ctx.quadraticCurveTo(25, -11, 21, -10);
    ctx.quadraticCurveTo(16, -8, 12, 3);
    ctx.closePath();
    ctx.fill();
    ctx.fillRect(-9, 7, 3.2, 7);
    ctx.fillRect(-4, 8, 3.2, 6);
    ctx.fillRect(2, 7, 3.2, 6);
    ctx.fillRect(6, 6, 3, 5);
    ctx.fillStyle = "#6fbf62";
    ctx.beginPath();
    ctx.ellipse(-1, 3.6, 8.4, 5.6, 0, 0.02 * Math.PI, 0.98 * Math.PI);
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(21, -13.4, 0.8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#2a1238";
    ctx.lineWidth = 0.9;
    ctx.beginPath();
    ctx.arc(20.4, -12.2, 1.6, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  } else if (id === "gru") {
    ctx.fillStyle = "#9aa6b2";
    ctx.beginPath();
    ctx.moveTo(22, 0);
    ctx.lineTo(8, -6.5);
    ctx.lineTo(-12, -6.5);
    ctx.lineTo(-12, 6.5);
    ctx.lineTo(8, 6.5);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = "#d7dee6";
    ctx.fillRect(-8, -5.2, 14, 10.4);
    ctx.fillStyle = "#d24b3a";
    ctx.fillRect(7.2, -6.6, 2.4, 13.2);
    ctx.fillStyle = "#2c3138";
    ctx.beginPath();
    ctx.moveTo(-10, -6.5);
    ctx.lineTo(-20, -13);
    ctx.lineTo(-12, -3.2);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(-10, 6.5);
    ctx.lineTo(-20, 13);
    ctx.lineTo(-12, 3.2);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(1.5, 0, 2.6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#9fd0ff";
    ctx.beginPath();
    ctx.arc(1.9, -0.5, 1.25, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "falcon") {
    ctx.fillStyle = "#aeb8c2";
    ctx.beginPath();
    ctx.ellipse(-1, 0.5, 12, 8.5, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#8e99a4";
    ctx.fillRect(7, -2.4, 9, 1.6);
    ctx.fillRect(7, 1.4, 9, 1.6);
    ctx.fillStyle = "#d7dee6";
    ctx.beginPath();
    ctx.ellipse(9.5, -6.2, 3.3, 2.1, -0.45, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#6d7882";
    ctx.lineWidth = 1.1;
    ctx.beginPath();
    ctx.moveTo(6.2, -5.2);
    ctx.lineTo(2.2, -1.4);
    ctx.stroke();
    ctx.fillStyle = "#7d8b96";
    ctx.beginPath();
    ctx.arc(-6.5, -2.6, 1.7, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(-6.5, -2.6, 3.1, 0.2, Math.PI * 1.7);
    ctx.stroke();
  } else if (id === "iron") {
    ctx.fillStyle = "#c4372f";
    ctx.beginPath();
    ctx.ellipse(-1, 0, 7.2, 4.2, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#e2b34a";
    ctx.beginPath();
    ctx.ellipse(7.4, 0, 3.5, 2.7, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#fff6e0";
    ctx.fillRect(7.6, -0.7, 2.4, 0.55);
    ctx.fillStyle = "#7fd4ff";
    ctx.beginPath();
    ctx.arc(-1.2, 0, 1.55, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#e2b34a";
    ctx.fillRect(-12, -1.15, 5.2, 2.3);
    ctx.fillStyle = "#c4372f";
    ctx.fillRect(-3.2, -7.2, 2.3, 4.2);
    ctx.fillRect(-3.2, 3, 2.3, 4.2);
    ctx.fillStyle = "#f2d27a";
    ctx.beginPath();
    ctx.arc(-3.4, -7.6, 1.15, 0, Math.PI * 2);
    ctx.arc(-3.4, 7.6, 1.15, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "disco") {
    ctx.beginPath();
    ctx.arc(0, 0, 12, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#fff6d0";
    for (const [x, y] of [[-4, -4], [2, -2], [-2, 3], [4, 4]]) {
      ctx.fillRect(x, y, 3, 3);
    }
  } else {
    ctx.beginPath();
    ctx.moveTo(16, 0);
    ctx.lineTo(-12, -6);
    ctx.lineTo(-7, 0);
    ctx.lineTo(-12, 6);
    ctx.closePath();
    ctx.fill();
  }
  ctx.restore();
}

function paintAlien(ctx, id) {
  ctx.save();
  ctx.lineWidth = 2;
  if (id === "noodle") {
    ctx.strokeStyle = "#8fd0a8";
    ctx.beginPath();
    ctx.moveTo(0, 10);
    ctx.quadraticCurveTo(-8, 0, 0, -12);
    ctx.stroke();
    ctx.fillStyle = "#8fd0a8";
    ctx.beginPath();
    ctx.arc(0, -14, 4, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "whiskers") {
    ctx.fillStyle = "#e7d7b8";
    ctx.beginPath();
    ctx.arc(0, 2, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(-6, -2);
    ctx.lineTo(-10, -10);
    ctx.lineTo(-2, -4);
    ctx.moveTo(6, -2);
    ctx.lineTo(10, -10);
    ctx.lineTo(2, -4);
    ctx.fill();
    ctx.strokeStyle = "#f4efe4";
    ctx.beginPath();
    ctx.arc(0, -2, 9, Math.PI, 0);
    ctx.stroke();
  } else if (id === "square") {
    ctx.fillStyle = "#e0b15a";
    ctx.fillRect(-8, -8, 16, 16);
    ctx.strokeStyle = "#1b1916";
    ctx.beginPath();
    ctx.moveTo(-4, 2);
    ctx.quadraticCurveTo(0, 6, 4, 2);
    ctx.stroke();
    ctx.fillRect(-2, 8, 2, 6);
    ctx.fillRect(2, 8, 2, 6);
  } else if (id === "honk") {
    ctx.fillStyle = "#f4efe4";
    ctx.beginPath();
    ctx.ellipse(0, 2, 8, 6, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#e07a3d";
    ctx.beginPath();
    ctx.moveTo(6, 2);
    ctx.lineTo(16, 0);
    ctx.lineTo(6, 5);
    ctx.fill();
    ctx.strokeStyle = "#f6d36b";
    ctx.beginPath();
    ctx.moveTo(0, -4);
    ctx.lineTo(2, -14);
    ctx.stroke();
  } else if (id === "dave") {
    ctx.fillStyle = "#7dce6a";
    ctx.fillRect(-3, 4, 6, 8);
    ctx.fillStyle = "#d7a15a";
    ctx.beginPath();
    ctx.arc(0, -4, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#f0ddb0";
    ctx.beginPath();
    ctx.ellipse(0, -4, 11, 3, -0.3, 0, Math.PI * 2);
    ctx.stroke();
  } else if (id === "glitter") {
    ctx.fillStyle = "#c47ad4";
    ctx.beginPath();
    ctx.arc(0, 2, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(-7, 0);
    ctx.lineTo(-13, -6);
    ctx.lineTo(-4, -2);
    ctx.moveTo(7, 0);
    ctx.lineTo(13, -6);
    ctx.lineTo(4, -2);
    ctx.fill();
    ctx.fillStyle = "#fff6d0";
    for (const [x, y] of [[-10, 8], [8, -10], [12, 6]]) {
      ctx.fillRect(x, y, 2, 2);
    }
  } else if (id === "gloop") {
    ctx.fillStyle = "#6aa8e8";
    ctx.beginPath();
    ctx.moveTo(-8, -4);
    ctx.quadraticCurveTo(-10, 12, 0, 12);
    ctx.quadraticCurveTo(12, 12, 8, -4);
    ctx.quadraticCurveTo(0, 2, -8, -4);
    ctx.fill();
    ctx.fillStyle = "#f6d36b";
    ctx.beginPath();
    ctx.arc(-4, -8, 3, 0, Math.PI * 2);
    ctx.arc(5, -9, 2.4, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "pip") {
    ctx.fillStyle = "#f0b7a4";
    ctx.beginPath();
    ctx.moveTo(0, -12);
    ctx.lineTo(10, 10);
    ctx.lineTo(-10, 10);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(0, 2, 1.6, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "moth") {
    ctx.fillStyle = "#d7c6ef";
    ctx.beginPath();
    ctx.ellipse(-7, 0, 7, 10, -0.4, 0, Math.PI * 2);
    ctx.ellipse(7, 0, 7, 10, 0.4, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#6b5a86";
    ctx.fillRect(-2, -8, 4, 16);
  } else if (id === "beak") {
    ctx.fillStyle = "#f4efe4";
    ctx.beginPath();
    ctx.arc(0, 2, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#e07a3d";
    ctx.beginPath();
    ctx.moveTo(-3, 4);
    ctx.lineTo(8, 6);
    ctx.lineTo(-3, 8);
    ctx.fill();
    ctx.strokeStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(-2, 0, 4, 0, Math.PI * 2);
    ctx.stroke();
  } else if (id === "sock") {
    ctx.fillStyle = "#d9897b";
    ctx.beginPath();
    ctx.moveTo(-5, -12);
    ctx.lineTo(4, -12);
    ctx.lineTo(4, 4);
    ctx.lineTo(10, 8);
    ctx.lineTo(6, 12);
    ctx.lineTo(-5, 6);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(-1, -4, 1.2, 0, Math.PI * 2);
    ctx.arc(2, -4, 1.2, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "croissant") {
    ctx.strokeStyle = "#e6c98a";
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.arc(0, 2, 9, Math.PI * 0.85, Math.PI * 0.15, true);
    ctx.stroke();
    ctx.fillStyle = "#9f3040";
    ctx.beginPath();
    ctx.moveTo(-2, -8);
    ctx.lineTo(2, -14);
    ctx.lineTo(6, -8);
    ctx.fill();
  } else if (id === "lantern") {
    ctx.fillStyle = "#f6d36b";
    ctx.fillRect(-7, -6, 14, 14);
    ctx.fillStyle = "#1b1916";
    ctx.fillRect(-2, -10, 4, 4);
    ctx.beginPath();
    ctx.arc(-2, 0, 1.2, 0, Math.PI * 2);
    ctx.arc(3, 0, 1.2, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "wobble") {
    ctx.fillStyle = "#8fd0a8";
    ctx.beginPath();
    ctx.arc(0, 8, 7, 0, Math.PI * 2);
    ctx.arc(0, 0, 6, 0, Math.PI * 2);
    ctx.arc(0, -8, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#f6d36b";
    ctx.beginPath();
    ctx.moveTo(-4, -12);
    ctx.lineTo(0, -18);
    ctx.lineTo(4, -12);
    ctx.fill();
  } else if (id === "shedeur") {
    const skin = "#8fd0a8";
    const brown = "#3c2415";
    const orange = "#ff6a00";
    ctx.fillStyle = "#f4efe4";
    ctx.fillRect(-5, 10, 3.4, 6);
    ctx.fillRect(1.6, 10, 3.4, 6);
    ctx.fillStyle = skin;
    ctx.fillRect(-14, -1, 7, 3.4);
    ctx.fillRect(7, -1, 7, 3.4);
    ctx.fillStyle = brown;
    ctx.beginPath();
    ctx.moveTo(-7, -4);
    ctx.lineTo(-10, -1);
    ctx.lineTo(-7, 2);
    ctx.lineTo(-6, 11);
    ctx.lineTo(6, 11);
    ctx.lineTo(7, 2);
    ctx.lineTo(10, -1);
    ctx.lineTo(7, -4);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = orange;
    ctx.fillRect(-7, -4, 14, 2.2);
    ctx.fillRect(-10, -1, 3, 1.4);
    ctx.fillRect(7, -1, 3, 1.4);
    ctx.font = "bold 8px Segoe UI, sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.lineJoin = "round";
    ctx.lineWidth = 2.2;
    ctx.strokeStyle = "#fff";
    ctx.strokeText("2", 0, 4);
    ctx.fillStyle = orange;
    ctx.fillText("2", 0, 4);
    ctx.fillStyle = skin;
    ctx.beginPath();
    ctx.arc(0, -9, 5.6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(-2.1, -10.2, 0.85, 0, Math.PI * 2);
    ctx.arc(2.1, -10.2, 0.85, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(0, -8.4, 3.3, 0.08 * Math.PI, 0.92 * Math.PI);
    ctx.fill();
    ctx.fillStyle = "#fff";
    ctx.fillRect(-2.4, -7.5, 4.8, 1.5);
    ctx.save();
    ctx.translate(13.4, 0.5);
    ctx.fillStyle = "#d7dee4";
    ctx.fillRect(-1.3, -2.6, 2.6, 5.6);
    ctx.beginPath();
    for (let i = 0; i < 8; i += 1) {
      const angle = Math.PI / 8 + (i * Math.PI) / 4;
      const px = Math.cos(angle) * 3.3;
      const py = Math.sin(angle) * 3.3;
      if (i === 0) {
        ctx.moveTo(px, py);
      } else {
        ctx.lineTo(px, py);
      }
    }
    ctx.closePath();
    ctx.fillStyle = "#eef2f5";
    ctx.fill();
    ctx.lineWidth = 0.7;
    ctx.strokeStyle = "#8b97a3";
    ctx.stroke();
    ctx.fillStyle = "#16305c";
    ctx.beginPath();
    ctx.arc(0, 0, 1.6, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#f4efe4";
    ctx.lineWidth = 0.55;
    ctx.beginPath();
    ctx.moveTo(0, 0.2);
    ctx.lineTo(0, -1.15);
    ctx.moveTo(0, 0.2);
    ctx.lineTo(0.85, 0.55);
    ctx.stroke();
    ctx.restore();
  } else if (id === "kevin") {
    ctx.fillStyle = "#f2c84b";
    ctx.beginPath();
    ctx.ellipse(0, -1, 7.4, 11.4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.save();
    ctx.beginPath();
    ctx.ellipse(0, -1, 7.4, 11.4, 0, 0, Math.PI * 2);
    ctx.clip();
    ctx.fillStyle = "#2f5f9e";
    ctx.fillRect(-8, 2.2, 16, 12);
    ctx.strokeStyle = "#1b1916";
    ctx.lineWidth = 1.15;
    ctx.beginPath();
    ctx.moveTo(-2.3, 2.4);
    ctx.lineTo(-3.5, 10.2);
    ctx.moveTo(2.3, 2.4);
    ctx.lineTo(3.5, 10.2);
    ctx.stroke();
    ctx.restore();
    ctx.fillStyle = "#f2c84b";
    ctx.fillRect(-12.4, -2.4, 5.4, 3.6);
    ctx.fillRect(7, -2.4, 5.4, 3.6);
    ctx.fillStyle = "#2a2622";
    ctx.fillRect(-12.6, -2.2, 2.8, 3.3);
    ctx.fillRect(9.6, -2.2, 2.8, 3.3);
    ctx.fillStyle = "#3a342c";
    ctx.fillRect(-5.4, 8.8, 3.8, 2.6);
    ctx.fillRect(1.6, 8.8, 3.8, 2.6);
    ctx.fillStyle = "#c5ced6";
    ctx.fillRect(-5.4, 11, 3.8, 0.7);
    ctx.fillRect(1.6, 11, 3.8, 0.7);
    ctx.fillStyle = "#d5dbe3";
    ctx.fillRect(-6.6, -6.4, 13.2, 4.2);
    ctx.fillStyle = "#f7f4ee";
    ctx.beginPath();
    ctx.arc(-2.5, -4.3, 2.15, 0, Math.PI * 2);
    ctx.arc(2.5, -4.3, 2.15, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#8b97a3";
    ctx.lineWidth = 0.7;
    ctx.stroke();
    ctx.fillStyle = "#5b4636";
    ctx.beginPath();
    ctx.arc(-2.5, -4.2, 0.85, 0, Math.PI * 2);
    ctx.arc(2.5, -4.2, 0.85, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#1b1916";
    ctx.lineWidth = 1.05;
    ctx.beginPath();
    ctx.arc(0, -1.5, 2.5, 0.12 * Math.PI, 0.88 * Math.PI);
    ctx.stroke();
    ctx.fillStyle = "#3a342c";
    ctx.beginPath();
    ctx.moveTo(-1.4, -11.6);
    ctx.lineTo(0.1, -15.6);
    ctx.lineTo(1.7, -11.6);
    ctx.closePath();
    ctx.moveTo(1.5, -11.2);
    ctx.lineTo(3.8, -14.6);
    ctx.lineTo(4, -10.8);
    ctx.closePath();
    ctx.fill();
  } else if (id === "chewie") {
    ctx.fillStyle = "#8a5a32";
    ctx.fillRect(-4.2, -1, 8.4, 12);
    ctx.beginPath();
    ctx.arc(0, -5.5, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#6b4424";
    ctx.beginPath();
    ctx.ellipse(0, -3.8, 2.1, 1.5, 0, 0, Math.PI);
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(-1.7, -6.4, 0.7, 0, Math.PI * 2);
    ctx.arc(1.7, -6.4, 0.7, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#d7c39a";
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(-3.6, -0.5);
    ctx.lineTo(3.8, 8);
    ctx.stroke();
    ctx.fillStyle = "#c4553a";
    ctx.fillRect(-2.2, 0.4, 1.4, 1.4);
    ctx.fillRect(-0.6, 2.2, 1.4, 1.4);
    ctx.fillRect(1, 4, 1.4, 1.4);
  } else if (id === "grogu") {
    ctx.fillStyle = "#8d5a32";
    ctx.beginPath();
    ctx.ellipse(0, 5, 5.5, 6.5, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#7dba6a";
    ctx.beginPath();
    ctx.arc(0, -1.5, 4.6, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(-6.6, -1.2, 4.2, 2.2, 0.35, 0, Math.PI * 2);
    ctx.ellipse(6.6, -1.2, 4.2, 2.2, -0.35, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.ellipse(-1.7, -1.6, 1.35, 1.8, 0, 0, Math.PI * 2);
    ctx.ellipse(1.7, -1.6, 1.35, 1.8, 0, 0, Math.PI * 2);
    ctx.fill();
  } else if (id === "rocket") {
    ctx.fillStyle = "#8d6a45";
    ctx.beginPath();
    ctx.ellipse(0, 3, 4.6, 6.4, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#e07a2f";
    ctx.fillRect(-3.8, 1, 7.6, 5.4);
    ctx.fillStyle = "#d9d3c8";
    ctx.beginPath();
    ctx.arc(0, -4.2, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#3a342c";
    ctx.beginPath();
    ctx.ellipse(0, -3.4, 3.4, 2, 0, 0, Math.PI);
    ctx.fill();
    ctx.fillStyle = "#f7f4ee";
    ctx.beginPath();
    ctx.arc(-1.3, -4.6, 1.05, 0, Math.PI * 2);
    ctx.arc(1.3, -4.6, 1.05, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(-1.3, -4.6, 0.42, 0, Math.PI * 2);
    ctx.arc(1.3, -4.6, 0.42, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#6b4424";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(-2.6, 7);
    ctx.quadraticCurveTo(-8, 9, -6, 13);
    ctx.stroke();
  } else if (id === "groot") {
    ctx.fillStyle = "#8a5a32";
    ctx.fillRect(-2.6, -1, 5.2, 12);
    ctx.beginPath();
    ctx.arc(0, -5, 3.6, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#6b4424";
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.moveTo(-1.6, -7.4);
    ctx.lineTo(-2.8, -12.4);
    ctx.moveTo(0.8, -8);
    ctx.lineTo(2.6, -13);
    ctx.moveTo(0, -8.4);
    ctx.lineTo(0.2, -14);
    ctx.stroke();
    ctx.fillStyle = "#6fbf62";
    ctx.beginPath();
    ctx.ellipse(-2.8, -12.2, 1.5, 0.9, 0.5, 0, Math.PI * 2);
    ctx.ellipse(2.6, -12.8, 1.5, 0.9, -0.4, 0, Math.PI * 2);
    ctx.ellipse(0.2, -14, 1.4, 0.85, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#1b1916";
    ctx.beginPath();
    ctx.arc(-1.2, -5.2, 0.6, 0, Math.PI * 2);
    ctx.arc(1.2, -5.2, 0.6, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#c4553a";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(0, -3.6, 1.3, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.stroke();
  } else if (id === "quiet") {
    ctx.fillStyle = "#c5d0de";
    ctx.beginPath();
    ctx.arc(-6, 4, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#f4efe4";
    ctx.strokeRect(-2, -12, 16, 10);
  } else {
    ctx.fillStyle = "#8fd0a8";
    ctx.beginPath();
    ctx.arc(0, 0, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#162016";
    ctx.beginPath();
    ctx.arc(-4, -1, 1.5, 0, Math.PI * 2);
    ctx.arc(0, -2, 1.5, 0, Math.PI * 2);
    ctx.arc(4, -1, 1.5, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
}

function spawnGuest(alienId) {
  const width = flightCanvas.clientWidth || window.innerWidth;
  guests.push({
    id: alienId,
    x: -50,
    y: Math.max(150, (flightCanvas.clientHeight || 400) * 0.28) + Math.random() * Math.max(40, (flightCanvas.clientHeight || 400) * 0.28),
    speed: 78,
    wobble: Math.random() * Math.PI * 2,
  });
  if (guests.length > 3) {
    guests.shift();
  }
}

function paintAstronaut(ctx) {
  ctx.save();
  ctx.translate(0, -15);
  ctx.fillStyle = "#c5ced6";
  ctx.fillRect(-6.5, 0, 3.2, 6);
  ctx.fillStyle = "#f7f4ee";
  ctx.fillRect(-3.2, -0.5, 7.2, 7.2);
  ctx.fillRect(-2.4, 6.4, 2.1, 3.4);
  ctx.fillRect(1.2, 6.4, 2.1, 3.4);
  ctx.beginPath();
  ctx.arc(0.4, -5.2, 4.6, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#7eb6e6";
  ctx.beginPath();
  ctx.ellipse(1.5, -5.1, 2.2, 2.8, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function paintRider(ctx) {
  if (!stats.rider || !stats.aliens.includes(stats.rider)) {
    return;
  }
  const elapsed = (performance.now() - riderCheer) / 1000;
  const dancing = riderCheer > 0 && elapsed < 1.8;
  ctx.save();
  ctx.translate(-13, -18);
  if (dancing) {
    const hop = Math.abs(Math.sin(elapsed * Math.PI * 3.4)) * 11;
    const sway = Math.sin(elapsed * Math.PI * 6.2) * 0.42;
    ctx.translate(0, -hop);
    ctx.rotate(sway);
    ctx.fillStyle = "#f4d35e";
    for (let index = 0; index < 3; index += 1) {
      const spark = (elapsed * 1.6 + index / 3) % 1;
      ctx.globalAlpha = 0.9 * (1 - spark);
      ctx.beginPath();
      ctx.arc(Math.sin(index * 2.1) * 16, -6 - spark * 18, 1.4, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }
  ctx.scale(0.62, 0.62);
  paintAlien(ctx, stats.rider);
  ctx.restore();
}

function drawRocket(x, y, color, scale) {
  flightCtx.save();
  flightCtx.translate(x, y);
  flightCtx.scale(scale, scale);
  paintShip(flightCtx, stats.ship || "dart", color);
  paintRider(flightCtx);
  paintAstronaut(flightCtx);
  flightCtx.restore();
}

function drawFlight(now) {
  const dt = Math.min(0.05, (now - flightLast) / 1000);
  flightLast = now;
  flightClock += dt * flightSpeed * 0.75;

  const ratio = window.devicePixelRatio || 1;
  const width = flightCanvas.clientWidth;
  const height = flightCanvas.clientHeight;
  if (flightCanvas.width !== Math.floor(width * ratio) || flightCanvas.height !== Math.floor(height * ratio)) {
    flightCanvas.width = Math.floor(width * ratio);
    flightCanvas.height = Math.floor(height * ratio);
  }
  flightCtx.setTransform(ratio, 0, 0, ratio, 0, 0);
  flightCtx.clearRect(0, 0, width, height);
  const insets = safeInsets();
  const compact = width < 740;
  const checkpointScale = width < 430 ? 1.45 : compact ? 1.7 : 2.45;
  const edge = Math.max(compact ? 20 : 16, insets.right + 14);

  const styles = getComputedStyle(document.body);
  const accent = styles.getPropertyValue("--accent").trim();
  const text = styles.getPropertyValue("--text").trim();
  const muted = styles.getPropertyValue("--muted").trim();

  flightCtx.lineWidth = 1.5;
  for (const comet of comets) {
    comet.x -= comet.drift * flightSpeed * dt;
    if (comet.x < -28) {
      Object.assign(comet, makeComet(false));
    }
    flightCtx.globalAlpha = 0.35;
    flightCtx.strokeStyle = muted;
    flightCtx.beginPath();
    flightCtx.moveTo(comet.x, comet.y);
    flightCtx.lineTo(comet.x + 14 + comet.size * 4, comet.y);
    flightCtx.stroke();
    flightCtx.globalAlpha = 0.8;
    flightCtx.fillStyle = text;
    flightCtx.beginPath();
    flightCtx.arc(comet.x, comet.y, comet.size, 0, Math.PI * 2);
    flightCtx.fill();
  }

  if (now >= nextUfoAt) {
    launchUfoVisit(width, height);
    nextUfoAt = now + (170 + Math.random() * 50) * 1000;
  }
  flightCtx.globalAlpha = 0.92;
  for (let index = ufos.length - 1; index >= 0; index -= 1) {
    const ufo = ufos[index];
    ufo.x += ufo.speed * dt;
    drawUfo(ufo);
    if (ufo.x < -160 || ufo.x > width + 160) {
      ufos.splice(index, 1);
    }
  }

  flightCtx.globalAlpha = 1;
  for (let index = guests.length - 1; index >= 0; index -= 1) {
    const guest = guests[index];
    guest.x += guest.speed * dt;
    const bob = Math.sin(flightClock * 3 + guest.wobble) * 6;
    flightCtx.save();
    flightCtx.translate(guest.x, guest.y + bob);
    flightCtx.scale(compact ? 1.2 : 1.8, compact ? 1.2 : 1.8);
    paintAlien(flightCtx, guest.id);
    flightCtx.restore();
    if (guest.x > width + 80) {
      guests.splice(index, 1);
    }
  }

  if (activeCheckpoint) {
    const wide = activeCheckpoint.name === "Constellation";
    const reach = (wide ? 48 : activeCheckpoint.name === "Saturn" ? 24 : 18) * checkpointScale;
    const dockX = width - edge - reach;
    const dockY = Math.max(insets.top + reach + (compact ? 28 : 20), compact ? 148 : 92);
    const glide = Math.min(1, dt * 1.4);
    activeCheckpoint.x += (dockX - activeCheckpoint.x) * glide;
    activeCheckpoint.y += (dockY - activeCheckpoint.y) * glide;
    if (currentScreen === "trivia") {
      flightCtx.globalAlpha = 0.95;
      drawCheckpointGraphic(activeCheckpoint.name, activeCheckpoint.x, activeCheckpoint.y, checkpointScale);
    }
  }

  const rocketScale = compact ? 0.78 : 1;
  const rocketX = width * (compact ? 0.34 : 0.28) + Math.sin(flightClock * 0.65) * width * (compact ? 0.16 : 0.24);
  let rocketY = (compact ? height * 0.58 : height * 0.48) + Math.sin(flightClock * 1.05) * height * (compact ? 0.14 : 0.3);
  if (compact) {
    rocketY = Math.max(insets.top + 168, Math.min(height - 96, rocketY));
  }
  drawRocket(rocketX, rocketY, accent, rocketScale);

  const tracker = checkpointName(stats.currentStreak);
  if (currentScreen === "trivia" && tracker !== "—" && activeCheckpoint) {
    const reach = (tracker === "Constellation" ? 48 : tracker === "Saturn" ? 24 : 18) * checkpointScale;
    const labelY = Math.max(insets.top + 8, activeCheckpoint.y - reach - 8);
    flightCtx.globalAlpha = 0.9;
    flightCtx.fillStyle = text;
    flightCtx.font = `700 ${compact ? 13 : 15}px Fredoka, sans-serif`;
    flightCtx.textAlign = "right";
    flightCtx.textBaseline = "top";
    flightCtx.fillText(tracker, width - edge, labelY);
  }
  flightCtx.globalAlpha = 1;

  requestAnimationFrame(drawFlight);
}

requestAnimationFrame(drawFlight);

if ("serviceWorker" in navigator) {
  let reloading = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (reloading) {
      return;
    }
    reloading = true;
    window.location.reload();
  });
  navigator.serviceWorker.register("sw.js", { updateViaCache: "none" })
    .then((registration) => registration.update())
    .catch(() => {});
}

fetch("questions.json")
  .then((response) => response.json())
  .then((loaded) => {
    questions = loaded;
  })
  .catch(() => {
    questions = [];
  });
