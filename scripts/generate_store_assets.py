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

# 1. 9:16 Poster Art (720 x 1080) - Required for Xbox!
html_poster_9_16 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 720px;
    height: 1080px;
    background: radial-gradient(circle at 50% 30%, #1A2436 0%, #0D121B 70%, #07090E 100%);
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 80px 48px;
    position: relative;
    overflow: hidden;
  }
  .glow {
    position: absolute;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(0, 229, 255, 0.15) 0%, rgba(199, 255, 107, 0.08) 40%, transparent 70%);
    top: 20%;
    left: 110px;
    z-index: 1;
  }
  .center-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 2;
    margin-top: 140px;
  }
  .wordmark-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
  }
  .wordmark-wrap img {
    width: 440px;
    filter: drop-shadow(0 15px 35px rgba(0,0,0,0.8));
  }
  .tv-badge {
    background: #00E5FF;
    color: #080D14;
    font-size: 32px;
    font-weight: 900;
    padding: 6px 18px;
    border-radius: 8px;
    margin-left: 16px;
    letter-spacing: 2px;
    box-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
  }
  .tagline {
    font-size: 20px;
    letter-spacing: 5px;
    color: #C7FF6B;
    font-weight: 800;
    text-transform: uppercase;
    text-align: center;
    margin-top: 12px;
  }
  .subtag {
    font-size: 16px;
    letter-spacing: 2px;
    color: #A0AEC0;
    margin-top: 12px;
    font-weight: 600;
    text-transform: uppercase;
  }
  .bottom-info {
    z-index: 2;
    text-align: center;
    color: #718096;
    font-size: 15px;
    letter-spacing: 1px;
    font-weight: 500;
  }
  .pills {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    z-index: 2;
  }
  .pill {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 13px;
    color: #E2E8F0;
    letter-spacing: 1px;
    font-weight: 600;
  }
</style>
</head>
<body>
  <div class="glow"></div>
  <div class="center-content">
    <div class="wordmark-wrap">
      <img src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
      <span class="tv-badge">TV</span>
    </div>
    <div class="tagline">Independent Culture</div>
    <div class="subtag">Always On &bull; Music &bull; Skate &bull; Arts</div>
  </div>
  
  <div class="pills">
    <div class="pill">FREE CHANNELS</div>
    <div class="pill">ON DEMAND</div>
    <div class="pill">XBOX READY</div>
  </div>

  <div class="bottom-info">
    AHOY INDIE MEDIA &bull; 2026
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
    background: radial-gradient(circle at 50% 45%, #182232 0%, #0E131C 60%, #06080C 100%);
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
  .glow {
    position: absolute;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(0, 229, 255, 0.12) 0%, rgba(199, 255, 107, 0.08) 50%, transparent 70%);
    z-index: 1;
  }
  .center-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 2;
  }
  .wordmark-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
  }
  .wordmark-wrap img {
    width: 580px;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.9));
  }
  .tv-badge {
    background: #00E5FF;
    color: #080D14;
    font-size: 42px;
    font-weight: 900;
    padding: 8px 24px;
    border-radius: 10px;
    margin-left: 20px;
    letter-spacing: 2px;
    box-shadow: 0 0 30px rgba(0, 229, 255, 0.6);
  }
  .tagline {
    font-size: 26px;
    letter-spacing: 7px;
    color: #C7FF6B;
    font-weight: 800;
    text-transform: uppercase;
    text-align: center;
    margin-top: 16px;
  }
  .subtag {
    font-size: 20px;
    letter-spacing: 3px;
    color: #A0AEC0;
    margin-top: 14px;
    font-weight: 600;
    text-transform: uppercase;
  }
</style>
</head>
<body>
  <div class="glow"></div>
  <div class="center-content">
    <div class="wordmark-wrap">
      <img src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
      <span class="tv-badge">TV</span>
    </div>
    <div class="tagline">Independent Culture. Always On.</div>
    <div class="subtag">Music &bull; Skating &bull; Disc Golf &bull; Independent Arts</div>
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
    background: linear-gradient(135deg, #0A0E17 0%, #151D2A 50%, #0A0D14 100%);
    position: relative;
    overflow: hidden;
  }
  .beam-1 {
    position: absolute;
    width: 800px;
    height: 1400px;
    background: linear-gradient(to right, rgba(0, 229, 255, 0.15), transparent);
    transform: rotate(35deg);
    top: -300px;
    left: 200px;
  }
  .beam-2 {
    position: absolute;
    width: 600px;
    height: 1200px;
    background: linear-gradient(to right, rgba(199, 255, 107, 0.1), transparent);
    transform: rotate(-25deg);
    top: -200px;
    right: 250px;
  }
  .grid-pattern {
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: 
      linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 80px 80px;
    opacity: 0.6;
  }
