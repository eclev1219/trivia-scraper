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
  document.querySelector("#fact").classList.add("hidden");
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
    button.classList.add("correct");
  } else {
    stats.currentStreak = 0;
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
  showFact();
  document.querySelector("#next-question").classList.remove("hidden");
}

function showFact() {
  const fact = current.fact || `The correct answer is ${current.correct_answer}.`;
  document.querySelector("#fact-text").textContent = fact;
  const credit = document.querySelector("#fact-credit");
  if (current.fact_source === "Wikipedia") {
    credit.textContent = "From Wikipedia, CC BY-SA 4.0.";
    credit.classList.remove("hidden");
  } else {
    credit.textContent = "";
    credit.classList.add("hidden");
  }
  document.querySelector("#fact").classList.remove("hidden");
}

function accuracy() {
  if (stats.answered === 0) {
    return "—";
  }
  return `${Math.round((stats.correct / stats.answered) * 1000) / 10}%`;
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
  // Beethoven's Ode to Joy, which is in the public domain.
  const melody = [64, 64, 65, 67, 67, 65, 64, 62, 60, 60, 62, 64, 64, 62, 62];
  const events = [];
  melody.forEach((note, index) => {
    const held = index === 12 || index === 14 ? 0.9 : 0.42;
    events.push({ note, time: index * 0.5, duration: held, wave: "triangle", volume: 0.18 });
  });
  for (const time of [0, 4, 8]) {
    events.push({ note: 48, time, duration: 1.4, wave: "sine", volume: 0.08 });
  }
  return { events, loopSeconds: 8 };
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

  if (kind === "jazz" || kind === "classical") {
    musicMaster.gain.value = 0.9;
    const tune = kind === "jazz" ? jazzTune() : classicalTune();
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

fetch("questions.json")
  .then((response) => response.json())
  .then((loaded) => {
    questions = loaded;
    document.querySelector("#bank-size").textContent =
      `${questions.length.toLocaleString()} questions in the bank`;
  })
  .catch(() => {
    document.querySelector("#bank-size").textContent =
      "The question bank could not be loaded.";
  });
