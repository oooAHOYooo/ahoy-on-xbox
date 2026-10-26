import subprocess
from pathlib import Path

OUT_DIR = Path("/Users/agworkywork/ahoy-on-xbox/dist/store_assets")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def render_html_to_png(html_content, out_path, width, height):
    tmp_html = OUT_DIR / "temp_render.html"
    tmp_html.write_text(html_content, encoding="utf-8")
    
    cmd = [
        CHROME,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={out_path}",
        f"file://{tmp_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if tmp_html.exists():
        tmp_html.unlink()
    print(f"Generated: {out_path} ({width}x{height})")

# Shared Minimalist Ahoy Brand Styles
# Dark obsidian #0A0D14 / #0E131C, unified, subtle vignette, authentic typography

# 1. 9:16 Poster Art (720 x 1080) - Required for Xbox
html_poster_9_16 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 720px;
    height: 1080px;
    background: radial-gradient(circle at 50% 40%, #141924 0%, #0A0D14 70%, #06080D 100%);
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 100px 60px;
    position: relative;
    overflow: hidden;
  }
  .center-brand {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 180px;
  }
  .wordmark {
    width: 460px;
    filter: drop-shadow(0 10px 25px rgba(0,0,0,0.8));
  }
  .subtitle {
    margin-top: 20px;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 12px;
    color: #FFFFFF;
    text-transform: uppercase;
    text-indent: 12px;
  }
  .descriptor {
    margin-top: 14px;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 6px;
    color: #6C7A8E;
    text-transform: uppercase;
    text-indent: 6px;
  }
  .bottom-tagline {
    font-size: 13px;
    letter-spacing: 3px;
    color: #4A5568;
    text-transform: uppercase;
    font-weight: 600;
  }
</style>
</head>
<body>
  <div class="center-brand">
    <img class="wordmark" src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
    <div class="subtitle">TV</div>
    <div class="descriptor">Indie Media</div>
  </div>
  <div class="bottom-tagline">
    Independent Culture &bull; Always On
  </div>
</body>
</html>
"""

# 2. 1:1 Box Art (1080 x 1080)
html_box_art_1_1 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px;
    height: 1080px;
    background: radial-gradient(circle at 50% 48%, #141924 0%, #0A0D14 65%, #06080D 100%);
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 80px;
    position: relative;
    overflow: hidden;
  }
  .center-brand {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .wordmark {
    width: 620px;
    filter: drop-shadow(0 15px 30px rgba(0,0,0,0.85));
  }
  .subtitle {
    margin-top: 24px;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: 16px;
    color: #FFFFFF;
    text-transform: uppercase;
    text-indent: 16px;
  }
  .descriptor {
    margin-top: 16px;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 8px;
    color: #6C7A8E;
    text-transform: uppercase;
    text-indent: 8px;
  }
</style>
</head>
<body>
  <div class="center-brand">
    <img class="wordmark" src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
    <div class="subtitle">TV</div>
    <div class="descriptor">Indie Media</div>
  </div>
</body>
</html>
"""

# 3. 16:9 Super Hero Art (1920 x 1080) - "Must NOT include product title"
html_super_hero_art = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1920px;
    height: 1080px;
    background: radial-gradient(ellipse at 50% 50%, #161C28 0%, #0B0E16 65%, #05070B 100%);
    position: relative;
    overflow: hidden;
  }
  .ambient-glow {
    position: absolute;
    width: 1200px;
    height: 600px;
    background: radial-gradient(ellipse, rgba(40, 52, 75, 0.4) 0%, transparent 70%);
    top: 240px;
    left: 360px;
  }
</style>
</head>
<body>
  <div class="ambient-glow"></div>
</body>
</html>
"""

# 4. Xbox Branded Key Art (584 x 800) - Title in top 3/4
html_branded_key_art = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 584px;
    height: 800px;
    background: radial-gradient(circle at 50% 40%, #141924 0%, #0A0D14 65%, #06080D 100%);
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 70px 40px;
    position: relative;
    overflow: hidden;
  }
  .center-brand {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 100px;
  }
  .wordmark {
    width: 380px;
    filter: drop-shadow(0 10px 20px rgba(0,0,0,0.8));
  }
  .subtitle {
    margin-top: 18px;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 10px;
    color: #FFFFFF;
    text-transform: uppercase;
    text-indent: 10px;
  }
  .descriptor {
    margin-top: 12px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 5px;
    color: #6C7A8E;
    text-transform: uppercase;
    text-indent: 5px;
  }
  .bottom-tagline {
    font-size: 12px;
    letter-spacing: 2px;
    color: #4A5568;
    text-transform: uppercase;
    font-weight: 600;
  }
</style>
</head>
<body>
  <div class="center-brand">
    <img class="wordmark" src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
    <div class="subtitle">TV</div>
    <div class="descriptor">Indie Media</div>
  </div>
  <div class="bottom-tagline">
    Always On &bull; Free Streaming
  </div>
</body>
</html>
"""

# 5. Xbox Titled Hero Art (1920 x 1080) - Title in top 3/4
html_titled_hero_art = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1920px;
    height: 1080px;
    background: radial-gradient(ellipse at 50% 45%, #151B27 0%, #0A0D14 65%, #05070B 100%);
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
  }
  .center-brand {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: -40px;
  }
  .wordmark {
    width: 720px;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.85));
  }
  .subtitle {
    margin-top: 24px;
    font-size: 36px;
    font-weight: 700;
    letter-spacing: 18px;
    color: #FFFFFF;
    text-transform: uppercase;
    text-indent: 18px;
  }
  .descriptor {
    margin-top: 16px;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 8px;
    color: #6C7A8E;
    text-transform: uppercase;
    text-indent: 8px;
  }
