#!/usr/bin/env python3
import re

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .xp-toast CSS to top-right
old_toast_css = """    #xbox-preview .xp-toast {
      position: absolute;
      top: 14%;
      left: 50%;
      transform: translate(-50%, -8px);
      padding: 9px 18px;
      border: 1px solid var(--xp-pink);
      border-radius: 999px;
      background: #141418fa;
      font-size: 12px;
      font-weight: 800;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s ease;
      white-space: nowrap;
      box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 20px rgba(255,0,96,0.3);
      z-index: 25;
    }
    #xbox-preview .xp-toast.on {
      opacity: 1;
      transform: translate(-50%, 0);
    }"""

new_toast_css = """    #xbox-preview .xp-toast {
      position: absolute;
      top: 22px;
      right: 36px;
      left: auto;
      transform: translateY(-8px);
      padding: 8px 16px;
      border: 1px solid var(--xp-pink);
      border-radius: 999px;
      background: rgba(18, 20, 26, 0.94);
      font-size: 11px;
      font-weight: 800;
      color: #FFFFFF;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s ease;
      white-space: nowrap;
      box-shadow: 0 10px 30px rgba(0,0,0,0.85), 0 0 20px rgba(255,0,96,0.35);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      z-index: 35;
    }
    #xbox-preview .xp-toast.on {
      opacity: 1;
      transform: translateY(0);
    }"""

if old_toast_css in content:
    content = content.replace(old_toast_css, new_toast_css, 1)
else:
    print("WARNING: old_toast_css not found verbatim")

