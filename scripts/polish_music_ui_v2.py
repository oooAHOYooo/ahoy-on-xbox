#!/usr/bin/env python3
import json
import re

with open('/tmp/ahoy_music_catalog_v2.json', 'r', encoding='utf-8') as f:
    music_items = json.load(f)

music_js_str = json.dumps(music_items, indent=10)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update mediaSections[2] with enriched tracks containing explicit trackTitle & artist
ms2_pattern = r'2:\s*\[[\s\S]*?\n\],(?=\s*3:)'
m2 = re.search(ms2_pattern, content)
if not m2:
    print("ERROR: could not find mediaSections[2]")
    exit(1)
content = content[:m2.start()] + f'2: {music_js_str},' + content[m2.end():]

# 2. Add Ambilight and enhanced Music CSS
css_marker = "/* DEDICATED HI-FI MUSIC HERO EXPERIENCE */"
new_css = """    /* AMBILIGHT DYNAMIC AMBIENT BACKDROP */
    #xbox-preview .xp-video-backdrop.ambilight {
      filter: blur(54px) saturate(2.0) brightness(0.42) !important;
      transform: scale(1.18);
    }

    /* DEDICATED HI-FI MUSIC HERO EXPERIENCE */"""

content = content.replace(css_marker, new_css, 1)

# Update Scrubber & Up Next CSS
scrubber_css_marker = "#xbox-preview .xp-music-scrubber-bar {"
new_scrubber_css = """#xbox-preview .xp-music-scrubber-bar {
      height: 6px;
      background: rgba(255, 255, 255, 0.16);
      border-radius: 6px;
      position: relative;
      cursor: pointer;
      overflow: visible;
      transition: height 0.15s ease;
    }
    #xbox-preview .xp-music-scrubber-bar:hover {
      height: 8px;
    }
    #xbox-preview .xp-music-scrubber-fill {
      height: 100%;
      background: linear-gradient(90deg, #FF0060, #FF5593);
      border-radius: 6px;
      box-shadow: 0 0 10px var(--xp-pink-glow);
      position: relative;
      width: 0%;
      pointer-events: none;
    }
    #xbox-preview .xp-music-scrubber-thumb {
      position: absolute;
      right: -5px;
      top: 50%;
      transform: translateY(-50%);
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #FFFFFF;
      box-shadow: 0 0 10px #FF0060, 0 0 4px #FFF;
      opacity: 1;
      transition: transform 0.15s ease;
    }
    #xbox-preview .xp-music-up-next {
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
    }
    #xbox-preview .xp-music-up-next:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
      color: #FFF;
    }
    #xbox-preview .xp-up-next-label {
      color: var(--xp-pink);
      font-weight: 900;
      letter-spacing: 0.08em;
      font-size: 8.5px;
    }
    #xbox-preview .xp-up-next-song {
      font-weight: 800;
      color: #FFFFFF;
    }
    #xbox-preview .xp-up-next-artist {
      color: #9A9AA4;
    }

    #xbox-preview .xp-music-cover-art {
      box-shadow: inset 0 0 14px rgba(0, 0, 0, 0.65);
    }
"""

content = re.sub(
    r'#xbox-preview \.xp-music-scrubber-bar \{[\s\S]*?#xbox-preview \.xp-music-btn-row \{',
    new_scrubber_css + "\n    #xbox-preview .xp-music-btn-row {",
    content,
    count=1
)

# 3. Update syncFromAhoyApp in preview.html to store trackTitle and artist cleanly
old_sync_code = """                  id: t.id || `track-${i+1}`,
                  no: `MU-${String(i+1).padStart(2, '0')}`,
                  name: artist,
                  artist: artist,
                  album: t.album || 'Single',
                  title: `${artist} — ${title}`,
                  line: `${genre} · ${dur}`,
                  sub: `${artist} · ${t.album || 'Single'} · ${genre}`,
                  description: `Streaming directly from app.ahoy.ooo music catalog.`,
                  category: genre,
                  duration: dur,
                  durationSec: d,
                  poster: cover,
                  thumb: cover,
                  url: t.audio_url || t.preview_url,
                  hero: '#ff0060',
                  glyph: '♪',
                  isMusic: true"""

