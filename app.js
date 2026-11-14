const STATS_KEY = "trivia-stats";
const SETTINGS_KEY = "trivia-settings";

const screens = {
  home: document.querySelector("#home"),
  trivia: document.querySelector("#trivia"),
  stats: document.querySelector("#stats"),
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
});

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
let musicGeneration = 0;

function loadJson(key, fallback) {
  const saved = localStorage.getItem(key);
  if (!saved) {
    return fallback;
  }
  return { ...fallback, ...JSON.parse(saved) };
}

function saveJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function show(name) {
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

function buildDeck() {
  const preferred = [];
  const others = [];
  for (const question of questions) {
    const general = PREFERRED_CATEGORIES.has(question.category) || question.source === "original";
    if (general) {
      preferred.push(question);
    } else {
      others.push(question);
    }
  }
  // History, places, animals, and the added questions come up more often.
  return shuffle([...preferred, ...preferred, ...others]);
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
}

function grade(button, answer) {
  if (answeredThisCard) {
    return;
  }
  answeredThisCard = true;

  const correct = answer === current.correct_answer;
  stats.answered += 1;
  stats.categories[current.category] = (stats.categories[current.category] || 0) + 1;

  if (correct) {
    stats.correct += 1;
    stats.currentStreak += 1;
    sessionCorrect += 1;
    stats.longestStreak = Math.max(stats.longestStreak, stats.currentStreak);
    stats.bestSession = Math.max(stats.bestSession, sessionCorrect);
    noteCheckpoint(stats.currentStreak);
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
  document.querySelector("#next-question").classList.remove("hidden");
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

function favoriteCategory() {
  const entries = Object.entries(stats.categories);
  if (entries.length === 0) {
    return "—";
  }
  entries.sort((a, b) => b[1] - a[1]);
  return entries[0][0];
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
    ["Furthest checkpoint", checkpointName(stats.furthestCheckpoint)],
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
  musicHums = [];
  if (musicMaster) {
    musicMaster.disconnect();
    musicMaster = null;
  }
}

function playTone(note, time, duration, wave, volume) {
  const oscillator = audioContext.createOscillator();
  const gain = audioContext.createGain();
  oscillator.type = wave;
  oscillator.frequency.value = midi(note);
  gain.gain.setValueAtTime(0.0001, time);
  gain.gain.exponentialRampToValueAtTime(volume, time + 0.03);
  gain.gain.exponentialRampToValueAtTime(0.0001, time + duration);
  oscillator.connect(gain);
  gain.connect(musicMaster);
  oscillator.start(time);
  oscillator.stop(time + duration + 0.05);
}

function scheduleLoop(events, loopSeconds, generation) {
  if (generation !== musicGeneration) {
    return;
  }
  const start = audioContext.currentTime + 0.06;
  for (const event of events) {
    if (generation !== musicGeneration) {
      return;
    }
    playTone(event.note, start + event.time, event.duration, event.wave, event.volume);
  }
  window.setTimeout(() => scheduleLoop(events, loopSeconds, generation), loopSeconds * 1000);
}

function classicalTune() {
  // Beethoven's Ode to Joy, which is in the public domain, with a harmony and bass.
  const melody = [
    64, 64, 65, 67, 67, 65, 64, 62, 60, 60, 62, 64, 64, 62, 62, 62,
    64, 64, 65, 67, 67, 65, 64, 62, 60, 60, 62, 64, 62, 60, 60, 60,
  ];
  const harmony = [
    60, 60, 60, 64, 64, 60, 60, 59, 55, 55, 57, 60, 60, 59, 59, 59,
    60, 60, 60, 64, 64, 60, 60, 59, 55, 55, 57, 60, 59, 55, 55, 55,
  ];
  const events = [];
  const step = 0.48;
  melody.forEach((note, index) => {
    const phraseEnd = index === 14 || index === 15 || index === 30 || index === 31;
    const duration = phraseEnd ? 0.78 : 0.4;
    events.push({ note, time: index * step, duration, wave: "triangle", volume: 0.16 });
    events.push({ note: harmony[index], time: index * step, duration, wave: "sine", volume: 0.08 });
  });
  const bass = [48, 43, 41, 43, 48, 43, 45, 41];
  bass.forEach((note, index) => {
    events.push({ note, time: index * step * 4, duration: 1.7, wave: "triangle", volume: 0.1 });
  });
  return { events, loopSeconds: melody.length * step + 0.35 };
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

  const tunes = { jazz: jazzTune, classical: classicalTune, space: spaceTune };
  if (tunes[kind]) {
    musicMaster.gain.value = kind === "space" ? 0.8 : 0.9;
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
  show("home");
}

document.querySelector("#open-stats").addEventListener("click", () => {
  renderStats();
  show("stats");
});
document.querySelector("#open-trivia").addEventListener("click", openTrivia);
document.querySelector("#open-settings").addEventListener("click", () => show("settings"));
document.querySelector("#trivia-home").addEventListener("click", goHome);
document.querySelector("#stats-home").addEventListener("click", () => show("home"));
document.querySelector("#settings-home").addEventListener("click", () => show("home"));
document.querySelector("#next-question").addEventListener("click", showQuestion);

for (const button of document.querySelectorAll("[data-theme-choice]")) {
  button.addEventListener("click", () => {
    settings.theme = button.dataset.themeChoice;
    saveJson(SETTINGS_KEY, settings);
    applyTheme(settings.theme);
  });
}

for (const button of document.querySelectorAll("[data-music-choice]")) {
  button.addEventListener("click", () => {
    settings.music = button.dataset.musicChoice;
    saveJson(SETTINGS_KEY, settings);
    startMusic(settings.music);
  });
}

applyTheme(settings.theme);
startMusic("off");
for (const button of document.querySelectorAll("[data-music-choice]")) {
  button.classList.toggle("selected", button.dataset.musicChoice === settings.music);
}

const flightCanvas = document.querySelector("#flight");
const flightCtx = flightCanvas.getContext("2d");
let flightSpeed = Number(localStorage.getItem("trivia-flight-speed"));
if (!Number.isFinite(flightSpeed) || flightSpeed <= 0) {
  flightSpeed = 1;
}

function changeFlightSpeed(correct) {
  if (correct) {
    flightSpeed = Math.min(8, flightSpeed + 0.5);
  } else {
    flightSpeed = 1;
  }
  localStorage.setItem("trivia-flight-speed", String(flightSpeed));
}

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
let nextUfoAt = performance.now() + 6000;
let activeCheckpoint = null;
let flightClock = 0;
let flightLast = performance.now();

function launchUfoVisit(width, height) {
  const fromLeft = Math.random() < 0.5;
  const direction = fromLeft ? 1 : -1;
  for (let index = 0; index < 2; index += 1) {
    ufos.push({
      x: (fromLeft ? -110 : width + 110) - direction * index * 120,
      y: 64 + Math.random() * Math.max(50, height * 0.42),
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
    y: 92,
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

function drawCheckpointGraphic(name, x, y) {
  flightCtx.save();
  flightCtx.translate(x, y);
  flightCtx.scale(2.45, 2.45);
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

function drawRocket(x, y, color) {
  flightCtx.save();
  flightCtx.translate(x, y);
  flightCtx.fillStyle = color;
  flightCtx.beginPath();
  flightCtx.moveTo(16, 0);
  flightCtx.lineTo(-12, -6);
  flightCtx.lineTo(-7, 0);
  flightCtx.lineTo(-12, 6);
  flightCtx.closePath();
  flightCtx.fill();
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

  if (activeCheckpoint) {
    const wide = activeCheckpoint.name === "Constellation";
    const dockX = width - (wide ? 156 : 84);
    const dockY = 92;
    const glide = Math.min(1, dt * 1.4);
    activeCheckpoint.x += (dockX - activeCheckpoint.x) * glide;
    activeCheckpoint.y += (dockY - activeCheckpoint.y) * glide;
    flightCtx.globalAlpha = 0.95;
    drawCheckpointGraphic(activeCheckpoint.name, activeCheckpoint.x, activeCheckpoint.y);
  }

  const rocketX = width * 0.28 + Math.sin(flightClock * 0.65) * width * 0.24;
  const rocketY = height * 0.48 + Math.sin(flightClock * 1.05) * height * 0.3;
  drawRocket(rocketX, rocketY, accent);

  const tracker = checkpointName(stats.currentStreak);
  if (tracker !== "—") {
    flightCtx.globalAlpha = 0.9;
    flightCtx.fillStyle = text;
    flightCtx.font = "15px Segoe UI, sans-serif";
    flightCtx.textAlign = "right";
    flightCtx.textBaseline = "top";
    flightCtx.fillText(tracker, width - 16, 6);
  }
  flightCtx.globalAlpha = 1;

  requestAnimationFrame(drawFlight);
}

requestAnimationFrame(drawFlight);

fetch("questions.json")
  .then((response) => response.json())
  .then((loaded) => {
    questions = loaded;
  })
  .catch(() => {
    questions = [];
  });