# 2. Add Music Hero & Square Cards CSS
music_ui_css = """
    /* DEDICATED HI-FI MUSIC HERO EXPERIENCE */
    #xbox-preview .xp-hero-music {
      display: flex;
      align-items: center;
      gap: clamp(16px, 2.5vw, 32px);
      width: min(90%, 880px);
      z-index: 5;
    }
    #xbox-preview .xp-music-hero-left {
      flex-shrink: 0;
    }
    #xbox-preview .xp-music-vinyl-wrap {
      position: relative;
      width: clamp(130px, 14vw, 172px);
      height: clamp(130px, 14vw, 172px);
    }
    #xbox-preview .xp-music-sleeve {
      position: relative;
      width: 100%;
      height: 100%;
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.22);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.85), 0 0 26px rgba(255, 0, 96, 0.25);
      z-index: 2;
      background: #141418;
    }
    #xbox-preview .xp-music-sleeve-inner {
      width: 100%;
      height: 100%;
      background-size: cover;
      background-position: center;
      transition: background-image 0.3s ease;
    }
    #xbox-preview .xp-music-vinyl {
      position: absolute;
      top: 5px;
      right: -24px;
      bottom: 5px;
      width: clamp(120px, 13vw, 160px);
      border-radius: 50%;
      background: radial-gradient(circle, #2a2a2e 0%, #121215 55%, #050507 100%);
      border: 1px solid rgba(255, 255, 255, 0.16);
      box-shadow: 0 12px 28px rgba(0,0,0,0.85);
      z-index: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      animation: xpSpin 8s linear infinite;
      animation-play-state: paused;
    }
    #xbox-preview .xp-music-vinyl.playing {
      animation-play-state: running;
    }
    @keyframes xpSpin {
      100% { transform: rotate(360deg); }
    }
    #xbox-preview .xp-vinyl-grooves {
      position: absolute;
      inset: 10px;
      border-radius: 50%;
      border: 1px dashed rgba(255, 255, 255, 0.08);
    }
    #xbox-preview .xp-vinyl-center {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background-size: cover;
      background-position: center;
      border: 2px solid #000;
      box-shadow: inset 0 0 4px #000;
    }

    #xbox-preview .xp-music-hero-right {
      display: flex;
      flex-direction: column;
      gap: 5px;
      flex: 1 1 auto;
      min-width: 0;
    }
    #xbox-preview .xp-music-tags-row {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    #xbox-preview .xp-music-tag-genre {
      background: rgba(255, 0, 96, 0.22);
      border: 1px solid var(--xp-pink);
      color: #FFFFFF;
      font-size: 9px;
      font-weight: 900;
      letter-spacing: 0.08em;
      padding: 2px 8px;
      border-radius: 999px;
      text-transform: uppercase;
    }
    #xbox-preview .xp-music-tag-source {
      color: #9A9AA4;
      font-size: 9.5px;
      font-weight: 800;
      letter-spacing: 0.06em;
    }
    #xbox-preview .xp-music-spectrum {
      display: inline-flex;
      align-items: flex-end;
      gap: 3px;
      height: 13px;
      margin-left: 4px;
    }
    #xbox-preview .xp-music-spectrum i {
      width: 3px;
      height: 4px;
      background: var(--xp-pink);
      border-radius: 1px;
      animation: xpSpectrum 0.8s ease-in-out infinite alternate;
    }
    #xbox-preview .xp-music-spectrum i:nth-child(1) { animation-delay: 0.1s; }
    #xbox-preview .xp-music-spectrum i:nth-child(2) { animation-delay: 0.35s; }
    #xbox-preview .xp-music-spectrum i:nth-child(3) { animation-delay: 0.5s; }
    #xbox-preview .xp-music-spectrum i:nth-child(4) { animation-delay: 0.2s; }
    #xbox-preview .xp-music-spectrum i:nth-child(5) { animation-delay: 0.4s; }
    #xbox-preview .xp-music-spectrum i:nth-child(6) { animation-delay: 0.65s; }
    #xbox-preview .xp-music-spectrum i:nth-child(7) { animation-delay: 0.28s; }
    #xbox-preview .xp-music-spectrum i:nth-child(8) { animation-delay: 0.48s; }

    #xbox-preview .xp-music-hero-title {
      font-size: clamp(22px, 3.2vw, 36px);
      line-height: 1.1;
      font-weight: 900;
      color: #FFFFFF;
      margin: 2px 0 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #xbox-preview .xp-music-hero-meta {
      font-size: clamp(12px, 1.25vw, 15px);
      color: #C0C0C8;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    #xbox-preview .xp-music-hero-meta strong {
      color: #FFF;
      font-weight: 800;
    }
    #xbox-preview .xp-music-hero-meta span {
      color: var(--xp-pink);
      font-weight: 700;
    }

    #xbox-preview .xp-music-scrubber-box {
      margin-top: 4px;
      max-width: 440px;
    }
    #xbox-preview .xp-music-scrubber-bar {
      height: 4px;
      background: rgba(255, 255, 255, 0.16);
      border-radius: 4px;
      overflow: hidden;
      position: relative;
    }
    #xbox-preview .xp-music-scrubber-fill {
      height: 100%;
      background: linear-gradient(90deg, #FF0060, #FF5593);
      box-shadow: 0 0 10px var(--xp-pink-glow);
      transition: width 0.3s linear;
      width: 0%;
    }
    #xbox-preview .xp-music-scrubber-times {
      display: flex;
      justify-content: space-between;
      font-size: 9.5px;
      color: #8E8E96;
      font-weight: 700;
      margin-top: 3px;
    }

    #xbox-preview .xp-music-btn-row {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 6px;
    }
    #xbox-preview .xp-music-sub-btn {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 10.5px;
      font-weight: 800;
      color: #FFF;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    #xbox-preview .xp-music-sub-btn:hover {
      background: rgba(255, 255, 255, 0.18);
      border-color: rgba(255, 255, 255, 0.35);
    }
    #xbox-preview .xp-music-hint-key {
      font-size: 10px;
      color: #8E8E96;
      font-weight: 700;
    }

    /* SQUARE ALBUM ART CARDS FOR MUSIC */
    #xbox-preview .xp-card.xp-music-card {
      flex: 0 0 clamp(118px, 12.5vw, 144px) !important;
      height: clamp(152px, 16vw, 184px) !important;
      background: #12141c !important;
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      border: 1px solid rgba(255, 255, 255, 0.12);
      overflow: hidden;
    }
    #xbox-preview .xp-card.xp-music-card .xp-music-cover-art {
      width: 100%;
      height: clamp(118px, 12.5vw, 144px);
      aspect-ratio: 1 / 1;
      position: relative;
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      border-top-left-radius: 11px;
      border-top-right-radius: 11px;
      overflow: hidden;
      flex-shrink: 0;
    }
    #xbox-preview .xp-card.xp-music-card .xp-music-cover-art::after {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, transparent 65%, rgba(10, 12, 16, 0.7) 100%);
    }
    #xbox-preview .xp-card.xp-music-card:after {
      display: none;
    }
    #xbox-preview .xp-card.xp-music-card .xp-card-copy {
      position: relative;
      bottom: auto;
      left: auto;
      right: auto;
      padding: 5px 8px 6px;
      display: flex;
      flex-direction: column;
      gap: 1px;
      background: #12141c;
      flex-grow: 1;
      justify-content: center;
    }
    #xbox-preview .xp-card.xp-music-card .xp-card-copy strong {
      font-size: 11px;
      font-weight: 800;
      color: #FFFFFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #xbox-preview .xp-card.xp-music-card .xp-card-copy span {
      font-size: 9px;
      color: #9A9AA4;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #xbox-preview .xp-card.xp-music-card .xp-music-dur-tag {
      position: absolute;
      top: 6px;
      right: 6px;
      background: rgba(0, 0, 0, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 4px;
      padding: 1px 4px;
      font-size: 8px;
      font-weight: 800;
      color: #FFF;
      z-index: 2;
    }
"""

