#!/usr/bin/env python3
import json
import re

with open('/tmp/ahoy_music_catalog.json', 'r', encoding='utf-8') as f:
    music_items = json.load(f)

with open('/tmp/ahoy_radio_catalog.json', 'r', encoding='utf-8') as f:
    radio_items = json.load(f)

music_js_str = json.dumps(music_items, indent=10)
radio_js_str = json.dumps(radio_items, indent=10)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace mediaSections[2] and mediaSections[3]
ms2_pattern = r'2:\s*\[[\s\S]*?\n        \],'
ms3_pattern = r'3:\s*\[[\s\S]*?\n        \]'

m2 = re.search(ms2_pattern, content)
if not m2:
    print("ERROR: could not find mediaSections[2]")
    exit(1)
content = content[:m2.start()] + f'2: {music_js_str},' + content[m2.end():]

m3 = re.search(ms3_pattern, content)
if not m3:
    print("ERROR: could not find mediaSections[3]")
    exit(1)
content = content[:m3.start()] + f'3: {radio_js_str}' + content[m3.end():]

# 2. Add dynamic fetch sync function and call it at initialization
sync_func_code = """      // LIVE SYNCHRONIZATION WITH APP.AHOY.OOO
      async function syncFromAhoyApp() {
        try {
          const resMusic = await fetch('https://app.ahoy.ooo/api/music');
          if (resMusic.ok) {
            const data = await resMusic.json();
            if (data.tracks && data.tracks.length > 0) {
              mediaSections[2] = data.tracks.map((t, i) => {
                const d = t.duration_seconds || 180;
                const m = Math.floor(d / 60);
                const s = d % 60;
                const dur = `${m}:${String(s).padStart(2, '0')}`;
                const cover = t.cover_art || t.background_image || 'https://app.ahoy.ooo/static/img/ahoy_logo.png';
                const artist = t.artist || 'Ahoy Artist';
                const title = t.title || 'Track';
                const genre = t.genre || 'Indie';
                return {
                  id: t.id || `track-${i+1}`,
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
                  isMusic: true
                };
              });
              if (section === 2) render();
            }
          }
        } catch (e) {
          console.log('Ahoy API offline fallback used:', e);
        }

        try {
          const resRadio = await fetch('https://app.ahoy.ooo/api/radio/live');
          if (resRadio.ok) {
            const rData = await resRadio.json();
            const tracks = rData.items || rData.tracks || [];
            const curItem = rData.current_item || rData.current || (tracks.length > 0 ? tracks[0] : null);
            if (curItem && mediaSections[3] && mediaSections[3][0]) {
              mediaSections[3][0].title = `Ahoy Radio — ${curItem.artist || ''} - ${curItem.title || ''}`;
              mediaSections[3][0].sub = `Live 24/7 Stream · Synchronized Station · ${tracks.length} Tracks in Rotation`;
              if (curItem.audio_url) mediaSections[3][0].url = curItem.audio_url;
              if (curItem.cover_art) {
                mediaSections[3][0].poster = curItem.cover_art;
                mediaSections[3][0].thumb = curItem.cover_art;
              }
              if (section === 3) render();
            }
          }
        } catch (e) {
          console.log('Ahoy Radio API offline fallback used:', e);
        }
      }
"""

content = content.replace("      function getCategoryRows() {", sync_func_code + "\n      function getCategoryRows() {", 1)

# Add syncFromAhoyApp() call at initialization right before render()
content = content.replace("      render();\n      updateClock();", "      syncFromAhoyApp();\n      render();\n      updateClock();", 1)

