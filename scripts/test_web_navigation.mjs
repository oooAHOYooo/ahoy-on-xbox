import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'AhoyXbox/Web/index.html');
const output = process.env.TV_SCREENSHOT_DIR || path.join(root, 'dist/web-ui-checks');
await fs.mkdir(output, { recursive: true });
assert.equal(await fs.readFile(source, 'utf8'), await fs.readFile(path.join(root, 'dist/store_assets/tv_app_preview.html'), 'utf8'), 'Source and preview must stay in sync');
const browser = await chromium.launch({ executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH || undefined });
try {
  for (const viewport of [{ width: 1290, height: 731 }, { width: 1280, height: 720 }, { width: 1920, height: 1080 }, { width: 1024, height: 600 }, { width: 390, height: 844 }]) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    // Test real DOM click/focus/source selection without depending on media hosts,
    // downloading videos, or asserting that mocked playback decodes successfully.
    await page.route('https://**/*', route => route.abort());
    await page.clock.install();
    await page.addInitScript(() => {
      HTMLMediaElement.prototype.play = function () { return Promise.resolve(); };
      HTMLMediaElement.prototype.pause = function () {};
    });
    await page.goto(pathToFileURL(source).href, { waitUntil: 'domcontentloaded' });
    // Check settled layout rather than a guide's in-progress slide transition.
    // Timer behavior is exercised separately with the virtual clock below.
    await page.addStyleTag({ content: '* { transition: none !important; animation: none !important; scroll-behavior: auto !important; }' });
    const checkBounds = async () => {
      const result = await page.evaluate(() => {
        const box = selector => {
          const r = document.querySelector(selector).getBoundingClientRect();
          return { x: r.x, y: r.y, right: r.right, bottom: r.bottom, width: r.width, height: r.height };
        };
        return { app: box('.app-container'), header: box('.top-bar'), nav: box('.section-nav'), guide: box('#guide-dock'), card: box('.item-card') };
      });
      assert.equal(result.app.width, viewport.width, 'App must fit the viewport width');
      for (const name of ['header', 'nav', 'guide', 'card']) {
        const box = result[name];
        assert(box.x >= -1 && box.y >= -1 && box.right <= viewport.width + 1 && box.bottom <= viewport.height + 1, `${name} is clipped at ${viewport.width}x${viewport.height}: ${JSON.stringify(box)}`);
      }
    };
    await checkBounds();
    await page.clock.fastForward(7000);
    assert.equal(await page.locator('#guide-dock').evaluate(el => el.classList.contains('hidden')), false, 'The guide must not disappear on a timer');
    for (const [section, label] of [['ondemand', 'ON DEMAND'], ['music', 'AHOY MUSIC'], ['podcasts', 'PODCASTS'], ['channels', 'CHANNELS']]) {
      await page.locator(`#nav-${section}`).click();
      assert.equal(await page.locator(`#nav-${section}`).getAttribute('aria-pressed'), 'true');
      assert.equal(await page.locator('.nav-btn.active').count(), 1, 'Only the selected section is active');
      assert((await page.locator('#shelf-title').innerText()).includes(label));
      assert(await page.locator('#items-row .item-card').count() > 0);
      await checkBounds();
    }
    await page.locator('#nav-music').click();
    const musicTitle = await page.locator('#items-row .item-title').first().innerText();
    await page.locator('#items-row .item-card').first().click();
    assert.equal(await page.locator('#hero-title').innerText(), musicTitle);
    assert.equal(await page.locator('#video-player').evaluate(el => el.style.display), 'none');
    assert.equal(await page.locator('#audio-player').evaluate(el => el.muted), false, 'A deliberate media selection should be audible');
    assert.equal(await page.locator('#audio-player').evaluate(el => el.src), await page.evaluate(() => MUSIC[0].stream_url));
    assert.equal(await page.locator('#status-live').innerText(), 'MUSIC');
    await page.locator('#nav-ondemand').click();
    const videoTitle = await page.locator('#items-row .item-title').first().innerText();
    await page.locator('#items-row .item-card').first().click();
    assert.equal(await page.locator('#hero-title').innerText(), videoTitle);
    assert.equal(await page.locator('#video-player').evaluate(el => el.style.display), 'block');
    assert.equal(await page.locator('#video-player').evaluate(el => el.muted), false);
    assert.equal(await page.locator('#status-live').innerText(), 'ON DEMAND');
    await page.locator('#nav-podcasts').click();
    await page.locator('#items-row .item-card').first().click();
    assert((await page.locator('#shelf-title').innerText()).includes('EPISODES'));
    const episodeTitle = await page.locator('#items-row .item-title').first().innerText();
    await page.locator('#items-row .item-card').first().click();
    assert.equal(await page.locator('#hero-title').innerText(), episodeTitle);
    assert.equal(await page.locator('#audio-player').evaluate(el => el.src), await page.evaluate(() => PODCASTS[0].episodes[0].audio_url));
    assert.equal(await page.locator('#status-live').innerText(), 'PODCAST');
    // Existing remote shortcuts and native keyboard buttons must both select items.
    await page.locator('#nav-channels').focus();
    await page.keyboard.press('ArrowRight');
    assert.equal(await page.locator('#nav-ondemand').getAttribute('aria-pressed'), 'true');
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('ArrowRight');
    const secondTitle = await page.locator('#items-row .item-title').nth(1).innerText();
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#hero-title').innerText(), secondTitle);
    await page.keyboard.press('b');
    assert.equal(await page.locator('#guide-dock').evaluate(el => el.classList.contains('hidden')), true);
    await page.locator('#nav-music').click();
    assert.equal(await page.locator('#guide-dock').evaluate(el => el.classList.contains('hidden')), false);
    await page.clock.fastForward(500);
    await checkBounds();
    await page.screenshot({ path: path.join(output, `navigation-${viewport.width}x${viewport.height}.png`) });
    assert.deepEqual(errors, [], 'No JavaScript errors are expected');
    console.log(`Passed ${viewport.width}x${viewport.height}: all sections, media selections, keyboard, persistent header and visible guide`);
    await page.close();
  }
} finally {
  await browser.close();
}
