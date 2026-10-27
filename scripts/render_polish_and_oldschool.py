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
rob_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/rob.png"
samuel_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/samuel.jpg"
gdub_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/gdub.jpg"

# 1. State 1: Ultra-Polished Apple TV Style Dashboard (No emoji icons, pure refined typography)
html_apple_polish = f"""<!DOCTYPE html>
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
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
    display: flex;
    overflow: hidden;
  }}

  /* Minimal Left Navigation Bar - No Emojis, Pure Apple TV Typography */
  .sidebar {{
    width: 280px;
    background: rgba(14, 18, 26, 0.6);
    backdrop-filter: blur(40px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 56px 40px;
  }}
  .brand {{
    display: flex;
    align-items: flex-end;
    margin-bottom: 56px;
  }}
  .brand img {{
    height: 34px;
    object-fit: contain;
  }}
  .brand-tv {{
    font-size: 19px;
    font-weight: 800;
    margin-left: 10px;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    margin-bottom: 2px;
  }}

  .nav-group {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .nav-header {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: #5A6678;
    text-transform: uppercase;
    margin-bottom: 12px;
  }}
  .nav-item {{
    padding: 14px 20px;
    border-radius: 10px;
    font-size: 19px;
    font-weight: 600;
    color: #8C99A8;
    letter-spacing: 0.3px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 2px solid transparent;
  }}
  .nav-item.active {{
    background: #FFFFFF;
    color: #000000;
    font-weight: 700;
    box-shadow: 0 10px 25px rgba(255, 255, 255, 0.2);
  }}
  .radio-pulse {{
    width: 7px;
    height: 7px;
    background: #FF3B30;
    border-radius: 50%;
  }}

  .sidebar-footer {{
    font-size: 13px;
    color: #4A5568;
    letter-spacing: 1px;
    font-weight: 500;
  }}

  /* Main Apple TV Stage */
  .stage {{
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 56px 64px;
    position: relative;
    background: radial-gradient(circle at 60% 20%, #161D2B 0%, #080A0F 60%, #000000 100%);
  }}

  .header-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 32px;
  }}
  .title-main {{
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.5px;
  }}
  .title-sub {{
    font-size: 16px;
    color: #718096;
    margin-top: 6px;
    font-weight: 500;
  }}

  .content-grid {{
    display: grid;
    grid-template-columns: 1.8fr 1.2fr;
    gap: 36px;
    flex: 1;
    min-height: 0;
  }}

  /* Apple TV Cinematic Feature Card */
  .hero-card {{
    background: #0E121A;
    border-radius: 18px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }}
  .hero-card img {{
    position: absolute;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.9;
  }}
  .hero-gradient {{
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.4) 50%, transparent 100%);
  }}
  .hero-content {{
    position: relative;
    z-index: 2;
    padding: 40px;
  }}
  .channel-pill {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #FFFFFF;
    margin-bottom: 14px;
  }}
  .hero-title {{
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
    line-height: 1.2;
  }}
  .hero-meta {{
    font-size: 16px;
    color: #A0AEC0;
    margin-bottom: 24px;
    font-weight: 500;
  }}
  .tune-in-btn {{
    background: #FFFFFF;
    color: #000000;
    padding: 14px 28px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 700;
    border: none;
    letter-spacing: 0.5px;
    box-shadow: 0 10px 20px rgba(255, 255, 255, 0.15);
  }}

  /* Right Column: Radio & Music */
  .right-column {{
    display: flex;
    flex-direction: column;
    gap: 24px;
  }}

  .apple-card {{
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 28px;
    backdrop-filter: blur(20px);
  }}

  .card-label-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }}
  .card-label {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #718096;
    text-transform: uppercase;
  }}
  .live-badge {{
    background: #FF3B30;
    color: #FFFFFF;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
    padding: 3px 8px;
    border-radius: 4px;
  }}

  .radio-body {{
    display: flex;
    align-items: center;
    gap: 20px;
  }}
  .album-art {{
    width: 80px;
    height: 80px;
    border-radius: 10px;
    object-fit: cover;
    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
  }}
  .track-title {{
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .artist-name {{
    font-size: 14px;
    color: #A0AEC0;
    margin-bottom: 8px;
  }}
  .broadcast-clock {{
    font-size: 12px;
    color: #718096;
    font-variant-numeric: tabular-nums;
  }}

  /* Music Queue List */
  .music-card {{
    flex: 1;
    display: flex;
    flex-direction: column;
  }}
  .track-list {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 10px;
  }}
  .track-item {{
    display: flex;
    align-items: center;
    padding: 12px 14px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.02);
  }}
  .track-idx {{
    font-size: 13px;
    color: #4A5568;
    width: 28px;
    font-weight: 600;
  }}
  .track-details {{
    flex: 1;
  }}
  .track-name {{
    font-size: 15px;
    font-weight: 600;
  }}
  .track-artist {{
    font-size: 13px;
    color: #718096;
  }}

  .footer-hints {{
    margin-top: 28px;
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: #4A5568;
    letter-spacing: 1px;
  }}
</style>
</head>
<body>
  <!-- Sidebar -->
  <div class="sidebar">
    <div>
      <div class="brand">
        <img src="{logo_src}">
        <span class="brand-tv">tv</span>
      </div>

      <div class="nav-group">
        <div class="nav-header">Browse</div>
        <div class="nav-item active">
          <span>AHOY TV</span>
        </div>
        <div class="nav-item">
          <span>Radio</span>
          <span class="radio-pulse"></span>
        </div>
        <div class="nav-item">
          <span>Music</span>
        </div>
        <div class="nav-item">
          <span>Skating</span>
        </div>
        <div class="nav-item">
          <span>Podcasts</span>
        </div>
      </div>
    </div>

    <div class="sidebar-footer">
      Xbox Series X|S &bull; Controller Ready
    </div>
  </div>

  <!-- Main Apple TV Stage -->
  <div class="stage">
    <div class="header-row">
      <div>
        <div class="title-main">Independent Culture</div>
        <div class="title-sub">Scheduled broadcast channels, 24/7 synchronized indie radio, and on-demand music.</div>
      </div>
    </div>

    <div class="content-grid">
      <!-- Big Stage Hero -->
      <div class="hero-card">
        <img src="{rob_thumb}">
        <div class="hero-gradient"></div>
        <div class="hero-content">
          <div class="channel-pill">Channel 01 &bull; Ahoy Mix</div>
          <div class="hero-title">Rob Meglio's Sponsor Me Tape</div>
          <div class="hero-meta">Rob Meglio &bull; Skating &bull; Recorded live at Flux</div>
          <button class="tune-in-btn">Tune Into Channel</button>
        </div>
      </div>

      <!-- Right Stack -->
      <div class="right-column">
        <!-- Live Radio -->
        <div class="apple-card">
          <div class="card-label-row">
            <span class="card-label">Live Indie Radio</span>
            <span class="live-badge">ON AIR</span>
          </div>
          <div class="radio-body">
            <img class="album-art" src="{samuel_thumb}">
            <div>
              <div class="track-title">Seen Better Days</div>
              <div class="artist-name">Samuel Dylan Witch</div>
              <div class="broadcast-clock">Synchronized Worldwide Broadcast</div>
            </div>
          </div>
        </div>

        <!-- Music On Demand -->
        <div class="apple-card music-card">
          <div class="card-label-row">
            <span class="card-label">Recent Releases</span>
            <span style="font-size: 12px; color: #718096; font-weight: 600;">Play All</span>
          </div>
          <div class="track-list">
            <div class="track-item">
              <span class="track-idx">01</span>
              <div class="track-details">
                <div class="track-name">Beneath the Willow Tree</div>
                <div class="track-artist">Samuel Dylan Witch</div>
              </div>
            </div>
            <div class="track-item">
              <span class="track-idx">02</span>
              <div class="track-details">
                <div class="track-name">Reasons (Radio Edit)</div>
                <div class="track-artist">Fella Gazelle</div>
              </div>
            </div>
            <div class="track-item">
              <span class="track-idx">03</span>
              <div class="track-details">
                <div class="track-name">Which Discraft Putter is Best</div>
                <div class="track-artist">Greg Weese &bull; G-Dub</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-hints">
      <span>D-pad to Navigate &bull; Press A to Select</span>
      <span>Ahoy TV v0.2.0</span>
    </div>
  </div>
</body>
</html>
"""