new_sync_code = """                  id: t.id || `track-${i+1}`,
                  no: `MU-${String(i+1).padStart(2, '0')}`,
                  name: title,
                  trackTitle: title,
                  artist: artist,
                  album: t.album || 'Single',
                  title: `${artist} — ${title}`,
                  line: `${genre} · ${dur}`,
                  sub: `${artist} · ${t.album || 'Single'} · ${genre}`,
                  description: `Streaming directly from app.ahoy.ooo music catalog.`,
                  category: genre,
                  duration: dur,
                  durationSec: d,
                  poster: cover,
                  thumb: cover,
                  url: t.audio_url || t.preview_url,
                  hero: '#ff0060',
                  glyph: '♪',
                  isMusic: true"""

if old_sync_code in content:
    content = content.replace(old_sync_code, new_sync_code, 1)

# 4. Update the Music Hero HTML DOM to include scrubber thumb and Up Next
old_scrubber_dom = """          <!-- AUDIO PROGRESS SCRUBBER -->
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
          </div>"""

new_scrubber_dom = """          <!-- AUDIO PROGRESS SCRUBBER -->
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
          </div>"""

if old_scrubber_dom in content:
    content = content.replace(old_scrubber_dom, new_scrubber_dom, 1)

# 5. Update Card Rendering in Music section:
old_card_copy = """              b.innerHTML = `
                <div class="xp-music-cover-art" style="background-image: url('${posterUrl}')">
                  <span class="xp-music-dur-tag">${c.duration || '3:00'}</span>
                </div>
                <span class="xp-card-copy">
                  <strong>${c.name || c.title}${isCur ? '<span class="xp-mini-eq"><i></i><i></i><i></i></span>' : ''}</strong>
                  <span>${c.artist || c.name}</span>
                </span>
              `;"""

new_card_copy = """              const trackSongTitle = c.trackTitle || (c.title ? c.title.replace(/^[^—-]+[—-]\s*/, '') : c.name);
              const trackArtistName = c.artist || c.name;
              b.innerHTML = `
                <div class="xp-music-cover-art" style="background-image: url('${posterUrl}')">
                  <span class="xp-music-dur-tag">${c.duration || '3:00'}</span>
                </div>
                <span class="xp-card-copy">
                  <strong>${trackSongTitle}${isCur ? '<span class="xp-mini-eq"><i></i><i></i><i></i></span>' : ''}</strong>
                  <span>${trackArtistName}</span>
                </span>
              `;"""

if old_card_copy in content:
    content = content.replace(old_card_copy, new_card_copy, 1)

# 6. Update Hero render logic for Music to correctly set Title, Artist, Album, and Up Next
old_hero_music_render = """            const track = curItem || {};
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
            if (musicTitle) musicTitle.textContent = track.title ? track.title.replace(/^[^-]+—\\s*/, '') : (track.name || 'Song');
            if (musicArtist) musicArtist.textContent = track.artist || track.name || 'Ahoy Artist';
            if (musicAlbum) musicAlbum.textContent = track.album ? `Album: ${track.album}` : 'Single Release';
            if (timeTotal) timeTotal.textContent = track.duration || '3:00';"""

