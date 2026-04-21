// ═══════════════════════════════════════════════════════════════
//  LE PENDU MÉDECINE · game.js
//  Logique principale du jeu — version 0.2 web
// ═══════════════════════════════════════════════════════════════

'use strict';

/* ─── CONFIG ─────────────────────────────────────────────────── */
const CONFIG = {
  maxAttempts:    6,
  initialLives:   3,
  bonusEvery:     5,          // Écran bonus toutes les N victoires
  bonusImages: [              // Chemin relatif depuis index.html
    'assets/images/niveau_01.jpg',
    'assets/images/niveau_02.jpg',
    'assets/images/niveau_03.jpg',
    'assets/images/niveau_04.jpg',
    'assets/images/niveau_05.jpg',
    'assets/images/niveau_06.jpg',
  ],
  sounds: {
    bg:      'assets/sounds/background.mp3',
    victory: 'assets/sounds/victory.mp3',
    defeat:  'assets/sounds/defeat.mp3',
    click:   'assets/sounds/click.mp3',
    correct: 'assets/sounds/correct.mp3',
    wrong:   'assets/sounds/wrong.mp3',
  },
  // Parties du pendu dans l'ordre d'apparition
  gallowsParts: ['g-head','g-body','g-arm-l','g-arm-r','g-leg-l','g-leg-r'],
};

/* ─── KEYBOARD ROWS ──────────────────────────────────────────── */
const KB_ROWS = [
  ['a','z','e','r','t','y','u','i','o','p'],
  ['q','s','d','f','g','h','j','k','l','m'],
  ['w','x','c','v','b','n'],
];

/* ─── STATE ──────────────────────────────────────────────────── */
let state = {};

function initState() {
  state = {
    score:         0,
    victories:     0,
    lives:         CONFIG.initialLives,
    // per-round
    word:          '',
    definition:    '',
    category:      '',
    correct:       new Set(),
    wrong:         new Set(),
    attempts:      0,
    gameRunning:   false,
    soundEnabled:  true,
    bonusIndex:    0,
    // words pool (shuffle once)
    wordsPool:     shuffle([...WORDS_DATA]),
    poolIndex:     0,
  };
}

/* ─── SOUND ──────────────────────────────────────────────────── */
const audio = {};

function loadAudio() {
  for (const [key, src] of Object.entries(CONFIG.sounds)) {
    try {
      audio[key] = new Audio(src);
      if (key === 'bg') {
        audio[key].loop = true;
        audio[key].volume = 0.35;
      } else {
        audio[key].volume = 0.7;
      }
    } catch(e) { /* son optionnel */ }
  }
}

function playSound(key) {
  if (!state.soundEnabled) return;
  const a = audio[key];
  if (!a) return;
  try {
    a.currentTime = 0;
    a.play().catch(() => {});
  } catch(e) {}
}

function stopSound(key) {
  const a = audio[key];
  if (a) { try { a.pause(); a.currentTime = 0; } catch(e) {} }
}

/* ─── DOM REFS ───────────────────────────────────────────────── */
const $ = id => document.getElementById(id);
const screens = {
  title:    $('screen-title'),
  game:     $('screen-game'),
  result:   $('screen-result'),
  bonus:    $('screen-bonus'),
  gameover: $('screen-gameover'),
};

/* ─── SCREEN TRANSITIONS ─────────────────────────────────────── */
function showScreen(name) {
  Object.values(screens).forEach(s => {
    s.style.display = 'none';
    s.classList.remove('active');
  });
  const target = screens[name];
  target.style.display = 'flex';
  // Force reflow then fade in
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      target.style.opacity = '1';
      target.classList.add('active');
    });
  });
}

/* ─── UTILITIES ──────────────────────────────────────────────── */
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function normalize(str) {
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

function pickWord() {
  if (state.poolIndex >= state.wordsPool.length) {
    state.wordsPool = shuffle([...WORDS_DATA]);
    state.poolIndex = 0;
  }
  const entry = state.wordsPool[state.poolIndex++];
  return entry;
}

function showToast(msg, duration = 2200) {
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), duration);
}

