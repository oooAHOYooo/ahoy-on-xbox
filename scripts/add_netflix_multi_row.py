#!/usr/bin/env python3
import re

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for Netflix Multi-Row & Grid View
css_marker = "/* SHELF CATEGORY & SORT BAR */"
css_addition = """    /* NETFLIX MULTI-ROW DOCK & VERTICAL SCROLL */
    #xbox-preview .xp-netflix-dock {
      display: flex;
      flex-direction: column;
      gap: 14px;
      max-height: clamp(180px, 22vw, 245px);
      overflow-y: auto;
      overflow-x: hidden;
      padding: 2px 6px 14px 2px;
      scroll-behavior: smooth;
      scrollbar-width: thin;
      scrollbar-color: rgba(255, 255, 255, 0.18) transparent;
    }
    #xbox-preview .xp-netflix-dock::-webkit-scrollbar {
      width: 4px;
    }
    #xbox-preview .xp-netflix-dock::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.2);
      border-radius: 4px;
    }
    #xbox-preview .xp-shelf-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: opacity 0.2s ease, transform 0.2s ease;
      scroll-margin-top: 8px;
    }
    #xbox-preview .xp-shelf-row-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 4px;
      cursor: pointer;
    }
    #xbox-preview .xp-row-title {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #9A9AA2;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: color 0.15s ease;
    }
    #xbox-preview .xp-shelf-row[data-active="true"] .xp-row-title {
      color: var(--xp-pink);
    }
    #xbox-preview .xp-shelf-row[data-active="true"] .xp-row-title::before {
      content: "▶";
      font-size: 8px;
      color: var(--xp-pink);
    }
    #xbox-preview .xp-row-count {
      font-size: 9px;
      font-weight: 700;
      color: #6E6E78;
      letter-spacing: 0.04em;
    }
    #xbox-preview .xp-shelf-row[data-active="true"] .xp-row-count {
      color: #FFFFFF;
    }

    /* VERTICAL GRID MODE */
    #xbox-preview .xp-grid-dock {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 12px;
      max-height: clamp(180px, 22vw, 245px);
      overflow-y: auto;
      padding: 4px 6px 14px 2px;
      scroll-behavior: smooth;
      scrollbar-width: thin;
      scrollbar-color: rgba(255, 255, 255, 0.18) transparent;
    }
    #xbox-preview .xp-grid-dock::-webkit-scrollbar {
      width: 4px;
    }
    #xbox-preview .xp-grid-dock::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.2);
      border-radius: 4px;
    }
    #xbox-preview .xp-grid-dock .xp-card {
      width: 100%;
      flex: 1 1 100%;
    }

    /* VIEW MODE TOGGLE BUTTON */
    #xbox-preview .xp-view-mode-btn {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 6px;
      padding: 3px 8px;
      font-size: 9.5px;
      font-weight: 800;
      color: #C0C0C8;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    #xbox-preview .xp-view-mode-btn:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
      color: #FFFFFF;
    }
    #xbox-preview .xp-view-mode-btn.active {
      background: rgba(255, 0, 96, 0.2);
      border-color: var(--xp-pink);
      color: var(--xp-pink);
    }
"""

if css_marker in content:
    content = content.replace(css_marker, css_addition + "\n    " + css_marker, 1)
else:
    print("ERROR: css_marker not found")
    exit(1)

# 2. Add state variables for Netflix Multi-Row & Grid View
old_state = """      let selected = 0;
      let section = 0;
      let activeCategory = 'ALL';
      let activeSort = 'curated';"""

new_state = """      let selected = 0;
      let section = 0;
      let activeCategory = 'ALL';
      let activeSort = 'curated';
      let onDemandViewMode = 'rows'; // 'rows' (Netflix multi-row) or 'grid' (vertical thumbnail wall)
      const categoryNames = ['Skate & Films', 'Series & Shows', 'Live Concerts', 'Music Videos', 'Poets & Friends'];
      let activeRow = 0;
      let activeCols = [0, 0, 0, 0, 0];"""

if old_state in content:
    content = content.replace(old_state, new_state, 1)
else:
    print("ERROR: old_state not found")
    exit(1)

