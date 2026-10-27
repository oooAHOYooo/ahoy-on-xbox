import subprocess
from pathlib import Path

OUT_DIR = Path("/Users/agworkywork/ahoy-on-xbox/dist/store_assets")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def render(html, out, w=1920, h=1080):
    tmp = OUT_DIR / "temp_render.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", f"--window-size={w},{h}", f"--screenshot={out}", f"file://{tmp}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if tmp.exists(): tmp.unlink()
    print(f"Rendered: {out.name}")

logo_src = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_official_white.png"
ep1_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/wintergreen_ep1.jpg"
sand_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/wintergreen_sand.jpg"
running_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/wintergreen_running.jpg"
dispatch_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/wintergreen_dispatch.jpg"

html_apple_wintergreen = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1920px;
    height: 1080px;
    background: #000000;
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif;
    position: relative;
    overflow: hidden;
  }}

  /* Full-bleed Cinematic Billboard Hero */
  .hero-background {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 700px;
    overflow: hidden;
    z-index: 1;
  }}
  .hero-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 20%;
    filter: brightness(0.9) contrast(1.05);
  }}
  .hero-vignette {{
    position: absolute;
    inset: 0;
    background: 
      linear-gradient(to right, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.5) 45%, transparent 100%),
      linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, transparent 25%, #000000 95%);
  }}

  /* Apple TV Floating Top Navigation Bar */
  .nav-header {{
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 44px 80px;
  }}
  .brand-logo-wrap {{
    display: flex;
    align-items: flex-end;
  }}
  .brand-logo-wrap img {{
    height: 32px;
    object-fit: contain;
  }}
  .brand-tv-pill {{
    font-size: 16px;
    font-weight: 800;
    margin-left: 8px;
    margin-bottom: 2px;
    letter-spacing: -0.5px;
    color: #FFFFFF;
  }}

  .nav-tabs {{
    display: flex;
    align-items: center;
    gap: 36px;
  }}
  .nav-tab {{
    font-size: 18px;
    font-weight: 600;
    color: #98A2B3;
    letter-spacing: 0.2px;
    position: relative;
    padding: 6px 0;
  }}
  .nav-tab.active {{
    color: #FFFFFF;
    font-weight: 700;
  }}
  .nav-tab.active::after {{
    content: '';
    position: absolute;
    bottom: -4px;
    left: 50%;
    transform: translateX(-50%);
    width: 24px;
    height: 3px;
    background: #FFFFFF;
    border-radius: 2px;
  }}

  .nav-badge-pill {{
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    color: #E2E8F0;
  }}
  .live-dot {{
    width: 7px;
    height: 7px;
    background: #FF3B30;
    border-radius: 50%;
    margin-right: 8px;
  }}

  /* Hero Content Description */
  .hero-content {{
    position: relative;
    z-index: 5;
    padding: 30px 80px 0 80px;
    max-width: 820px;
  }}
  .hero-kicker {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #CBD5E1;
    margin-bottom: 14px;
  }}
  .hero-kicker-dot {{
    color: #FFC107;
  }}
  .hero-title {{
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -1.2px;
    line-height: 1.1;
    margin-bottom: 16px;
  }}
  .hero-synopsis {{
    font-size: 18px;
    line-height: 1.5;
    color: #94A3B8;
    margin-bottom: 28px;
    font-weight: 400;
  }}
  .hero-actions {{
    display: flex;
    align-items: center;
    gap: 18px;
  }}
  .btn-primary {{
    background: #FFFFFF;
    color: #000000;
    padding: 16px 36px;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 700;
    border: none;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 10px 25px rgba(255, 255, 255, 0.25);
  }}
  .btn-secondary {{
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #FFFFFF;
    padding: 16px 28px;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 600;
  }}

  /* Bottom Apple TV Horizontal Shelf (Row of Cards) */
  .shelf-container {{
    position: absolute;
    bottom: 50px;
    left: 80px;
    right: 80px;
    z-index: 10;
  }}
  .shelf-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 18px;
  }}
  .shelf-title {{
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #FFFFFF;
  }}
  .shelf-count {{
    font-size: 14px;
    color: #64748B;
    font-weight: 500;
  }}

  .shelf-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 28px;
  }}
  .shelf-card {{
    background: #0E131E;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: transform 0.2s ease;
    position: relative;
  }}
  .shelf-card.focused {{
    transform: scale(1.04);
    border: 2px solid #FFFFFF;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.9), 0 0 20px rgba(255, 255, 255, 0.3);
  }}
  .card-img-wrap {{
    width: 100%;
    height: 180px;
    overflow: hidden;
    position: relative;
  }}
  .card-img-wrap img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}
  .duration-tag {{
    position: absolute;
    bottom: 10px;
    right: 10px;
    background: rgba(0, 0, 0, 0.8);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    color: #E2E8F0;
  }}
  .card-body {{
    padding: 16px 18px;
  }}
  .card-item-title {{
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .card-item-sub {{
    font-size: 13px;
    color: #64748B;
  }}
</style>
</head>
<body>

  <!-- Full-bleed Billboard Hero -->
  <div class="hero-background">
    <img class="hero-img" src="{ep1_thumb}">
    <div class="hero-vignette"></div>
  </div>

  <!-- Apple TV Navigation Header -->
  <div class="nav-header">
    <div class="brand-logo-wrap">
      <img src="{logo_src}">
      <span class="brand-tv-pill">tv</span>
    </div>

    <div class="nav-tabs">
      <div class="nav-tab active">Ahoy TV Channels</div>
      <div class="nav-tab">Radio</div>
      <div class="nav-tab">Music</div>
      <div class="nav-tab">Skating</div>
    </div>

    <div class="nav-badge-pill">
      <span class="live-dot"></span>
      <span>Radio Live: Seen Better Days</span>
    </div>
  </div>

  <!-- Hero Information -->
  <div class="hero-content">
    <div class="hero-kicker">
      <span>Wintergreen Sessions</span>
      <span class="hero-kicker-dot">&bull;</span>
      <span>Season 01 Premiere</span>
    </div>
    <div class="hero-title">Wintergreen Sessions: Whatnot</div>
    <div class="hero-synopsis">
      Live studio session recorded in Connecticut with Kicker Pictures. Experience raw indie rock performances featuring unreleased debuts and reworked classics captured in high-definition video and master audio.
    </div>
    <div class="hero-actions">
      <button class="btn-primary">▶ &nbsp;Play Full Episode</button>
      <button class="btn-secondary">View 4 Performances</button>
    </div>
  </div>

  <!-- Apple TV Shelf: All Wintergreen Studios Episodes -->
  <div class="shelf-container">
    <div class="shelf-header">
      <div class="shelf-title">Wintergreen Studios &bull; Complete Collection</div>
      <div class="shelf-count">4 Tracks &bull; Live Performances</div>
    </div>

    <div class="shelf-row">
      <!-- Card 1 (Focused) -->
      <div class="shelf-card focused">
        <div class="card-img-wrap">
          <img src="{ep1_thumb}">
          <span class="duration-tag">14:28</span>
        </div>
        <div class="card-body">
          <div class="card-item-title">Episode 1: Whatnot (Full Session)</div>
          <div class="card-item-sub">Live Studio Recording &bull; Kicker Pictures</div>
        </div>
      </div>

      <!-- Card 2 -->
      <div class="shelf-card">
        <div class="card-img-wrap">
          <img src="{sand_thumb}">
          <span class="duration-tag">03:45</span>
        </div>
        <div class="card-body">
          <div class="card-item-title">Whatnot — Sand</div>
          <div class="card-item-sub">Wintergreen Sessions &bull; Track 01</div>
        </div>
      </div>

      <!-- Card 3 -->
      <div class="shelf-card">
        <div class="card-img-wrap">
          <img src="{running_thumb}">
          <span class="duration-tag">04:12</span>
        </div>
        <div class="card-body">
          <div class="card-item-title">Whatnot — Running Away</div>
          <div class="card-item-sub">Wintergreen Sessions &bull; Track 02</div>
        </div>
      </div>

      <!-- Card 4 -->
      <div class="shelf-card">
        <div class="card-img-wrap">
          <img src="{dispatch_thumb}">
          <span class="duration-tag">04:58</span>
        </div>
        <div class="card-body">
          <div class="card-item-title">Whatnot — Dispatch</div>
          <div class="card-item-sub">Wintergreen Sessions &bull; Track 03</div>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

# Render the Apple TV Wintergreen experience
render(html_apple_wintergreen, OUT_DIR / "tv_apple_wintergreen.png")