/* ─── LIVES HUD ──────────────────────────────────────────────── */
function renderLives() {
  const el = $('lives-icons');
  el.innerHTML = '';
  for (let i = 0; i < CONFIG.initialLives; i++) {
    const span = document.createElement('span');
    span.className = 'heart' + (i >= state.lives ? ' lost' : '');
    span.textContent = '❤';
    el.appendChild(span);
  }
}

function animateHud(id) {
  const el = $(id);
  el.classList.remove('pop');
  void el.offsetWidth;
  el.classList.add('pop');
}

/* ─── GALLOWS ────────────────────────────────────────────────── */
function renderGallows() {
  CONFIG.gallowsParts.forEach((id, i) => {
    const el = $(id);
    if (!el) return;
    el.classList.toggle('hidden', i >= state.attempts);
    el.classList.toggle('show',   i < state.attempts);
  });
  $('attempts-counter').textContent = `${state.attempts} / ${CONFIG.maxAttempts}`;
}

/* ─── WORD DISPLAY ───────────────────────────────────────────── */
function renderWord(revealAll = false) {
  const container = $('word-display');
  container.innerHTML = '';
  const wordNorm = normalize(state.word);

  for (const ch of state.word) {
    if (ch === ' ') {
      const sp = document.createElement('span');
      sp.className = 'space-slot';
      container.appendChild(sp);
      continue;
    }
    const slot  = document.createElement('div');
    slot.className = 'letter-slot';
    const chNorm = normalize(ch);
    const revealed = revealAll || state.correct.has(chNorm);

    const charEl = document.createElement('span');
    charEl.className = 'letter-char' + (revealed ? ' revealed' : '');
    charEl.textContent = revealed ? ch.toUpperCase() : '';
    charEl.setAttribute('data-norm', chNorm);

    const line = document.createElement('div');
    line.className = 'letter-line';

    slot.appendChild(charEl);
    slot.appendChild(line);
    container.appendChild(slot);
  }
}

function revealLetter(letter) {
  document.querySelectorAll('.letter-char').forEach(el => {
    if (el.dataset.norm === letter) {
      el.textContent = el.closest('.letter-slot').previousSibling
        ? '' : ''; // will re-render
    }
  });
  // Simpler: just re-render
  renderWord();
}

/* ─── WRONG LETTERS ──────────────────────────────────────────── */
function renderWrong() {
  const container = $('wrong-letters');
  container.innerHTML = '';
  [...state.wrong].sort().forEach(l => {
    const chip = document.createElement('span');
    chip.className = 'wrong-chip';
    chip.textContent = l.toUpperCase();
    container.appendChild(chip);
  });
}

/* ─── KEYBOARD ───────────────────────────────────────────────── */
function buildKeyboard() {
  const kb = $('keyboard');
  kb.innerHTML = '';
  KB_ROWS.forEach(row => {
    const rowEl = document.createElement('div');
    rowEl.className = 'kb-row';
    row.forEach(letter => {
      const btn = document.createElement('button');
      btn.className = 'kb-key';
      btn.textContent = letter.toUpperCase();
      btn.dataset.letter = letter;
      btn.addEventListener('click', () => handleGuess(letter));
      rowEl.appendChild(btn);
    });
    kb.appendChild(rowEl);
  });
}

function updateKeyboard() {
  document.querySelectorAll('.kb-key').forEach(btn => {
    const l = btn.dataset.letter;
    if (state.correct.has(l)) {
      btn.classList.add('correct');
      btn.disabled = true;
    } else if (state.wrong.has(l)) {
      btn.classList.add('wrong');
      btn.disabled = true;
    } else {
      btn.classList.remove('correct','wrong');
      btn.disabled = false;
    }
  });
}