# 3. Update getActiveItems() for section === 2 (Music) to support genre filtering & sorting
old_active_items = """      function getActiveItems() {
        if (section === 0) return liveChannels;
        let items = mediaSections[section] || [];
        if (section === 1) {
          if (activeCategory && activeCategory !== 'ALL') {
            items = items.filter(it => it.category === activeCategory);
          }
          if (activeSort === 'az') {
            items = [...items].sort((a, b) => (a.title || a.name || '').localeCompare(b.title || b.name || ''));
          } else if (activeSort === 'duration-desc') {
            items = [...items].sort((a, b) => (b.durationSec || 0) - (a.durationSec || 0));
          } else if (activeSort === 'duration-asc') {
            items = [...items].sort((a, b) => (a.durationSec || 0) - (b.durationSec || 0));
          }
        }
        return items;
      }"""

new_active_items = """      function getActiveItems() {
        if (section === 0) return liveChannels;
        let items = mediaSections[section] || [];
        if (section === 1 || section === 2) {
          if (activeCategory && activeCategory !== 'ALL') {
            items = items.filter(it => it.category === activeCategory);
          }
          if (activeSort === 'az') {
            items = [...items].sort((a, b) => (a.title || a.name || '').localeCompare(b.title || b.name || ''));
          } else if (activeSort === 'duration-desc') {
            items = [...items].sort((a, b) => (b.durationSec || 0) - (a.durationSec || 0));
          } else if (activeSort === 'duration-asc') {
            items = [...items].sort((a, b) => (a.durationSec || 0) - (b.durationSec || 0));
          }
        }
        return items;
      }"""

content = content.replace(old_active_items, new_active_items, 1)

# 4. Enhance Music shelf in render() to show genre chips & title count from app.ahoy.ooo
old_music_shelf = """          } else {
            // MUSIC & RADIO SECTIONS
            const cardsContainer = document.createElement('div');
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
              const hasPhoto = Boolean(posterUrl);

              b.innerHTML = `
                ${hasPhoto ? `<div class="xp-card-poster" style="background-image: url('${posterUrl}')"></div>` : `<span class="xp-glyph" aria-hidden="true">${c.glyph || '▶'}</span>`}
                <span class="xp-card-copy">
                  <small>${c.category || c.no}${isCur ? '<span class="xp-mini-eq"><i></i><i></i><i></i></span>' : ''}</small>
                  <strong>${c.title || c.name}</strong>
                  <span>${c.line || c.duration || c.name}</span>
                </span>
              `;
              b.addEventListener('click', () => {
                selected = i;
                render();
                tune(false);
              });
              cardsContainer.append(b);
            });
            contentDock.append(cardsContainer);

            const activeCard = cardsContainer.querySelector('.xp-card[aria-current="true"]');
            if (activeCard) {
              setTimeout(() => {
                activeCard.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
              }, 30);
            }

            const hints = root.querySelector('#xp-hints');
            if (hints) {
              hints.innerHTML = `
                <span><kbd>◀ ▶</kbd> Browse (${items.length})</span>
                <span><kbd class="xp-hint-a">A</kbd> Play</span>
                <span><kbd class="xp-hint-b">B</kbd> Close Guide</span>
              `;
            }
          }"""

