#!/usr/bin/env python3
import re

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .xp-hero to width: min(92%, 1180px);
content = content.replace("width: min(64%, 740px);", "width: min(92%, 1180px);", 1)

# Add .xp-hero-default width rule
hero_default_css = """    #xbox-preview .xp-hero-default {
      width: min(64%, 740px);
    }"""
content = content.replace("/* HERO STAGE */", "/* HERO STAGE */\n" + hero_default_css, 1)

# 2. Tone down the loud neon red in tabs, chips, and buttons:
old_tab_selected = """    #xbox-preview .xp-tab[aria-selected="true"] {
      background: var(--xp-pink);
      color: #FFFFFF;
      box-shadow: 0 0 16px var(--xp-pink-glow);
    }"""

new_tab_selected = """    #xbox-preview .xp-tab[aria-selected="true"] {
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.28);
      color: #FFFFFF;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
      position: relative;
    }
    #xbox-preview .xp-tab[aria-selected="true"]::after {
      content: "";
      position: absolute;
      bottom: -6px;
      left: 18%;
      right: 18%;
      height: 2px;
      background: var(--xp-pink);
      border-radius: 2px;
      box-shadow: 0 0 8px var(--xp-pink-glow);
    }"""

if old_tab_selected in content:
    content = content.replace(old_tab_selected, new_tab_selected, 1)

# Tone down active filter chip from harsh red to frosted glass
old_chip_selected = """    #xbox-preview .xp-filter-chip[aria-selected=true] {
      background: var(--xp-pink);
      border-color: var(--xp-pink);
      color: #FFFFFF;
      box-shadow: 0 0 12px var(--xp-pink-glow);
    }"""

new_chip_selected = """    #xbox-preview .xp-filter-chip[aria-selected=true] {
      background: rgba(255, 255, 255, 0.16);
      border-color: rgba(255, 255, 255, 0.35);
      color: #FFFFFF;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }"""

if old_chip_selected in content:
    content = content.replace(old_chip_selected, new_chip_selected, 1)

# Tone down Music Action buttons to liquid glass:
music_btn_css = """
    /* CALM LIQUID GLASS MUSIC BUTTONS */
    #xbox-preview .xp-music-btn-row .xp-action {
      background: rgba(255, 255, 255, 0.12) !important;
      border: 1px solid rgba(255, 255, 255, 0.24) !important;
      color: #FFFFFF !important;
      backdrop-filter: blur(12px) !important;
      -webkit-backdrop-filter: blur(12px) !important;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
      transition: all 0.2s ease !important;
    }
    #xbox-preview .xp-music-btn-row .xp-action:hover {
      background: rgba(255, 255, 255, 0.2) !important;
      border-color: rgba(255, 255, 255, 0.38) !important;
      transform: translateY(-1px) !important;
    }
    #xbox-preview .xp-music-tag-genre {
      background: rgba(255, 255, 255, 0.08) !important;
      border: 1px solid rgba(255, 255, 255, 0.18) !important;
      color: #D8D8E0 !important;
    }
    #xbox-preview .xp-music-hero-meta span {
      color: #8E8E98 !important;
      font-weight: 600 !important;
    }

    /* RIGHT QUEUE CARD */
    #xbox-preview .xp-music-queue-card {
      background: rgba(16, 18, 24, 0.68);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      padding: 10px 14px;
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      width: clamp(230px, 25vw, 295px);
      display: flex;
      flex-direction: column;
      gap: 6px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
      margin-left: auto;
      flex-shrink: 0;
    }
    #xbox-preview .xp-queue-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 8.5px;
      font-weight: 800;
      letter-spacing: 0.08em;
      color: #9A9AA6;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 5px;
    }
    #xbox-preview .xp-queue-header small {
      color: #7E7E88;
    }
    #xbox-preview .xp-queue-row {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 4px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.15s ease;
    }
    #xbox-preview .xp-queue-row:hover {
      background: rgba(255, 255, 255, 0.08);
    }
    #xbox-preview .xp-queue-thumb {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      background-size: cover;
      background-position: center;
      flex-shrink: 0;
    }
    #xbox-preview .xp-queue-info {
      display: flex;
      flex-direction: column;
      min-width: 0;
      flex: 1 1 auto;
    }
    #xbox-preview .xp-queue-title {
      font-size: 10px;
      font-weight: 800;
      color: #FFFFFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #xbox-preview .xp-queue-artist {
      font-size: 8.5px;
      color: #8E8E98;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #xbox-preview .xp-queue-dur {
      font-size: 8.5px;
      color: #7E7E88;
      font-weight: 700;
      flex-shrink: 0;
    }
"""