content = content.replace("/* SHELF CATEGORY & SORT BAR */", music_ui_css + "\n    /* SHELF CATEGORY & SORT BAR */", 1)

# 3. Update Hero DOM in preview.html to have both default hero and music hero
old_hero_dom = """    <!-- MAIN HERO DISPLAY -->
    <main class="xp-hero" id="xp-hero" aria-live="polite">
      <div class="xp-eyebrow" id="xp-eyebrow">CH 101 · LIVE SHOWS</div>
      <div class="xp-title" id="xp-title">The Wintergreen Sessions</div>
      <div class="xp-subtitle" id="xp-subtitle">Live Broadcast · Ahoy TV</div>
      <div class="xp-description" id="xp-description">Independent culture, live sessions, and stories from the Ahoy community. Select a channel card to tune in.</div>
      <button class="xp-action" id="xp-play">▶ &nbsp; FULLSCREEN &nbsp; [A]</button>
    </main>"""

new_hero_dom = """    <!-- MAIN HERO DISPLAY -->
    <main class="xp-hero" id="xp-hero" aria-live="polite">
      <div class="xp-hero-default" id="xp-hero-default">
        <div class="xp-eyebrow" id="xp-eyebrow">CH 101 · LIVE SHOWS</div>
        <div class="xp-title" id="xp-title">The Wintergreen Sessions</div>
        <div class="xp-subtitle" id="xp-subtitle">Live Broadcast · Ahoy TV</div>
        <div class="xp-description" id="xp-description">Independent culture, live sessions, and stories from the Ahoy community. Select a channel card to tune in.</div>
        <button class="xp-action" id="xp-play">▶ &nbsp; FULLSCREEN &nbsp; [A]</button>
      </div>

      <!-- DEDICATED HI-FI MUSIC & RADIO PLAYER HERO -->
      <div class="xp-hero-music" id="xp-hero-music" style="display: none;">
        <div class="xp-music-hero-left">
          <div class="xp-music-vinyl-wrap">
            <div class="xp-music-sleeve" id="xp-music-sleeve">
              <div class="xp-music-sleeve-inner" id="xp-music-hero-art"></div>
            </div>
            <div class="xp-music-vinyl" id="xp-music-vinyl">
              <div class="xp-vinyl-grooves"></div>
              <div class="xp-vinyl-center" id="xp-vinyl-center"></div>
            </div>
          </div>
        </div>
        <div class="xp-music-hero-right">
          <div class="xp-music-tags-row">
            <span class="xp-music-tag-genre" id="xp-music-hero-genre">INDIE ROCK</span>
            <span class="xp-music-tag-source">● APP.AHOY.OOO</span>
            <div class="xp-music-spectrum" id="xp-music-spectrum">
              <i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>
            </div>
          </div>
          <h1 class="xp-music-hero-title" id="xp-music-hero-title">Song Title</h1>
          <div class="xp-music-hero-meta" id="xp-music-hero-meta">
            <strong id="xp-music-hero-artist">Artist Name</strong>
            <span>·</span>
            <span id="xp-music-hero-album">Album Name</span>
          </div>

          <!-- AUDIO PROGRESS SCRUBBER -->
          <div class="xp-music-scrubber-box">
            <div class="xp-music-scrubber-bar">
              <div class="xp-music-scrubber-fill" id="xp-music-scrubber-fill"></div>
            </div>
            <div class="xp-music-scrubber-times">
              <span id="xp-music-time-cur">0:00</span>
              <span id="xp-music-time-total">3:00</span>
            </div>
          </div>

          <!-- AUDIO CONTROLS -->
          <div class="xp-music-btn-row">
            <button class="xp-action" id="xp-music-play-btn" type="button">
              <span id="xp-music-play-label">▶ &nbsp; PLAY TRACK [A]</span>
            </button>
            <button class="xp-music-sub-btn" type="button" onclick="act('X')">
              <span>★ SAVE TO LIBRARY [X]</span>
            </button>
            <span class="xp-music-hint-key"><kbd>◀ ▶</kbd> Next / Previous Track</span>
          </div>
        </div>
      </div>
    </main>"""