# 2. State 2: "Old School TV" mode when you hit AHOY TV!
# Vintage cable OSD channel banner (green/white mono CRT font), scanline warmth, channel surfing guide
html_oldschool_tv = f"""<!DOCTYPE html>
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
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    position: relative;
    overflow: hidden;
  }}

  /* Fullscreen Vintage Broadcast Background */
  .broadcast-video {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: contrast(1.08) saturate(1.1);
  }}

  /* CRT Scanline and Vignette Overlay */
  .crt-overlay {{
    position: absolute;
    inset: 0;
    background: 
      linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
      radial-gradient(circle at 50% 50%, transparent 65%, rgba(0,0,0,0.7) 100%);
    background-size: 100% 4px, 100% 100%;
    pointer-events: none;
    z-index: 5;
  }}

  /* Vintage Top Right Channel Bug (Like 90s cable / MTV) */
  .channel-bug {{
    position: absolute;
    top: 48px;
    right: 64px;
    z-index: 10;
    display: flex;
    align-items: center;
    background: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 8px 18px;
    border-radius: 4px;
    font-family: "Courier New", Courier, monospace;
    color: #39FF14; /* Classic CRT Neon Green */
    text-shadow: 0 0 10px rgba(57, 255, 20, 0.7);
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 2px;
  }}
  .bug-live-dot {{
    width: 10px;
    height: 10px;
    background: #FF3B30;
    border-radius: 50%;
    margin-right: 12px;
    box-shadow: 0 0 8px #FF3B30;
  }}

  /* Classic Cable TV Bottom On-Screen Display (OSD Banner) */
  .tv-osd-banner {{
    position: absolute;
    bottom: 48px;
    left: 64px;
    right: 64px;
    z-index: 10;
    background: linear-gradient(180deg, rgba(8, 14, 28, 0.92) 0%, rgba(4, 7, 16, 0.98) 100%);
    border: 2px solid #3182CE;
    border-radius: 6px;
    padding: 24px 32px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.9), inset 0 0 15px rgba(49, 130, 206, 0.3);
  }}

  .osd-top-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    padding-bottom: 12px;
    margin-bottom: 14px;
    font-family: "Courier New", Courier, monospace;
  }}
  .channel-number {{
    font-size: 26px;
    font-weight: 900;
    color: #FEEBC8;
    letter-spacing: 2px;
  }}
  .channel-name {{
    font-size: 22px;
    color: #63B3ED;
    font-weight: 700;
    letter-spacing: 3px;
    margin-left: 16px;
  }}
  .osd-clock {{
    font-size: 20px;
    color: #FEEBC8;
    font-weight: 700;
    letter-spacing: 1px;
  }}
  .osd-tech-tags {{
    display: flex;
    gap: 12px;
    font-size: 13px;
    color: #A0AEC0;
  }}
  .tech-tag {{
    background: rgba(255, 255, 255, 0.1);
    padding: 2px 8px;
    border-radius: 2px;
  }}

  .osd-main-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .program-title {{
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.3px;
    margin-bottom: 4px;
  }}
  .program-meta {{
    font-size: 16px;
    color: #CBD5E0;
    font-weight: 500;
  }}
  .next-program-preview {{
    text-align: right;
    font-family: "Courier New", Courier, monospace;
  }}
  .next-label {{
    font-size: 12px;
    color: #ECC94B;
    letter-spacing: 1px;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .next-title {{
    font-size: 15px;
    color: #E2E8F0;
  }}

  /* Controller overlay hints */
  .channel-surf-hint {{
    position: absolute;
    top: 48px;
    left: 64px;
    z-index: 10;
    font-family: "Courier New", Courier, monospace;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    background: rgba(0, 0, 0, 0.6);
    padding: 8px 16px;
    border-radius: 4px;
    letter-spacing: 1px;
  }}
</style>
</head>
<body>
  <div class="crt-overlay"></div>

  <!-- Fullscreen Broadcast Video -->
  <img class="broadcast-video" src="{rob_thumb}">

  <!-- Top Left: Channel Surfer Hint -->
  <div class="channel-surf-hint">
    ▲ / ▼ D-PAD TO CHANGE CHANNEL &bull; B FOR GUIDE
  </div>

  <!-- Top Right: Classic CRT Channel Bug -->
  <div class="channel-bug">
    <div class="bug-live-dot"></div>
    <span>CH 01 &bull; AHOY TV &bull; STEREO</span>
  </div>

  <!-- Bottom: Classic Cable TV OSD Channel Banner -->
  <div class="tv-osd-banner">
    <div class="osd-top-row">
      <div style="display: flex; align-items: baseline;">
        <span class="channel-number">01</span>
        <span class="channel-name">AHOY MIX</span>
      </div>
      <div style="display: flex; align-items: center; gap: 24px;">
        <div class="osd-tech-tags">
          <span class="tech-tag">CABLE FEED</span>
          <span class="tech-tag">1080p HD</span>
          <span class="tech-tag">STEREO</span>
        </div>
        <span class="osd-clock">8:30 PM EDT</span>
      </div>
    </div>

    <div class="osd-main-row">
      <div>
        <div class="program-title">Rob Meglio's Sponsor Me Tape - October 2026</div>
        <div class="program-meta">Filmed at Flux &bull; Skating &bull; Tallboyz &bull; Runtime: 09:15</div>
      </div>
      <div class="next-program-preview">
        <div class="next-label">UP NEXT AT 8:39 PM</div>
        <div class="next-title">Samuel Dylan Witch — Stop and Rewind</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

print("Rendering Polish Apple TV Dashboard & Old School TV Experience...")
render(html_apple_polish, OUT_DIR / "tv_apple_polish.png")
render(html_oldschool_tv, OUT_DIR / "tv_oldschool_broadcast.png")
print("Done!")