</style>
</head>
<body>
  <div class="grid-pattern"></div>
  <div class="beam-1"></div>
  <div class="beam-2"></div>
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
    background: radial-gradient(circle at 50% 35%, #182232 0%, #0E131C 65%, #06080C 100%);
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 60px 36px;
    position: relative;
    overflow: hidden;
  }
  .top-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 60px;
    z-index: 2;
  }
  .wordmark-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .wordmark-wrap img {
    width: 360px;
    filter: drop-shadow(0 15px 30px rgba(0,0,0,0.8));
  }
  .tv-badge {
    background: #00E5FF;
    color: #080D14;
    font-size: 26px;
    font-weight: 900;
    padding: 5px 14px;
    border-radius: 6px;
    margin-left: 12px;
    letter-spacing: 1px;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.6);
  }
  .tagline {
    font-size: 17px;
    letter-spacing: 4px;
    color: #C7FF6B;
    font-weight: 800;
    text-transform: uppercase;
    text-align: center;
    margin-top: 14px;
  }
  .bottom-section {
    z-index: 2;
    text-align: center;
    color: #A0AEC0;
    font-size: 14px;
    letter-spacing: 1px;
  }
</style>
</head>
<body>
  <div class="top-section">
    <div class="wordmark-wrap">
      <img src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
      <span class="tv-badge">TV</span>
    </div>
    <div class="tagline">Independent Culture</div>
  </div>
  <div class="bottom-section">
    Curated Channels &bull; On Demand
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
    background: radial-gradient(circle at 50% 40%, #1A2436 0%, #0F1520 60%, #070A0F 100%);
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
  }
  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: -80px;
    z-index: 2;
  }
  .wordmark-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .wordmark-wrap img {
    width: 680px;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.9));
  }
  .tv-badge {
    background: #00E5FF;
    color: #080D14;
    font-size: 48px;
    font-weight: 900;
    padding: 10px 28px;
    border-radius: 12px;
    margin-left: 24px;
    letter-spacing: 2px;
    box-shadow: 0 0 35px rgba(0, 229, 255, 0.6);
  }
  .tagline {
    font-size: 32px;
    letter-spacing: 8px;
    color: #C7FF6B;
    font-weight: 800;
    text-transform: uppercase;
    text-align: center;
    margin-top: 24px;
  }
</style>
</head>
<body>
  <div class="content">
    <div class="wordmark-wrap">
      <img src="file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_wordmark_white.png">
      <span class="tv-badge">TV</span>
    </div>
    <div class="tagline">Independent Culture. Always On.</div>
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
    background: radial-gradient(circle at 50% 50%, #1B2538 0%, #101622 65%, #080C12 100%);
    position: relative;
    overflow: hidden;
  }
  .rings {
    position: absolute;
    width: 800px;
    height: 800px;
    border-radius: 50%;
    border: 2px solid rgba(0, 229, 255, 0.15);
    top: 140px;
    left: 140px;
  }
  .rings-inner {
    position: absolute;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    border: 2px solid rgba(199, 255, 107, 0.12);
    top: 290px;
    left: 290px;
  }
</style>
</head>
<body>
  <div class="rings"></div>
  <div class="rings-inner"></div>
</body>
</html>
"""

print("Generating all Partner Center store assets...")
render_html_to_png(html_poster_9_16, OUT_DIR / "poster_art_9_16.png", 720, 1080)
render_html_to_png(html_box_art_1_1, OUT_DIR / "box_art_1_1.png", 1080, 1080)
render_html_to_png(html_super_hero_art, OUT_DIR / "super_hero_art_16_9.png", 1920, 1080)
render_html_to_png(html_branded_key_art, OUT_DIR / "branded_key_art_584x800.png", 584, 800)
render_html_to_png(html_titled_hero_art, OUT_DIR / "titled_hero_art_1920x1080.png", 1920, 1080)
render_html_to_png(html_promo_square, OUT_DIR / "promo_square_1080x1080.png", 1080, 1080)

# Also generate the smaller app tiles: 300x300, 150x150, 71x71
subprocess.run(["sips", "-z", "300", "300", str(OUT_DIR / "box_art_1_1.png"), "--out", str(OUT_DIR / "app_tile_300x300.png")], check=True)
subprocess.run(["sips", "-z", "150", "150", str(OUT_DIR / "box_art_1_1.png"), "--out", str(OUT_DIR / "app_tile_150x150.png")], check=True)
subprocess.run(["sips", "-z", "71", "71", str(OUT_DIR / "box_art_1_1.png"), "--out", str(OUT_DIR / "app_tile_71x71.png")], check=True)

print("ALL STORE ASSETS SUCCESSFULLY GENERATED!")