# 3. Add getCategoryRows() and update getCurrentItem()
category_rows_func = """      function getCategoryRows() {
        const fullList = mediaSections[1] || [];
        return categoryNames.map(cat => {
          let items = fullList.filter(it => it.category === cat);
          if (activeSort === 'az') {
            items = [...items].sort((a, b) => (a.title || a.name || '').localeCompare(b.title || b.name || ''));
          } else if (activeSort === 'duration-desc') {
            items = [...items].sort((a, b) => (b.durationSec || 0) - (a.durationSec || 0));
          } else if (activeSort === 'duration-asc') {
            items = [...items].sort((a, b) => (a.durationSec || 0) - (b.durationSec || 0));
          }
          return {
            category: cat,
            count: items.length,
            items: items
          };
        }).filter(r => r.items.length > 0);
      }
"""

content = content.replace("      function getActiveItems() {", category_rows_func + "\n      function getActiveItems() {", 1)

# Update getCurrentItem() for section === 1 Netflix multi-row
old_get_cur = """        } else {
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

new_get_cur = """        } else if (section === 1) {
          if (onDemandViewMode === 'rows' && activeCategory === 'ALL') {
            const rows = getCategoryRows();
            const r = rows[activeRow] || rows[0];
            const colIdx = activeCols[activeRow] || 0;
            const m = (r && r.items[colIdx]) || (r && r.items[0]) || {};
            return {
              id: m.id || `od-${activeRow}-${colIdx}`,
              title: m.title || m.name,
              badge: m.category || m.no,
              sub: m.sub || `${m.name} • On Demand`,
              sec: 1,
              idx: colIdx,
              url: m.url,
              poster: m.poster || m.thumb
            };
          } else {
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
          }
        } else {
          const items = getActiveItems();
          const m = items[selected] || items[0] || {};
          return {
            id: m.id || `sec-${section}-${selected}`,
            title: m.title || m.name,
            badge: m.glyph || m.no,
            sub: m.sub || `${m.name} • ${sections[section]}`,
            sec: section,
            idx: selected,
            url: m.url,
            poster: m.poster || m.thumb
          };
        }"""

if old_get_cur in content:
    content = content.replace(old_get_cur, new_get_cur, 1)
else:
    print("ERROR: old_get_cur not found")
    exit(1)

# 4. Replace On Demand shelf rendering inside render()
old_shelf_block = """        } else {
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

new_shelf_block = """        } else {
          // HORIZONTAL CARD SHELF FOR ON DEMAND, MUSIC, RADIO
          const curItem = getCurrentItem();

          // If On Demand (section 1), render category chips, sort selector, and Netflix Multi-Row vs Vertical Grid toggle
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
              <button type="button" class="xp-view-mode-btn" id="xp-view-mode-btn" title="Toggle Netflix Multi-Row vs Vertical Grid">
                <span>${onDemandViewMode === 'rows' ? '▦ GRID VIEW' : '⊞ NETFLIX ROWS'}</span>
              </button>
              <span>SORT:</span>
              <select class="xp-sort-select" aria-label="Sort videos">
                <option value="curated"${activeSort === 'curated' ? ' selected' : ''}>Curated</option>
                <option value="az"${activeSort === 'az' ? ' selected' : ''}>A–Z</option>
                <option value="duration-desc"${activeSort === 'duration-desc' ? ' selected' : ''}>Duration (Longest)</option>
                <option value="duration-asc"${activeSort === 'duration-asc' ? ' selected' : ''}>Duration (Shortest)</option>
              </select>
            `;
            sortBox.querySelector('#xp-view-mode-btn').addEventListener('click', () => {
              playXboxSound('action');
              onDemandViewMode = onDemandViewMode === 'rows' ? 'grid' : 'rows';
              render();
              tune(false);
              say(onDemandViewMode === 'rows' ? 'Netflix Multi-Row Shelves' : 'Vertical Thumbnail Grid');
            });
            sortBox.querySelector('select').addEventListener('change', (e) => {
              playXboxSound('tick');
              activeSort = e.target.value;
              selected = 0;
              render();
              tune(false);
            });
            filtersBar.append(sortBox);

            contentDock.append(filtersBar);

            if (onDemandViewMode === 'rows' && activeCategory === 'ALL') {
              // NETFLIX MULTI-ROW CAROUSELS
              const dock = document.createElement('div');
              dock.className = 'xp-netflix-dock';
              const rows = getCategoryRows();
              if (activeRow >= rows.length) activeRow = 0;

              rows.forEach((r, rIdx) => {
                const isRowActive = rIdx === activeRow;
                const rowDiv = document.createElement('div');
                rowDiv.className = 'xp-shelf-row';
                rowDiv.setAttribute('data-active', isRowActive ? 'true' : 'false');

                const headDiv = document.createElement('div');
                headDiv.className = 'xp-shelf-row-head';
                headDiv.innerHTML = `
                  <span class="xp-row-title">${r.category}</span>
                  <span class="xp-row-count">${r.count} TITLES</span>
                `;
                headDiv.addEventListener('click', () => {
                  activeRow = rIdx;
                  render();
                  tune(false);
                });
                rowDiv.append(headDiv);

                const cardsContainer = document.createElement('div');
                cardsContainer.className = 'xp-cards';

                const curCol = activeCols[rIdx] || 0;
                r.items.forEach((c, cIdx) => {
                  const isCardCur = isRowActive && cIdx === curCol;
                  const b = document.createElement('button');
                  b.type = 'button';
                  b.className = 'xp-card';
                  b.setAttribute('aria-current', isCardCur ? 'true' : 'false');
                  if (c.art) b.style.setProperty('--art', c.art);

                  const posterUrl = c.thumb || c.poster;
                  const hasPhoto = Boolean(posterUrl);

                  b.innerHTML = `
                    ${hasPhoto ? `<div class="xp-card-poster" style="background-image: url('${posterUrl}')"></div>` : `<span class="xp-glyph" aria-hidden="true">${c.glyph || '▶'}</span>`}
                    <span class="xp-card-copy">
                      <small>${c.category}${isCardCur ? '<span class="xp-mini-eq"><i></i><i></i><i></i></span>' : ''}</small>
                      <strong>${c.title}</strong>
                      <span>${c.line || c.duration}</span>
                    </span>
                  `;
                  b.addEventListener('click', () => {
                    activeRow = rIdx;
                    activeCols[rIdx] = cIdx;
                    render();
                    tune(false);
                  });
                  cardsContainer.append(b);
                });
                rowDiv.append(cardsContainer);
                dock.append(rowDiv);

                if (isRowActive) {
                  const activeCard = cardsContainer.querySelector('.xp-card[aria-current="true"]');
                  if (activeCard) {
                    setTimeout(() => {
                      activeCard.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
                      rowDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 30);
                  }
                }
              });

              contentDock.append(dock);

              const hints = root.querySelector('#xp-hints');
              if (hints) {
                hints.innerHTML = `
                  <span><kbd>▲ ▼</kbd> Category Rows</span>
                  <span><kbd>◀ ▶</kbd> Browse Cards</span>
                  <span><kbd>V</kbd> Grid View</span>
                  <span><kbd class="xp-hint-a">A</kbd> Play</span>
                  <span><kbd class="xp-hint-b">B</kbd> Close</span>
                `;
              }
            } else if (onDemandViewMode === 'grid') {
              // VERTICAL GRID VIEW
              const gridDock = document.createElement('div');
              gridDock.className = 'xp-grid-dock';
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
                gridDock.append(b);
              });
              contentDock.append(gridDock);

              const activeCard = gridDock.querySelector('.xp-card[aria-current="true"]');
              if (activeCard) {
                setTimeout(() => {
                  activeCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 30);
              }

              const hints = root.querySelector('#xp-hints');
              if (hints) {
                hints.innerHTML = `
                  <span><kbd>▲ ▼ ◀ ▶</kbd> Grid</span>
                  <span><kbd>V</kbd> Netflix Rows</span>
                  <span><kbd class="xp-hint-a">A</kbd> Play</span>
                  <span><kbd class="xp-hint-b">B</kbd> Close</span>
                `;
              }
            } else {
              // SINGLE CATEGORY HORIZONTAL SHELF
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
            }
          } else {
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
          }

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

if old_shelf_block in content:
    content = content.replace(old_shelf_block, new_shelf_block, 1)
else:
    print("ERROR: old_shelf_block not found")
    exit(1)

# 5. Update act() navigation for section === 1
old_act_block = """        } else {
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

new_act_block = """        } else if (section === 1) {
          // ON DEMAND NAVIGATION (NETFLIX MULTI-ROW VS GRID)
          if (onDemandViewMode === 'rows' && activeCategory === 'ALL') {
            const rows = getCategoryRows();
            if (rows.length === 0) return;
            if (key === 'ArrowDown' || key === '↓') {
              playXboxSound('tick');
              activeRow = (activeRow + 1) % rows.length;
              render();
              tune(false);
            } else if (key === 'ArrowUp' || key === '↑') {
              playXboxSound('tick');
              activeRow = (activeRow - 1 + rows.length) % rows.length;
              render();
              tune(false);
            } else if (key === 'ArrowRight' || key === '→') {
              playXboxSound('tick');
              const rowItems = rows[activeRow].items;
              activeCols[activeRow] = (activeCols[activeRow] + 1) % rowItems.length;
              render();
              tune(false);
            } else if (key === 'ArrowLeft' || key === '←') {
              playXboxSound('tick');
              const rowItems = rows[activeRow].items;
              activeCols[activeRow] = (activeCols[activeRow] - 1 + rowItems.length) % rowItems.length;
              render();
              tune(false);
            }
          } else if (onDemandViewMode === 'grid') {
            const list = getActiveItems();
            if (list.length === 0) return;
            if (key === 'ArrowRight' || key === '→') {
              playXboxSound('tick');
              selected = (selected + 1) % list.length;
              render();
              tune(false);
            } else if (key === 'ArrowLeft' || key === '←') {
              playXboxSound('tick');
              selected = (selected - 1 + list.length) % list.length;
              render();
              tune(false);
            } else if (key === 'ArrowDown' || key === '↓') {
              playXboxSound('tick');
              selected = Math.min(list.length - 1, selected + 4);
              render();
              tune(false);
            } else if (key === 'ArrowUp' || key === '↑') {
              playXboxSound('tick');
              selected = Math.max(0, selected - 4);
              render();
              tune(false);
            }
          } else {
            const list = getActiveItems();
            if (list.length === 0) return;
            if (key === 'ArrowRight' || key === '→') {
              playXboxSound('tick');
              selected = (selected + 1) % list.length;
              render();
              tune(false);
            } else if (key === 'ArrowLeft' || key === '←') {
              playXboxSound('tick');
              selected = (selected - 1 + list.length) % list.length;
              render();
              tune(false);
            }
          }
        } else {
          // MUSIC & RADIO NAVIGATION
          const list = getActiveItems();
          if (list.length === 0) return;
          if (key === 'ArrowRight' || key === '→') {
            playXboxSound('tick');
            selected = (selected + 1) % list.length;
            render();
            tune(false);
          } else if (key === 'ArrowLeft' || key === '←') {
            playXboxSound('tick');
            selected = (selected - 1 + list.length) % list.length;
            render();
            tune(false);
          } else if (key === 'ArrowDown' || key === '↓') {
            playXboxSound('tick');
            selected = (selected + 1) % list.length;
            render();
            tune(false);
          } else if (key === 'ArrowUp' || key === '↑') {
            playXboxSound('tick');
            selected = (selected - 1 + list.length) % list.length;
            render();
            tune(false);
          }
        }"""

if old_act_block in content:
    content = content.replace(old_act_block, new_act_block, 1)
else:
    print("ERROR: old_act_block not found")
    exit(1)

# 6. Add 'v' / 'V' shortcut in keydown handler
old_v_key = "} else if ('xyabXYAB1234mM'.includes(e.key)) {"
new_v_key = "} else if ('xyabXYAB1234mMvV'.includes(e.key)) {"
content = content.replace(old_v_key, new_v_key, 1)

# Add handling inside act()
view_key_handler = """        if (key === 'v' || key === 'V') {
          if (section === 1) {
            playXboxSound('action');
            onDemandViewMode = onDemandViewMode === 'rows' ? 'grid' : 'rows';
            render();
            tune(false);
            say(onDemandViewMode === 'rows' ? 'Netflix Multi-Row Shelves' : 'Vertical Thumbnail Grid');
            return;
          }
        }
"""
content = content.replace("        if (key === 'LT') {", view_key_handler + "        if (key === 'LT') {", 1)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('/Users/agworkywork/ahoy-on-xbox/docs/xbox-ui-preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Netflix multi-row layout and vertical grid toggle installed in preview.html and xbox-ui-preview.html!")