new_hero_music_render = """            const track = curItem || {};
            const heroArt = root.querySelector('#xp-music-hero-art');
            const vinylCenter = root.querySelector('#xp-vinyl-center');
            const genreBadge = root.querySelector('#xp-music-hero-genre');
            const musicTitle = root.querySelector('#xp-music-hero-title');
            const musicArtist = root.querySelector('#xp-music-hero-artist');
            const musicAlbum = root.querySelector('#xp-music-hero-album');
            const timeTotal = root.querySelector('#xp-music-time-total');
            const playLabel = root.querySelector('#xp-music-play-label');
            const vinylDisc = root.querySelector('#xp-music-vinyl');
            const upNextSong = root.querySelector('#xp-up-next-song');
            const upNextArtist = root.querySelector('#xp-up-next-artist');

            const songTitle = track.trackTitle || (track.title ? track.title.replace(/^[^—-]+[—-]\s*/, '') : (track.name || 'Song'));
            const artistName = track.artist || (track.title && track.title.includes('—') ? track.title.split('—')[0].trim() : (track.name || 'Samuel Dylan Witch'));
            const albumName = (track.album && track.album !== 'Single') ? `Album: ${track.album}` : 'Single Release';

            const posterImg = track.poster || track.thumb || 'https://app.ahoy.ooo/static/img/ahoy_logo.png';
            if (heroArt) heroArt.style.backgroundImage = `url("${posterImg}")`;
            if (vinylCenter) vinylCenter.style.backgroundImage = `url("${posterImg}")`;
            if (genreBadge) genreBadge.textContent = track.category || 'INDIE';
            if (musicTitle) musicTitle.textContent = songTitle;
            if (musicArtist) musicArtist.textContent = artistName;
            if (musicAlbum) musicAlbum.textContent = albumName;
            if (timeTotal) timeTotal.textContent = track.duration || '3:00';

            // Next Track in Queue preview
            const musicList = getActiveItems();
            const nextIdx = (selected + 1) % musicList.length;
            const nextTrack = musicList[nextIdx] || {};
            const nextSong = nextTrack.trackTitle || (nextTrack.title ? nextTrack.title.replace(/^[^—-]+[—-]\s*/, '') : nextTrack.name);
            const nextArtist = nextTrack.artist || 'Artist';
            if (upNextSong) upNextSong.textContent = nextSong;
            if (upNextArtist) upNextArtist.textContent = `· ${nextArtist}`;"""

if old_hero_music_render in content:
    content = content.replace(old_hero_music_render, new_hero_music_render, 1)

# 7. Update updateVideoPlayback to toggle ambilight class on backdrop
old_playback = """        const video = root.querySelector('#xp-hero-video');
        const backdrop = root.querySelector('#xp-video-backdrop');
        if (backdrop && cur.poster) {
          backdrop.style.backgroundImage = `url("${cur.poster}")`;
        }"""

new_playback = """        const video = root.querySelector('#xp-hero-video');
        const backdrop = root.querySelector('#xp-video-backdrop');
        if (backdrop && cur.poster) {
          backdrop.style.backgroundImage = `url("${cur.poster}")`;
          if (section === 2) {
            backdrop.classList.add('ambilight');
          } else {
            backdrop.classList.remove('ambilight');
          }
        }"""

if old_playback in content:
    content = content.replace(old_playback, new_playback, 1)

# 8. Add click-to-seek handler on #xp-music-scrubber-bar
scrubber_click_handler = """
      const scrubberBar = root.querySelector('#xp-music-scrubber-bar');
      if (scrubberBar) {
        scrubberBar.addEventListener('click', (e) => {
          const rect = scrubberBar.getBoundingClientRect();
          const pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
          const heroVid = root.querySelector('#xp-hero-video');
          if (heroVid && heroVid.duration) {
            heroVid.currentTime = pct * heroVid.duration;
            playXboxSound('tick');
          }
        });
      }
"""

content = content.replace("      const musicPlayBtn = root.querySelector('#xp-music-play-btn');", scrubber_click_handler + "\n      const musicPlayBtn = root.querySelector('#xp-music-play-btn');", 1)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('/Users/agworkywork/ahoy-on-xbox/docs/xbox-ui-preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Polish upgrades applied to preview.html and xbox-ui-preview.html!")
