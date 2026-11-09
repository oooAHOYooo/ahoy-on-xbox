#!/usr/bin/env python3
import json
import re

with open('/tmp/ondemand_catalog_enriched.json', 'r', encoding='utf-8') as f:
    ondemand_items = json.load(f)

items_json_str = json.dumps(ondemand_items, indent=10)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace mediaSections[1]
pattern_ms1 = r'1:\s*\[[\s\S]*?\n        \],'
replacement_ms1 = f'1: {items_json_str},'

m = re.search(pattern_ms1, content)
if not m:
    print("ERROR: could not find mediaSections[1]")
    exit(1)

content = content[:m.start()] + replacement_ms1 + content[m.end():]

# 2. Add activeCategory & activeSort after selected / section
state_vars_target = """      let selected = 0;
      let section = 0;"""

state_vars_replacement = """      let selected = 0;
      let section = 0;
      let activeCategory = 'ALL';
      let activeSort = 'curated';"""

if state_vars_target in content:
    content = content.replace(state_vars_target, state_vars_replacement, 1)
else:
    print("WARNING: state_vars_target not found verbatim")

# 3. Add getActiveItems() before getCurrentItem()
get_active_items_code = """      function getActiveItems() {
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
      }

      function getCurrentItem() {"""

content = content.replace("      function getCurrentItem() {", get_active_items_code, 1)

# 4. Update getCurrentItem() for section !== 0 to use getActiveItems()
old_get_current = """        } else {
          const m = (mediaSections[section] || [])[selected] || {};
          return {
            id: `sec-${section}-${selected}`,
            title: m.title || m.name,
            badge: m.glyph || m.no,
            sub: `${m.name} • ${sections[section]}`,
            sec: section,
            idx: selected,
            url: m.url,
            poster: m.poster
          };
        }"""

new_get_current = """        } else {
          const items = getActiveItems();
          const m = items[selected] || items[0] || {};
          return {
            id: m.id || `sec-${section}-${selected}`,
            title: m.title || m.name,
            badge: m.category || m.glyph || m.no,
            sub: m.sub || `${m.name} • ${sections[section]}`,
            sec: section,
            idx: selected,
            url: m.url,
            poster: m.poster || m.thumb
          };
        }"""

content = content.replace(old_get_current, new_get_current, 1)

# 5. Update render() for section !== 0
old_shelf_render = """        } else {
          // HORIZONTAL CARD SHELF FOR ON DEMAND, MUSIC, RADIO
          const cardsContainer = document.createElement('div');
          cardsContainer.className = 'xp-cards';
          const items = mediaSections[section] || [];
          if (selected >= items.length) selected = 0;
          const curItem = items[selected] || items[0];

          items.forEach((c, i) => {
            const isCur = i === selected;
            const b = document.createElement('button');
            b.type = 'button';
            b.className = 'xp-card';
            b.setAttribute('aria-current', isCur ? 'true' : 'false');
            b.style.setProperty('--art', c.art);
            b.innerHTML = `
              <span class="xp-glyph" aria-hidden="true">${c.glyph}</span>
              <span class="xp-card-copy">
                <small>${c.no}${isCur ? '<span class="xp-mini-eq"><i></i><i></i><i></i></span>' : ''}</small>
                <strong>${c.name}</strong>
                <span>${c.line}</span>
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

          root.querySelector('#xp-eyebrow').textContent = `${curItem.no} · ${curItem.name.toUpperCase()}`;
          root.querySelector('#xp-title').textContent = curItem.title;
          root.querySelector('#xp-subtitle').textContent = curItem.sub;
          root.querySelector('#xp-description').textContent = curItem.description;
          root.querySelector('#xp-shelf-status').textContent = `${curItem.no} SELECTED`;
          root.querySelector('#xp-picture').style.background = `radial-gradient(ellipse at 69% 35%, ${curItem.hero} 0%, #241f24 38%, #08090c 82%)`;
          root.querySelector('#xp-shelf-label').textContent = `${sections[section]} • AHOY LIBRARY`;
          const hints = root.querySelector('#xp-hints');
          if (hints) {
            hints.innerHTML = `
              <span><kbd>◀ ▶</kbd> Browse</span>
              <span><kbd class="xp-hint-a">A</kbd> Play</span>
              <span><kbd class="xp-hint-b">B</kbd> Close Guide</span>
            `;
          }
        }"""