content = content.replace("/* DEDICATED HI-FI MUSIC HERO EXPERIENCE */", music_btn_css + "\n    /* DEDICATED HI-FI MUSIC HERO EXPERIENCE */", 1)

# 3. Fix the UP NEXT pill styling (no wrap, max-width, clean padding)
old_up_next_css = """    #xbox-preview .xp-music-up-next {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 999px;
      padding: 3px 10px;
      font-size: 9.5px;
      color: #C0C0C8;
      cursor: pointer;
      transition: all 0.15s ease;
      margin-left: 6px;
    }"""

new_up_next_css = """    #xbox-preview .xp-music-up-next {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 999px;
      padding: 5px 12px;
      font-size: 9.5px;
      color: #C0C0C8;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
      flex-shrink: 0;
      max-width: 260px;
      overflow: hidden;
    }"""

if old_up_next_css in content:
    content = content.replace(old_up_next_css, new_up_next_css, 1)

# 4. Fix scrubber times alignment
old_scrubber_times_css = """    #xbox-preview .xp-music-scrubber-times {
      display: flex;
      justify-content: space-between;
      font-size: 9.5px;
      color: #8E8E96;
      font-weight: 700;
      margin-top: 3px;
    }"""

new_scrubber_times_css = """    #xbox-preview .xp-music-scrubber-times {
      display: flex !important;
      justify-content: space-between !important;
      width: 100% !important;
      font-size: 9.5px;
      color: #8E8E96;
      font-weight: 700;
      margin-top: 4px;
    }
    #xbox-preview .xp-music-scrubber-box {
      width: 100% !important;
      max-width: 440px !important;
    }"""

if old_scrubber_times_css in content:
    content = content.replace(old_scrubber_times_css, new_scrubber_times_css, 1)

# 5. Add Queue card to #xp-hero-music DOM
old_hero_music_dom = """        <div class="xp-music-hero-right">
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
            <div class="xp-music-scrubber-bar" id="xp-music-scrubber-bar" title="Click timeline to seek">
              <div class="xp-music-scrubber-fill" id="xp-music-scrubber-fill">
                <div class="xp-music-scrubber-thumb"></div>
              </div>
            </div>
            <div class="xp-music-scrubber-times">
              <span id="xp-music-time-cur">0:00</span>
              <span id="xp-music-time-total">3:00</span>
            </div>
          </div>

          <!-- AUDIO CONTROLS & UP NEXT -->
          <div class="xp-music-btn-row">
            <button class="xp-action" id="xp-music-play-btn" type="button">
              <span id="xp-music-play-label">▶ &nbsp; PLAY TRACK [A]</span>
            </button>
            <button class="xp-music-sub-btn" type="button" onclick="act('X')">
              <span>★ SAVE TO LIBRARY [X]</span>
            </button>
            <div class="xp-music-up-next" id="xp-music-up-next" onclick="act('ArrowRight')">
              <span class="xp-up-next-label">UP NEXT:</span>
              <span class="xp-up-next-song" id="xp-up-next-song">Song</span>
              <span class="xp-up-next-artist" id="xp-up-next-artist">Artist</span>
            </div>
          </div>
        </div>
      </div>"""