if old_hero_dom in content:
    content = content.replace(old_hero_dom, new_hero_dom, 1)
else:
    print("WARNING: old_hero_dom not found verbatim")

# 4. Update render() for section === 2 (Music) to render square cards and update music hero
old_music_render_target = """            const cardsContainer = document.createElement('div');
            cardsContainer.className = 'xp-cards';
            const items = getActiveItems();
            if (selected >= items.length) selected = 0;

            items.forEach((c, i) => {
              const isCur = i === selected;
              const b = document.createElement('button');
              b.type = 'button';
              b.className = 'xp-card';
              b.setAttribute('aria-current', isCur ? 'true' : 'false');
              if (c.art) b.style.setProperty('--art', c.art);

              const posterUrl = c.thumb || c.poster;
              b.innerHTML = `
                <div class="xp-card-poster" style="background-image: url('${posterUrl}')"></div>
                <span class="xp-card-copy">
                  <small>${c.category || 'MUSIC'}${isCur ? '<span class="xp-mini-eq"><i></i><i></i><i></i></span>' : ''}</small>
                  <strong>${c.title || c.name}</strong>
                  <span>${c.line || c.duration}</span>
                </span>
              `;
              b.addEventListener('click', () => {
                selected = i;
                render();
                tune(false);
              });
              cardsContainer.append(b);
            });
            contentDock.append(cardsContainer);"""

new_music_render_target = """            const cardsContainer = document.createElement('div');
            cardsContainer.className = 'xp-cards';
            const items = getActiveItems();
            if (selected >= items.length) selected = 0;

            items.forEach((c, i) => {
              const isCur = i === selected;
              const b = document.createElement('button');
              b.type = 'button';
              b.className = 'xp-card xp-music-card';
              b.setAttribute('aria-current', isCur ? 'true' : 'false');
              if (c.art) b.style.setProperty('--art', c.art);

              const posterUrl = c.thumb || c.poster;
              b.innerHTML = `
                <div class="xp-music-cover-art" style="background-image: url('${posterUrl}')">
                  <span class="xp-music-dur-tag">${c.duration || '3:00'}</span>
                </div>
                <span class="xp-card-copy">
                  <strong>${c.name || c.title}${isCur ? '<span class="xp-mini-eq"><i></i><i></i><i></i></span>' : ''}</strong>
                  <span>${c.artist || c.name}</span>
                </span>
              `;
              b.addEventListener('click', () => {
                selected = i;
                render();
                tune(false);
              });
              cardsContainer.append(b);
            });
            contentDock.append(cardsContainer);"""

if old_music_render_target in content:
    content = content.replace(old_music_render_target, new_music_render_target, 1)
else:
    print("WARNING: old_music_render_target not found")

# 5. Update hero updating logic in render() to toggle default vs music hero
old_hero_update = """          if (curItem && curItem.title) {
            root.querySelector('#xp-eyebrow').textContent = `${curItem.badge || 'AHOY'} · ${(curItem.badge || curItem.title || '').toUpperCase()}`;
            root.querySelector('#xp-title').textContent = curItem.title;
            root.querySelector('#xp-subtitle').textContent = curItem.sub || '';
            root.querySelector('#xp-description').textContent = curItem.description || '';
            root.querySelector('#xp-shelf-status').textContent = `${curItem.badge || 'OD'} TUNED`;
            root.querySelector('#xp-picture').style.background = `radial-gradient(ellipse at 69% 35%, ${curItem.hero || '#ff0060'} 0%, #241f24 38%, #08090c 82%)`;
            root.querySelector('#xp-shelf-label').textContent = `${sections[section]} • AHOY LIBRARY`;
          }"""