</style>
</head>
<body>
  <div class="center-brand">
    <img class="wordmark" src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
    <div class="subtitle">TV</div>
    <div class="descriptor">Indie Media</div>
  </div>
</body>
</html>
"""

# 6. Xbox Featured Promo Square Art (1080 x 1080) - "Must NOT include product title"
html_promo_square = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px;
    height: 1080px;
    background: radial-gradient(circle at 50% 50%, #161C28 0%, #0B0E16 65%, #05070B 100%);
    position: relative;
    overflow: hidden;
  }
  .subtle-ring {
    position: absolute;
    width: 700px;
    height: 700px;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.04);
    top: 190px;
    left: 190px;
  }
</style>
</head>
<body>
  <div class="subtle-ring"></div>
</body>
</html>
"""

# 7. Screenshot 1: Clean, Authentic TV Guide Interface (1920 x 1080)
# Featuring real Rob Meglio fisheye still, Samuel Dylan Witch, and G-Dub thumbnails
html_screenshot_guide = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1920px;
    height: 1080px;
    background: #0A0D14;
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    padding: 48px 64px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
  }
  .header {
    display: flex;
    align-items: center;
    margin-bottom: 24px;
  }
  .logo-img {
    height: 44px;
  }
  .tv-label {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 6px;
    margin-left: 18px;
    color: #FFFFFF;
  }
  .tagline {
    font-size: 15px;
    letter-spacing: 3px;
    color: #6C7A8E;
    margin-left: 32px;
    font-weight: 600;
    text-transform: uppercase;
  }
  .main-layout {
    display: grid;
    grid-template-columns: 340px 1fr;
    gap: 40px;
    flex: 1;
    min-height: 0;
  }
  .channel-col {
    display: flex;
    flex-direction: column;
    background: #0E121A;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }
  .col-title {
    font-size: 14px;
    letter-spacing: 2px;
    color: #6C7A8E;
    font-weight: 700;
    margin-bottom: 20px;
  }
  .channel-card {
    padding: 16px 18px;
    border-radius: 8px;
    margin-bottom: 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 2px solid transparent;
  }
  .channel-card.selected {
    background: rgba(255, 255, 255, 0.08);
    border-color: #FFFFFF;
  }
  .channel-card .name {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 4px;
  }
  .channel-card .desc {
    font-size: 13px;
    color: #8E9AA8;
  }
  .stage-col {
    display: flex;
    flex-direction: column;
    min-height: 0;
  }
  .player-frame {
    width: 100%;
    height: 520px;
    background: #000;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
  .player-frame img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .player-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 24px 32px;
    background: linear-gradient(to top, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
  }
  .progress-bg {
    width: 100%;
    height: 5px;
    background: rgba(255,255,255,0.25);
    border-radius: 2px;
    margin-bottom: 14px;
    overflow: hidden;
  }
  .progress-bar {
    width: 42%;
    height: 100%;
    background: #FFFFFF;
  }
  .player-meta {
    display: flex;
    justify-content: space-between;
    font-size: 15px;
    color: #CBD5E0;
    font-weight: 500;
  }
  .playing-info {
    margin: 20px 0 16px 0;
  }
  .playing-title {
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 6px;
  }
  .playing-sub {
    font-size: 15px;
    color: #8E9AA8;
  }
  .queue-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 8px;
  }
  .queue-item {
    background: #0E121A;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    padding: 10px;
  }
  .queue-thumb {
    width: 80px;
    height: 54px;
    border-radius: 6px;
    object-fit: cover;
    margin-right: 14px;
    flex-shrink: 0;
  }
  .queue-title {
    font-size: 15px;
    font-weight: 700;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 3px;
  }
  .queue-host {
    font-size: 13px;
    color: #718096;
  }
  .footer {
    font-size: 14px;
    color: #4A5568;
    letter-spacing: 1px;
    padding-top: 18px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }
</style>
</head>
<body>
  <div class="header">
    <img class="logo-img" src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
    <div class="tv-label">TV</div>
    <div class="tagline">Independent Culture &bull; Always On</div>
  </div>

  <div class="main-layout">
    <div class="channel-col">
      <div class="col-title">CHANNELS</div>
      <div class="channel-card selected">
        <div class="name">Ahoy Mix</div>
        <div class="desc">36 videos &bull; continuous queue</div>
      </div>
      <div class="channel-card">
        <div class="name">Music Videos</div>
        <div class="desc">Independent releases & visuals</div>
      </div>
      <div class="channel-card">
        <div class="name">Skating</div>
        <div class="desc">Street, park & sponsor reels</div>
      </div>
      <div class="channel-card">
        <div class="name">G-Dub Disc Golf</div>
        <div class="desc">Courses, reviews & rounds</div>
      </div>
    </div>

    <div class="stage-col">
      <div class="player-frame">
        <img src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/rob.png">
        <div class="player-overlay">
          <div class="progress-bg">
            <div class="progress-bar"></div>
          </div>
          <div class="player-meta">
            <span>▶ Playing &bull; 03:42 / 09:15</span>
            <span>HD &bull; Stereo</span>
          </div>
        </div>
      </div>

      <div class="playing-info">
        <div class="playing-title">Rob Meglio's Sponsor Me Tape - October 2026</div>
        <div class="playing-sub">Ahoy Mix &bull; Rob Meglio &bull; Next video plays automatically</div>
      </div>

      <div class="queue-grid">
        <div class="queue-item">
          <img class="queue-thumb" src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/samuel.jpg">
          <div style="min-width: 0;">
            <div class="queue-title">Samuel Dylan Witch — Stop and Rewind</div>
            <div class="queue-host">Samuel Dylan Witch</div>
          </div>
        </div>
        <div class="queue-item">
          <img class="queue-thumb" src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/gdub.jpg">
          <div style="min-width: 0;">
            <div class="queue-title">Which Discraft Putter is Best</div>
            <div class="queue-host">Greg Weese</div>
          </div>
        </div>
        <div class="queue-item">
          <img class="queue-thumb" src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/rob.png">
          <div style="min-width: 0;">
            <div class="queue-title">Sponsor Me Tape for Flux</div>
            <div class="queue-host">Rob Meglio</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="footer">
    D-pad to browse &nbsp;&bull;&nbsp; A to select &nbsp;&bull;&nbsp; Playback controls for pause, seek and fullscreen
  </div>
</body>
</html>
"""

print("Rendering unified, minimalist Ahoy TV Store assets...")
render_html_to_png(html_poster_9_16, OUT_DIR / "poster_art_9_16.png", 720, 1080)
render_html_to_png(html_box_art_1_1, OUT_DIR / "box_art_1_1.png", 1080, 1080)
render_html_to_png(html_super_hero_art, OUT_DIR / "super_hero_art_16_9.png", 1920, 1080)
render_html_to_png(html_branded_key_art, OUT_DIR / "branded_key_art_584x800.png", 584, 800)
render_html_to_png(html_titled_hero_art, OUT_DIR / "titled_hero_art_1920x1080.png", 1920, 1080)
render_html_to_png(html_promo_square, OUT_DIR / "promo_square_1080x1080.png", 1080, 1080)
render_html_to_png(html_screenshot_guide, OUT_DIR / "screenshot_tv_guide.png", 1920, 1080)

# Generate small tile icons: 300x300, 150x150, 71x71
subprocess.run(["sips", "-z", "300", "300", str(OUT_DIR / "box_art_1_1.png"), "--out", str(OUT_DIR / "app_tile_300x300.png")], check=True)
subprocess.run(["sips", "-z", "150", "150", str(OUT_DIR / "box_art_1_1.png"), "--out", str(OUT_DIR / "app_tile_150x150.png")], check=True)
subprocess.run(["sips", "-z", "71", "71", str(OUT_DIR / "box_art_1_1.png"), "--out", str(OUT_DIR / "app_tile_71x71.png")], check=True)

print("ALL MINIMALIST ASSETS SUCCESSFULLY GENERATED!")