/* ─── NEW ROUND ──────────────────────────────────────────────── */
function startRound() {
  const entry      = pickWord();
  state.word       = entry.word;
  state.definition = entry.definition;
  state.category   = entry.category || '';
  state.correct    = new Set();
  state.wrong      = new Set();
  state.attempts   = 0;
  state.gameRunning = true;

  renderWord();
  renderGallows();
  renderWrong();
  updateKeyboard();
  $('definition-display').textContent = state.definition;
}

/* ─── CHECK WIN / LOSE ───────────────────────────────────────── */
function checkWin() {
  const wordLetters = [...new Set(normalize(state.word).replace(/[^a-z]/g,''))];
  return wordLetters.every(l => state.correct.has(l));
}

/* ─── HANDLE GUESS ───────────────────────────────────────────── */
function handleGuess(letter) {
  if (!state.gameRunning) return;
  letter = normalize(letter);
  if (!/^[a-z]$/.test(letter)) return;
  if (state.correct.has(letter) || state.wrong.has(letter)) {
    showToast(`« ${letter.toUpperCase()} » déjà essayée !`);
    return;
  }

  const wordNorm = normalize(state.word);
  if (wordNorm.includes(letter)) {
    state.correct.add(letter);
    playSound('correct');
    renderWord();
    updateKeyboard();
    if (checkWin()) {
      state.gameRunning = false;
      setTimeout(() => onWin(), 600);
    }
  } else {
    state.wrong.add(letter);
    state.attempts++;
    playSound('wrong');
    renderGallows();
    renderWrong();
    updateKeyboard();
    if (state.attempts >= CONFIG.maxAttempts) {
      state.gameRunning = false;
      setTimeout(() => onLose(), 600);
    }
  }
}

/* ─── WIN ─────────────────────────────────────────────────────── */
function onWin() {
  state.victories++;
  state.score++;
  stopSound('bg');
  playSound('victory');

  $('result-icon').textContent   = '🏆';
  $('result-title').textContent  = 'Bravo !';
  $('result-word').textContent   = state.word.toUpperCase();
  $('result-definition').textContent = state.definition;

  animateHud('score-value');
  $('score-value').textContent    = state.score;
  $('victories-value').textContent = state.victories;

  showScreen('result');

  $('btn-continue').onclick = () => {
    stopSound('victory');
    if (state.victories % CONFIG.bonusEvery === 0) {
      showBonusScreen();
    } else {
      nextRound();
    }
  };
  $('btn-quit').onclick = () => confirmQuit();
}

/* ─── LOSE ────────────────────────────────────────────────────── */
function onLose() {
  state.lives--;
  stopSound('bg');
  playSound('defeat');
  renderLives();
  renderWord(true); // Reveal answer

  $('result-icon').textContent  = '💀';
  $('result-title').textContent = 'Perdu !';
  $('result-word').textContent  = state.word.toUpperCase();
  $('result-definition').textContent = state.definition;

  showScreen('result');

  $('btn-continue').onclick = () => {
    stopSound('defeat');
    if (state.lives <= 0) {
      showGameOver();
    } else {
      nextRound();
    }
  };
  $('btn-quit').onclick = () => confirmQuit();
}

/* ─── NEXT ROUND ─────────────────────────────────────────────── */
function nextRound() {
  showScreen('game');
  if (state.soundEnabled) {
    playSound('bg');
  }
  buildKeyboard();
  startRound();
}