new_music_shelf = """          } else if (section === 2) {
            // MUSIC SECTION (DIRECT APP.AHOY.OOO CATALOG)
            const filtersBar = document.createElement('div');
            filtersBar.className = 'xp-shelf-filters';

            const chipsBox = document.createElement('div');
            chipsBox.className = 'xp-filter-chips';

            const musicGenres = ['ALL', 'Indie Rock', 'Alternative Rock', 'Indie Pop', 'Indie'];
            musicGenres.forEach(genre => {
              const count = genre === 'ALL' ? mediaSections[2].length : mediaSections[2].filter(x => x.category === genre).length;
              if (count === 0 && genre !== 'ALL') return;
              const chip = document.createElement('button');
              chip.type = 'button';
              chip.className = 'xp-filter-chip';
              chip.setAttribute('aria-selected', activeCategory === genre ? 'true' : 'false');
              chip.textContent = `${genre} (${count})`;
              chip.addEventListener('click', () => {
                playXboxSound('tick');
                activeCategory = genre;
                selected = 0;
                render();
                tune(false);
              });
              chipsBox.append(chip);
            });
            filtersBar.append(chipsBox);

            const sortBox = document.createElement('div');
            sortBox.className = 'xp-sort-box';
            sortBox.innerHTML = `
              <span style="color:#ff0060;font-weight:900;">APP.AHOY.OOO</span>
              <span>SORT:</span>
              <select class="xp-sort-select" aria-label="Sort music">
                <option value="curated"${activeSort === 'curated' ? ' selected' : ''}>Curated</option>
                <option value="az"${activeSort === 'az' ? ' selected' : ''}>A–Z (Artist)</option>
                <option value="duration-desc"${activeSort === 'duration-desc' ? ' selected' : ''}>Longest</option>
                <option value="duration-asc"${activeSort === 'duration-asc' ? ' selected' : ''}>Shortest</option>
              </select>
            `;
            sortBox.querySelector('select').addEventListener('change', (e) => {
              playXboxSound('tick');
              activeSort = e.target.value;
              selected = 0;
              render();
              tune(false);
            });
            filtersBar.append(sortBox);
            contentDock.append(filtersBar);

            const cardsContainer = document.createElement('div');
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
            contentDock.append(cardsContainer);

            const activeCard = cardsContainer.querySelector('.xp-card[aria-current="true"]');
            if (activeCard) {
              setTimeout(() => {
                activeCard.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
              }, 30);
            }

            const hints = root.querySelector('#xp-hints');
            if (hints) {
              hints.innerHTML = `
                <span><kbd>◀ ▶</kbd> Browse Music (${items.length} Tracks)</span>
                <span><kbd class="xp-hint-a">A</kbd> Play Audio</span>
                <span><kbd class="xp-hint-b">B</kbd> Close Guide</span>
              `;
            }
          } else {
            // RADIO SECTION (LIVE FROM APP.AHOY.OOO)
            const filtersBar = document.createElement('div');
            filtersBar.className = 'xp-shelf-filters';
            filtersBar.innerHTML = `
              <div class="xp-filter-chips">
                <span class="xp-filter-chip" aria-selected="true">● 24/7 LIVE BROADCASTS (APP.AHOY.OOO)</span>
                <span class="xp-filter-chip" aria-selected="false">86 ROTATING TRACKS</span>
              </div>
              <div class="xp-sort-box">
                <span style="color:#00a2ff;font-weight:900;">AHOY RADIO STATION</span>
              </div>
            `;
            contentDock.append(filtersBar);

            const cardsContainer = document.createElement('div');
            cardsContainer.className = 'xp-cards';
            const items = mediaSections[3] || [];
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
                  <small>${c.category || 'RADIO'}${isCur ? '<span class="xp-mini-eq"><i></i><i></i><i></i></span>' : ''}</small>
                  <strong>${c.name}</strong>
                  <span>${c.line || c.title}</span>
                </span>
              `;
              b.addEventListener('click', () => {
                selected = i;
                render();
                tune(false);
              });
              cardsContainer.append(b);
            });
            contentDock.append(cardsContainer);

            const activeCard = cardsContainer.querySelector('.xp-card[aria-current="true"]');
            if (activeCard) {
              setTimeout(() => {
                activeCard.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
              }, 30);
            }

            const hints = root.querySelector('#xp-hints');
            if (hints) {
              hints.innerHTML = `
                <span><kbd>◀ ▶</kbd> Select Station</span>
                <span><kbd class="xp-hint-a">A</kbd> Tune Live Stream</span>
                <span><kbd class="xp-hint-b">B</kbd> Close Guide</span>
              `;
            }
          }"""

if old_music_shelf in content:
    content = content.replace(old_music_shelf, new_music_shelf, 1)
else:
    print("ERROR: old_music_shelf not found")
    exit(1)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('/Users/agworkywork/ahoy-on-xbox/docs/xbox-ui-preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Music (86 tracks) and Radio (live station) wired directly to app.ahoy.ooo!")
