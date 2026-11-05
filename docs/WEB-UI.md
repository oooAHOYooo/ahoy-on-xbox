# Web TV navigation

The browser interface lives in `AhoyXbox/Web/index.html`; `dist/store_assets/tv_app_preview.html` is its matching standalone preview. `scripts/build_unified_frontend.py` generates both, so layout and handler changes must also be made in that template.

The layout fits the current viewport rather than a fixed 1920×1080 canvas. The top navigation occupies its own persistent header. Live TV, On Demand, Music, and Podcasts each reveal their catalog in a visible lower shelf. Selecting a title changes the player source; merely browsing another section keeps the current media playing. The guide stays visible until explicitly hidden with the existing B shortcut, and choosing a section reveals it again.

Content cards are buttons, so clicking or pressing Enter/Space selects them. Arrow Down enters the cards, Left/Right moves through cards or top sections, and Arrow Up returns to the current section. Native Tab navigation is preserved. Explicit playback selections unmute media; the initial autoplay remains muted to comply with browser autoplay behavior.

## Regression checks

```sh
npm ci
npx playwright install chromium
npm run test:web
```

To use an existing Chrome installation on macOS:

```sh
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' npm run test:web
```

The browser checks cover 1290×731 (the reported screenshot size in CSS pixels), 1280×720, 1920×1080, 1024×600, and 390×844. They check all sections, visible header/catalog/card bounds, click selection of video/music/podcast sources, keyboard selection, correct playback labels, and guide persistence after seven seconds. Source and generated preview must match. CSS transitions are disabled to measure settled geometry.

External media requests are blocked and play/pause calls are stubbed, so these tests verify UI behavior and source selection, not network streaming, codec decoding, or native Windows/Xbox playback. Screenshots go to ignored `dist/web-ui-checks/`. GitHub Actions runs these checks alongside the existing native build jobs.