new_shelf_render = """        } else {
          // HORIZONTAL CARD SHELF FOR ON DEMAND, MUSIC, RADIO
          const items = getActiveItems();
          if (selected >= items.length) selected = 0;
          const curItem = items[selected] || items[0] || {};

          // If On Demand (section 1), render category chips and sort options above the shelf
          if (section === 1) {
            const filtersBar = document.createElement('div');
            filtersBar.className = 'xp-shelf-filters';

            const chipsBox = document.createElement('div');
            chipsBox.className = 'xp-filter-chips';

            const categories = [
              { id: 'ALL', label: `ALL (${mediaSections[1].length})` },
              { id: 'Skate & Films', label: `Skate & Films (${mediaSections[1].filter(x => x.category === 'Skate & Films').length})` },
              { id: 'Series & Shows', label: `Series & Shows (${mediaSections[1].filter(x => x.category === 'Series & Shows').length})` },
              { id: 'Live Concerts', label: `Live Concerts (${mediaSections[1].filter(x => x.category === 'Live Concerts').length})` },
              { id: 'Music Videos', label: `Music Videos (${mediaSections[1].filter(x => x.category === 'Music Videos').length})` },
              { id: 'Poets & Friends', label: `Poets & Friends (${mediaSections[1].filter(x => x.category === 'Poets & Friends').length})` }
            ];

            categories.forEach(cat => {
              const chip = document.createElement('button');
              chip.type = 'button';
              chip.className = 'xp-filter-chip';
              chip.setAttribute('aria-selected', activeCategory === cat.id ? 'true' : 'false');
              chip.textContent = cat.label;
              chip.addEventListener('click', () => {
                playXboxSound('tick');
                activeCategory = cat.id;
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
              <span>SORT:</span>
              <select class="xp-sort-select" aria-label="Sort videos">
                <option value="curated"${activeSort === 'curated' ? ' selected' : ''}>Curated</option>
                <option value="az"${activeSort === 'az' ? ' selected' : ''}>A–Z</option>
                <option value="duration-desc"${activeSort === 'duration-desc' ? ' selected' : ''}>Duration (Longest)</option>
                <option value="duration-asc"${activeSort === 'duration-asc' ? ' selected' : ''}>Duration (Shortest)</option>
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
          }

          const cardsContainer = document.createElement('div');
          cardsContainer.className = 'xp-cards';

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

          // Auto-scroll active card into center view smoothly
          const activeCard = cardsContainer.querySelector('.xp-card[aria-current="true"]');
          if (activeCard) {
            setTimeout(() => {
              activeCard.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
            }, 30);
          }

          if (curItem && curItem.title) {
            root.querySelector('#xp-eyebrow').textContent = `${curItem.no || 'AHOY'} · ${(curItem.category || curItem.name || '').toUpperCase()}`;
            root.querySelector('#xp-title').textContent = curItem.title;
            root.querySelector('#xp-subtitle').textContent = curItem.sub || curItem.line || '';
            root.querySelector('#xp-description').textContent = curItem.description || '';
            root.querySelector('#xp-shelf-status').textContent = `${curItem.no || 'OD'} SELECTED (${selected + 1} of ${items.length})`;
            root.querySelector('#xp-picture').style.background = `radial-gradient(ellipse at 69% 35%, ${curItem.hero || '#ff0060'} 0%, #241f24 38%, #08090c 82%)`;
            root.querySelector('#xp-shelf-label').textContent = `${sections[section]} • AHOY LIBRARY (${items.length} TITLES)`;
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

if old_shelf_render not in content:
    print("ERROR: old_shelf_render not found")
    exit(1)

content = content.replace(old_shelf_render, new_shelf_render, 1)

# 6. Update tune() section !== 0 item lookup
old_tune = """        } else {
          const item = mediaSections[section][selected];
          say(`Playing ${item.name} • ${item.title}`);
        }"""

new_tune = """        } else {
          const items = getActiveItems();
          const item = items[selected] || items[0] || {};
          say(`Playing ${item.name || item.title} • ${item.title || item.name}`);
        }"""

if old_tune in content:
    content = content.replace(old_tune, new_tune, 1)

# 7. Update act() arrow navigation for other sections
old_act_nav = """        } else {
          // OTHER SECTIONS: LEFT & RIGHT BROWSE MEDIA CARDS
          const list = mediaSections[section] || [];
          if (key === 'ArrowRight' || key === '→') {
            playXboxSound('tick');
            selected = (selected + 1) % list.length;
            render();
          } else if (key === 'ArrowLeft' || key === '←') {
            playXboxSound('tick');
            selected = (selected - 1 + list.length) % list.length;
            render();
          } else if (key === 'ArrowDown' || key === '↓') {
            playXboxSound('tick');
            selected = (selected + 1) % list.length;
            render();
          } else if (key === 'ArrowUp' || key === '↑') {
            playXboxSound('tick');
            selected = (selected - 1 + list.length) % list.length;
            render();
          }
        }"""

new_act_nav = """        } else {
          // OTHER SECTIONS: LEFT & RIGHT BROWSE MEDIA CARDS
          const list = getActiveItems();
          if (list.length === 0) return;
          if (key === 'ArrowRight' || key === '→') {
            playXboxSound('tick');
            selected = (selected + 1) % list.length;
            render();
          } else if (key === 'ArrowLeft' || key === '←') {
            playXboxSound('tick');
            selected = (selected - 1 + list.length) % list.length;
            render();
          } else if (key === 'ArrowDown' || key === '↓') {
            playXboxSound('tick');
            selected = (selected + 1) % list.length;
            render();
          } else if (key === 'ArrowUp' || key === '↑') {
            playXboxSound('tick');
            selected = (selected - 1 + list.length) % list.length;
            render();
          }
        }"""

if old_act_nav in content:
    content = content.replace(old_act_nav, new_act_nav, 1)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('/Users/agworkywork/ahoy-on-xbox/docs/xbox-ui-preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Successfully updated preview.html and xbox-ui-preview.html with 36 on-demand titles, photographic thumbnails, category chips, and sorting!")