new_hero_update = """          const defaultHero = root.querySelector('#xp-hero-default');
          const musicHero = root.querySelector('#xp-hero-music');

          if (section === 2) {
            // MUSIC SECTION HERO
            if (defaultHero) defaultHero.style.display = 'none';
            if (musicHero) musicHero.style.display = 'flex';

            const track = curItem || {};
            const heroArt = root.querySelector('#xp-music-hero-art');
            const vinylCenter = root.querySelector('#xp-vinyl-center');
            const genreBadge = root.querySelector('#xp-music-hero-genre');
            const musicTitle = root.querySelector('#xp-music-hero-title');
            const musicArtist = root.querySelector('#xp-music-hero-artist');
            const musicAlbum = root.querySelector('#xp-music-hero-album');
            const timeTotal = root.querySelector('#xp-music-time-total');
            const playLabel = root.querySelector('#xp-music-play-label');
            const vinylDisc = root.querySelector('#xp-music-vinyl');

            const posterImg = track.poster || track.thumb || 'https://app.ahoy.ooo/static/img/ahoy_logo.png';
            if (heroArt) heroArt.style.backgroundImage = `url("${posterImg}")`;
            if (vinylCenter) vinylCenter.style.backgroundImage = `url("${posterImg}")`;
            if (genreBadge) genreBadge.textContent = track.category || 'INDIE';
            if (musicTitle) musicTitle.textContent = track.title ? track.title.replace(/^[^-]+—\s*/, '') : (track.name || 'Song');
            if (musicArtist) musicArtist.textContent = track.artist || track.name || 'Ahoy Artist';
            if (musicAlbum) musicAlbum.textContent = track.album ? `Album: ${track.album}` : 'Single Release';
            if (timeTotal) timeTotal.textContent = track.duration || '3:00';

            const video = root.querySelector('#xp-hero-video');
            const isPlaying = video && !video.paused;
            if (playLabel) playLabel.textContent = isPlaying ? '❚❚  PAUSE TRACK [A]' : '▶  PLAY TRACK [A]';
            if (vinylDisc) vinylDisc.classList.toggle('playing', isPlaying);

            root.querySelector('#xp-shelf-status').textContent = `MUSIC • ${track.category || 'INDIE'}`;
            root.querySelector('#xp-shelf-label').textContent = `AHOY MUSIC CATALOG (${mediaSections[2].length} TRACKS)`;
          } else {
            // DEFAULT VIDEO HERO (LIVE TV & ON DEMAND & RADIO)
            if (defaultHero) defaultHero.style.display = 'block';
            if (musicHero) musicHero.style.display = 'none';

            if (curItem && curItem.title) {
              root.querySelector('#xp-eyebrow').textContent = `${curItem.badge || 'AHOY'} · ${(curItem.badge || curItem.title || '').toUpperCase()}`;
              root.querySelector('#xp-title').textContent = curItem.title;
              root.querySelector('#xp-subtitle').textContent = curItem.sub || '';
              root.querySelector('#xp-description').textContent = curItem.description || '';
              root.querySelector('#xp-shelf-status').textContent = `${curItem.badge || 'OD'} TUNED`;
              root.querySelector('#xp-picture').style.background = `radial-gradient(ellipse at 69% 35%, ${curItem.hero || '#ff0060'} 0%, #241f24 38%, #08090c 82%)`;
              root.querySelector('#xp-shelf-label').textContent = `${sections[section]} • AHOY LIBRARY`;
            }
          }"""

if old_hero_update in content:
    content = content.replace(old_hero_update, new_hero_update, 1)
else:
    print("WARNING: old_hero_update not found")

# 6. Add audio progress scrubber sync with video.currentTime
timeupdate_handler = """
      const heroVideo = root.querySelector('#xp-hero-video');
      if (heroVideo) {
        heroVideo.addEventListener('timeupdate', () => {
          if (section === 2) {
            const cur = heroVideo.currentTime || 0;
            const dur = heroVideo.duration || 180;
            const pct = dur > 0 ? Math.min(100, (cur / dur) * 100) : 0;
            const fill = root.querySelector('#xp-music-scrubber-fill');
            if (fill) fill.style.width = `${pct}%`;
            const curSpan = root.querySelector('#xp-music-time-cur');
            if (curSpan) {
              const m = Math.floor(cur / 60);
              const s = Math.floor(cur % 60);
              curSpan.textContent = `${m}:${String(s).padStart(2, '0')}`;
            }
          }
        });
      }
"""

content = content.replace("      root.querySelector('#xp-play').addEventListener('click', () => {", timeupdate_handler + "\n      root.querySelector('#xp-play').addEventListener('click', () => {", 1)

# Add click event for #xp-music-play-btn
play_btn_handler = """      const musicPlayBtn = root.querySelector('#xp-music-play-btn');
      if (musicPlayBtn) {
        musicPlayBtn.addEventListener('click', () => {
          const video = root.querySelector('#xp-hero-video');
          if (video) {
            if (video.paused) {
              video.play().catch(() => {});
              say('Playing audio [A]');
            } else {
              video.pause();
              say('Audio paused [A]');
            }
            render();
          }
        });
      }
"""
content = content.replace("      root.querySelector('#xp-play').addEventListener('click', () => {", play_btn_handler + "\n      root.querySelector('#xp-play').addEventListener('click', () => {", 1)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('/Users/agworkywork/ahoy-on-xbox/docs/xbox-ui-preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Improved Music UI installed in preview.html and xbox-ui-preview.html!")