new_hero_music_dom = """        <div class="xp-music-hero-right">
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
            <div class="xp-music-scrubber-bar" id="xp-music-scrubber-bar" title="Click timeline to seek">
              <div class="xp-music-scrubber-fill" id="xp-music-scrubber-fill">
                <div class="xp-music-scrubber-thumb"></div>
              </div>
            </div>
            <div class="xp-music-scrubber-times">
              <span id="xp-music-time-cur">0:00</span>
              <span id="xp-music-time-total">3:00</span>
            </div>
          </div>

          <!-- AUDIO CONTROLS & UP NEXT -->
          <div class="xp-music-btn-row">
            <button class="xp-action" id="xp-music-play-btn" type="button">
              <span id="xp-music-play-label">▶ &nbsp; PLAY TRACK [A]</span>
            </button>
            <button class="xp-music-sub-btn" type="button" onclick="act('X')">
              <span>★ SAVE TO LIBRARY [X]</span>
            </button>
            <div class="xp-music-up-next" id="xp-music-up-next" onclick="act('ArrowRight')">
              <span class="xp-up-next-label">⏭ UP NEXT:</span>
              <span class="xp-up-next-song" id="xp-up-next-song">Song</span>
              <span class="xp-up-next-artist" id="xp-up-next-artist">Artist</span>
            </div>
          </div>
        </div>

        <!-- RIGHT SIDE: UPCOMING QUEUE PANEL -->
        <div class="xp-music-queue-card" id="xp-music-queue-card">
          <div class="xp-queue-header">
            <span>UPCOMING QUEUE</span>
            <small>APP.AHOY.OOO</small>
          </div>
          <div class="xp-queue-items" id="xp-queue-items"></div>
        </div>
      </div>"""

if old_hero_music_dom in content:
    content = content.replace(old_hero_music_dom, new_hero_music_dom, 1)

# 6. Update render() to populate the upcoming queue items dynamically
queue_render_code = """
            // Render upcoming 3 tracks in queue card
            const queueItemsContainer = root.querySelector('#xp-queue-items');
            if (queueItemsContainer) {
              queueItemsContainer.innerHTML = '';
              for (let q = 1; q <= 3; q++) {
                const qIdx = (selected + q) % musicList.length;
                const qTrack = musicList[qIdx];
                if (!qTrack) continue;
                const qRow = document.createElement('div');
                qRow.className = 'xp-queue-row';
                const qThumb = qTrack.poster || qTrack.thumb || 'https://app.ahoy.ooo/static/img/ahoy_logo.png';
                const qSong = qTrack.trackTitle || (qTrack.title ? qTrack.title.replace(/^[^—-]+[—-]\s*/, '') : qTrack.name);
                qRow.innerHTML = `
                  <div class="xp-queue-thumb" style="background-image: url('${qThumb}')"></div>
                  <div class="xp-queue-info">
                    <span class="xp-queue-title">${qSong}</span>
                    <span class="xp-queue-artist">${qTrack.artist || 'Ahoy'}</span>
                  </div>
                  <span class="xp-queue-dur">${qTrack.duration || '3:00'}</span>
                `;
                qRow.addEventListener('click', () => {
                  selected = qIdx;
                  render();
                  tune(false);
                });
                queueItemsContainer.append(qRow);
              }
            }
"""

content = content.replace("            if (upNextArtist) upNextArtist.textContent = `· ${nextArtist}`;", "            if (upNextArtist) upNextArtist.textContent = `· ${nextArtist}`;\n" + queue_render_code, 1)

# 7. Tone down the right shelf status "MUSIC · INDIE" from red to neutral
content = content.replace("root.querySelector('#xp-shelf-status').textContent = `MUSIC • ${track.category || 'INDIE'}`;", "root.querySelector('#xp-shelf-status').textContent = `${track.category ? track.category.toUpperCase() : 'INDIE'} · AHOY CATALOG`;", 1)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('/Users/agworkywork/ahoy-on-xbox/docs/xbox-ui-preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Calmed red accents, fixed UP NEXT pill, and filled right side with Queue panel!")