/* ─── BONUS SCREEN ───────────────────────────────────────────── */
function showBonusScreen() {
  $('bonus-title').textContent = `Niveau ${Math.floor(state.victories / CONFIG.bonusEvery)} accompli !`;
  $('bonus-stats').textContent = `Score : ${state.score} · Victoires : ${state.victories} · Vies : ${state.lives}`;

  const imgPath = CONFIG.bonusImages[state.bonusIndex % CONFIG.bonusImages.length];
  state.bonusIndex++;

  const zone = $('bonus-image-zone');
  zone.innerHTML = '';

  const img = new Image();
  img.id = 'bonus-img';
  img.alt = `Niveau ${Math.floor(state.victories / CONFIG.bonusEvery)}`;
  img.onload = () => {
    zone.innerHTML = '';
    zone.appendChild(img);
  };
  img.onerror = () => {
    // Image non trouvée → afficher le placeholder
    zone.innerHTML = `
      <div class="bonus-image-placeholder">
        <svg viewBox="0 0 200 150" width="200">
          <rect width="200" height="150" rx="8" fill="var(--surface2)"/>
          <text x="100" y="70" text-anchor="middle" fill="var(--text-muted)" font-size="12" font-family="Crimson Pro">Image non trouvée</text>
          <text x="100" y="90" text-anchor="middle" fill="var(--text-muted)" font-size="11" font-family="Crimson Pro">${imgPath}</text>
        </svg>
        <p class="bonus-image-hint">Placez vos images dans <code>assets/images/</code></p>
      </div>`;
  };
  img.src = imgPath;

  showScreen('bonus');

  $('btn-bonus-yes').onclick = () => nextRound();
  $('btn-bonus-no').onclick  = () => { playSound('click'); pygame_quit(); };
}

/* ─── GAME OVER ──────────────────────────────────────────────── */
function showGameOver() {
  const stats = $('gameover-stats');
  stats.innerHTML = `
    <div class="stat-item"><span class="stat-label">Score</span><span class="stat-value">${state.score}</span></div>
    <div class="stat-item"><span class="stat-label">Victoires</span><span class="stat-value">${state.victories}</span></div>
    <div class="stat-item"><span class="stat-label">Vies</span><span class="stat-value">0</span></div>
  `;
  showScreen('gameover');
  playSound('defeat');

  $('btn-restart').onclick = () => {
    stopSound('defeat');
    initState();
    loadAudio();
    showScreen('game');
    buildKeyboard();
    renderLives();
    $('score-value').textContent     = 0;
    $('victories-value').textContent = 0;
    startRound();
    playSound('bg');
  };
}

/* ─── QUIT ───────────────────────────────────────────────────── */
function confirmQuit() {
  if (confirm('Quitter la partie en cours ?')) {
    pygame_quit();
  }
}

function pygame_quit() {
  // Dans un contexte web, on affiche un écran de fin
  showGameOver();
}

/* ─── KEYBOARD INPUT ─────────────────────────────────────────── */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') return;
  if (!state.gameRunning) return;
  const letter = e.key;
  if (/^[a-zA-ZÀ-ÿ]$/.test(letter)) {
    handleGuess(letter);
  }
});

/* ─── SOUND BUTTON ───────────────────────────────────────────── */
$('btn-sound').addEventListener('click', () => {
  state.soundEnabled = !state.soundEnabled;
  $('btn-sound').textContent = state.soundEnabled ? '🔊' : '🔇';
  if (!state.soundEnabled) {
    Object.keys(audio).forEach(stopSound);
  } else {
    if (screens.game.classList.contains('active')) playSound('bg');
  }
});

/* ─── MENU BUTTON ────────────────────────────────────────────── */
$('btn-menu').addEventListener('click', () => {
  if (confirm('Retourner au menu principal ? La partie sera perdue.')) {
    state.gameRunning = false;
    Object.keys(audio).forEach(stopSound);
    showScreen('title');
  }
});

/* ─── TITLE SCREEN ───────────────────────────────────────────── */
function startFromTitle() {
  showScreen('game');
  buildKeyboard();
  renderLives();
  $('score-value').textContent     = state.score;
  $('victories-value').textContent = state.victories;
  startRound();
  // Démarrer la musique de fond (nécessite interaction utilisateur)
  if (state.soundEnabled) playSound('bg');
}

screens.title.addEventListener('click', startFromTitle);
screens.title.addEventListener('keydown', e => {
  if (e.key === ' ' || e.key === 'Enter') startFromTitle();
});

/* ─── INIT ───────────────────────────────────────────────────── */
(function init() {
  initState();
  loadAudio();
  showScreen('title');

  // Rendre le title screen focusable pour keydown
  screens.title.tabIndex = 0;
  screens.title.focus();
})();
