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
samuel_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/samuel.jpg"
rob_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/rob.png"
gdub_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/gdub.jpg"

# 1. Main Hub: Core Features: TV - RADIO - MUSIC - SAVED
html_main_core = f"""<!DOCTYPE html>
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

  /* Apple TV Floating Top Navigation Bar: TV - RADIO - MUSIC - SAVED */
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
    gap: 48px;
  }}
  .nav-tab {{
    font-size: 19px;
    font-weight: 600;
    color: #98A2B3;
    letter-spacing: 0.5px;
    position: relative;
    padding: 6px 0;
    text-transform: uppercase;
  }}
  .nav-tab.active {{
    color: #FFFFFF;
    font-weight: 800;
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
    box-shadow: 0 10px 25px rgba(255, 255, 255, 0.25);
  }}
  .btn-save {{
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #FFFFFF;
    padding: 16px 28px;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .controller-btn-badge {{
    background: #3182CE;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 4px;
    margin-left: 6px;
  }}

  /* Bottom Shelf */
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

  <!-- Apple TV Navigation Header: TV - RADIO - MUSIC - SAVED -->
  <div class="nav-header">
    <div class="brand-logo-wrap">
      <img src="{logo_src}">
      <span class="brand-tv-pill">tv</span>
    </div>

    <div class="nav-tabs">
      <div class="nav-tab active">TV</div>
      <div class="nav-tab">Radio</div>
      <div class="nav-tab">Music</div>
      <div class="nav-tab">Saved</div>
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
      <span>&bull;</span>
      <span>Live Studio Recording</span>
    </div>
    <div class="hero-title">Wintergreen Sessions: Whatnot</div>
    <div class="hero-synopsis">
      Live studio session recorded in Connecticut with Kicker Pictures. Raw indie rock performances featuring unreleased debuts and reworked classics captured in master audio.
    </div>
    <div class="hero-actions">
      <button class="btn-primary">▶ &nbsp;Play Episode</button>
      <button class="btn-save">
        <span>+ Save to Library</span>
        <span class="controller-btn-badge">X</span>
      </button>
    </div>
  </div>

  <!-- Apple TV Shelf -->
  <div class="shelf-container">
    <div class="shelf-header">
      <div class="shelf-title">Featured Episodes &bull; Wintergreen Studios</div>
      <div class="shelf-count">4 Tracks &bull; Live Performances</div>
    </div>

    <div class="shelf-row">
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

# 2. Saved Screen: User's Bookmarks / Saved Library Screen
html_saved_screen = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1920px;
    height: 1080px;
    background: radial-gradient(circle at 50% 10%, #111726 0%, #06090F 60%, #000000 100%);
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif;
    padding: 44px 80px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
  }}

  /* Top Nav */
  .nav-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 40px;
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
    gap: 48px;
  }}
  .nav-tab {{
    font-size: 19px;
    font-weight: 600;
    color: #98A2B3;
    letter-spacing: 0.5px;
    position: relative;
    padding: 6px 0;
    text-transform: uppercase;
  }}
  .nav-tab.active {{
    color: #FFFFFF;
    font-weight: 800;
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

  .saved-summary-pill {{
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 13px;
    color: #CBD5E1;
  }}

  /* Saved Page Header */
  .saved-title-row {{
    margin-bottom: 32px;
  }}
  .page-title {{
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
  }}
  .page-sub {{
    font-size: 16px;
    color: #64748B;
  }}

  /* Saved Items Grid */
  .saved-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 28px;
    flex: 1;
  }}
  .saved-card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
  }}
  .saved-card.focused {{
    transform: scale(1.04);
    border: 2px solid #FFFFFF;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.9), 0 0 20px rgba(255, 255, 255, 0.3);
  }}
  .saved-card-img {{
    width: 100%;
    height: 190px;
    object-fit: cover;
    position: relative;
  }}
  .saved-type-badge {{
    position: absolute;
    top: 12px;
    left: 12px;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #F8FAFC;
  }}
  .saved-body {{
    padding: 18px 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .saved-item-title {{
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .saved-item-sub {{
    font-size: 13px;
    color: #64748B;
  }}
  .saved-date {{
    font-size: 11px;
    color: #475569;
    margin-top: 10px;
  }}

  /* Footer */
  .footer-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 20px;
    font-size: 14px;
    color: #475569;
  }}
</style>
</head>
<body>

  <!-- Top Nav -->
  <div class="nav-header">
    <div class="brand-logo-wrap">
      <img src="{logo_src}">
      <span class="brand-tv-pill">tv</span>
    </div>

    <div class="nav-tabs">
      <div class="nav-tab">TV</div>
      <div class="nav-tab">Radio</div>
      <div class="nav-tab">Music</div>
      <div class="nav-tab active">Saved</div>
    </div>

    <div class="saved-summary-pill">
      <span>4 Items Saved &bull; Stored Locally</span>
    </div>
  </div>

  <!-- Title -->
  <div class="saved-title-row">
    <div class="page-title">Saved Library</div>
    <div class="page-sub">Your personal bookmarks across Ahoy TV, Radio stations, and Music tracks.</div>
  </div>

  <!-- Saved Items Grid -->
  <div class="saved-grid">
    <!-- Item 1 (Video) -->
    <div class="saved-card focused">
      <div style="position: relative;">
        <img class="saved-card-img" src="{ep1_thumb}">
        <span class="saved-type-badge">TV Episode</span>
      </div>
      <div class="saved-body">
        <div>
          <div class="saved-item-title">Wintergreen Sessions: Whatnot</div>
          <div class="saved-item-sub">Wintergreen Studios &bull; 14:28</div>
        </div>
        <div class="saved-date">Saved to Xbox &bull; Oct 26</div>
      </div>
    </div>

    <!-- Item 2 (Music Track) -->
    <div class="saved-card">
      <div style="position: relative;">
        <img class="saved-card-img" src="{samuel_thumb}">
        <span class="saved-type-badge">Music Track</span>
      </div>
      <div class="saved-body">
        <div>
          <div class="saved-item-title">Seen Better Days</div>
          <div class="saved-item-sub">Samuel Dylan Witch &bull; Indie</div>
        </div>
        <div class="saved-date">Saved to Xbox &bull; Oct 26</div>
      </div>
    </div>

    <!-- Item 3 (Skate Tape) -->
    <div class="saved-card">
      <div style="position: relative;">
        <img class="saved-card-img" src="{rob_thumb}">
        <span class="saved-type-badge">Skate Tape</span>
      </div>
      <div class="saved-body">
        <div>
          <div class="saved-item-title">Rob Meglio's Sponsor Me Tape</div>
          <div class="saved-item-sub">Rob Meglio &bull; Tallboyz</div>
        </div>
        <div class="saved-date">Saved to Xbox &bull; Oct 26</div>
      </div>
    </div>

    <!-- Item 4 (Live Performance) -->
    <div class="saved-card">
      <div style="position: relative;">
        <img class="saved-card-img" src="{sand_thumb}">
        <span class="saved-type-badge">Performance</span>
      </div>
      <div class="saved-body">
        <div>
          <div class="saved-item-title">Whatnot — Sand</div>
          <div class="saved-item-sub">Wintergreen Studios &bull; Track 01</div>
        </div>
        <div class="saved-date">Saved to Xbox &bull; Oct 26</div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer-bar">
    <span>D-pad to Browse &bull; Press A to Play &bull; Press X to Remove &bull; Press B to Back</span>
    <span>Local Favorites &bull; No Sign-In Required</span>
  </div>

</body>
</html>
"""

print("Rendering Core Features (TV, Radio, Music, Saved) & Saved Library Screen...")
render(html_main_core, OUT_DIR / "tv_core_features.png")
render(html_saved_screen, OUT_DIR / "tv_saved_screen.png")
print("Done!")
