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
rob_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/rob.png"
samuel_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/samuel.jpg"
gdub_thumb = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/thumbs/gdub.jpg"

html_pluto_live = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1920px;
    height: 1080px;
    background: #06090F;
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  /* Top 50%: Active Live Video Player Stage (Like Pluto TV) */
  .player-stage {{
    height: 520px;
    width: 100%;
    position: relative;
    background: #000000;
    overflow: hidden;
  }}
  .live-stream-video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 25%;
  }}
  .player-top-bar {{
    position: absolute;
    top: 28px;
    left: 48px;
    right: 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .brand-area {{
    display: flex;
    align-items: center;
  }}
  .brand-logo {{
    height: 28px;
    object-fit: contain;
  }}
  .brand-tv {{
    font-size: 15px;
    font-weight: 800;
    margin-left: 8px;
    color: #FFFFFF;
  }}
  .live-pill {{
    display: flex;
    align-items: center;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.5px;
  }}
  .live-red-dot {{
    width: 8px;
    height: 8px;
    background: #FF3B30;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 10px #FF3B30;
  }}

  .nav-tabs-bar {{
    display: flex;
    align-items: center;
    gap: 32px;
    background: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(20px);
    padding: 8px 24px;
    border-radius: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }}
  .nav-tab-item {{
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #94A3B8;
    text-transform: uppercase;
  }}
  .nav-tab-item.active {{
    color: #FFFFFF;
    border-bottom: 2px solid #FFFFFF;
    padding-bottom: 2px;
  }}

  /* Player Bottom Info Overlay */
  .player-bottom-overlay {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 24px 48px;
    background: linear-gradient(to top, rgba(6, 9, 15, 0.98) 0%, rgba(6, 9, 15, 0.6) 60%, transparent 100%);
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }}
  .stream-channel-info {{
    max-width: 900px;
  }}
  .stream-meta-line {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 6px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #64748B;
  }}
  .stream-channel-num {{
    background: #3B82F6;
    color: #FFFFFF;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
  }}
  .stream-title {{
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
  }}
  .stream-desc {{
    font-size: 14px;
    color: #94A3B8;
  }}
  .stream-controls-hint {{
    display: flex;
    gap: 16px;
    font-size: 13px;
    color: #94A3B8;
  }}
  .ctrl-badge {{
    background: rgba(255, 255, 255, 0.15);
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 700;
    color: #FFFFFF;
    margin-right: 6px;
  }}

  /* Bottom 50%: Pluto TV Live EPG Channel Guide */
  .guide-container {{
    flex: 1;
    background: #06090F;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    flex-direction: column;
    padding: 16px 48px 24px 48px;
  }}

  /* Timeline Header */
  .timeline-header {{
    display: grid;
    grid-template-columns: 280px 1.2fr 1fr;
    gap: 16px;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #64748B;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 8px;
  }}

  /* Channel Guide Rows */
  .channel-row {{
    display: grid;
    grid-template-columns: 280px 1.2fr 1fr;
    gap: 16px;
    align-items: center;
    margin-bottom: 10px;
  }}

  /* Channel Identity Column */
  .channel-id-cell {{
    display: flex;
    align-items: center;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
  }}
  .ch-num {{
    font-size: 18px;
    font-weight: 800;
    color: #60A5FA;
    width: 36px;
  }}
  .ch-name-wrap {{
    flex: 1;
  }}
  .ch-name {{
    font-size: 16px;
    font-weight: 700;
  }}
  .ch-sub {{
    font-size: 11px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  /* Program Slot (NOW / NEXT) */
  .program-slot {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 14px 20px;
    position: relative;
    overflow: hidden;
    height: 72px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
  .program-slot.live-active {{
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid #FFFFFF;
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
  }}
  .slot-progress-bar {{
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;
    background: #3B82F6;
    width: 58%;
  }}
  .slot-title {{
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .slot-time {{
    font-size: 12px;
    color: #94A3B8;
  }}

  /* Bottom status strip */
  .guide-footer {{
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    color: #475569;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }}
</style>
</head>
<body>

  <!-- Top Active Live Player Stage -->
  <div class="player-stage">
    <img class="live-stream-video" src="{ep1_thumb}">

    <!-- Top Bar -->
    <div class="player-top-bar">
      <div class="brand-area">
        <img class="brand-logo" src="{logo_src}">
        <span class="brand-tv">tv</span>
      </div>

      <div class="nav-tabs-bar">
        <span class="nav-tab-item active">Live TV Guide</span>
        <span class="nav-tab-item">Radio</span>
        <span class="nav-tab-item">Music</span>
        <span class="nav-tab-item">Saved</span>
      </div>

      <div class="live-pill">
        <span class="live-red-dot"></span>
        <span>PLUTO-STYLE LIVE FEED</span>
      </div>
    </div>

    <!-- Live Player Bottom Info -->
    <div class="player-bottom-overlay">
      <div class="stream-channel-info">
        <div class="stream-meta-line">
          <span class="stream-channel-num">CH 01</span>
          <span>WINTERGREEN STUDIOS</span>
          <span>&bull;</span>
          <span>NOW PLAYING LIVE (8:30 PM - 8:45 PM)</span>
        </div>
        <div class="stream-title">Wintergreen Sessions Episode 1: Whatnot</div>
        <div class="stream-desc">Live performance recorded in CT &bull; Featuring debut live tracks & reworked EP favorites &bull; Stereo HD</div>
      </div>

      <div class="stream-controls-hint">
        <span><span class="ctrl-badge">A</span> Tune Channel</span>
        <span><span class="ctrl-badge">B</span> Toggle Fullscreen</span>
        <span><span class="ctrl-badge">X</span> Save Show</span>
      </div>
    </div>
  </div>

  <!-- Bottom Pluto TV Live Channel Guide (EPG) -->
  <div class="guide-container">
    <div class="timeline-header">
      <span>Channel</span>
      <span>On Now (8:30 PM)</span>
      <span>Up Next (8:45 PM)</span>
    </div>

    <!-- Channel 01 (Currently Playing & Focused) -->
    <div class="channel-row">
      <div class="channel-id-cell" style="border-left: 4px solid #3B82F6;">
        <span class="ch-num">01</span>
        <div class="ch-name-wrap">
          <div class="ch-name">Wintergreen Studios</div>
          <div class="ch-sub">Live Sessions &bull; 24/7</div>
        </div>
      </div>
      <div class="program-slot live-active">
        <div class="slot-title">Episode 1: Whatnot (Live Session)</div>
        <div class="slot-time">8:30 PM - 8:45 PM &bull; 9 mins remaining</div>
        <div class="slot-progress-bar"></div>
      </div>
      <div class="program-slot">
        <div class="slot-title">Whatnot — Sand (Live Session)</div>
        <div class="slot-time">8:45 PM - 8:50 PM</div>
      </div>
    </div>

    <!-- Channel 02 (Ahoy Mix) -->
    <div class="channel-row">
      <div class="channel-id-cell">
        <span class="ch-num">02</span>
        <div class="ch-name-wrap">
          <div class="ch-name">Ahoy Mix</div>
          <div class="ch-sub">Curated Stream</div>
        </div>
      </div>
      <div class="program-slot">
        <div class="slot-title">Samuel Dylan Witch — Stop and Rewind</div>
        <div class="slot-time">8:28 PM - 8:33 PM</div>
      </div>
      <div class="program-slot">
        <div class="slot-title">Poets & Friends #13 — Opening Remarks</div>
        <div class="slot-time">8:33 PM - 8:48 PM</div>
      </div>
    </div>

    <!-- Channel 03 (Skating) -->
    <div class="channel-row">
      <div class="channel-id-cell">
        <span class="ch-num">03</span>
        <div class="ch-name-wrap">
          <div class="ch-name">Skate Network</div>
          <div class="ch-sub">Tallboyz &bull; Street</div>
        </div>
      </div>
      <div class="program-slot">
        <div class="slot-title">Rob Meglio's Sponsor Me Tape</div>
        <div class="slot-time">8:20 PM - 8:35 PM</div>
      </div>
      <div class="program-slot">
        <div class="slot-time">Flux Street Session #12</div>
        <div class="slot-time">8:35 PM - 8:55 PM</div>
      </div>
    </div>

    <!-- Channel 04 (G-Dub Disc Golf) -->
    <div class="channel-row">
      <div class="channel-id-cell">
        <span class="ch-num">04</span>
        <div class="ch-name-wrap">
          <div class="ch-name">G-Dub Disc Golf</div>
          <div class="ch-sub">Tours &bull; Reviews</div>
        </div>
      </div>
      <div class="program-slot">
        <div class="slot-title">Which Discraft Putter is Best</div>
        <div class="slot-time">8:15 PM - 8:35 PM</div>
      </div>
      <div class="program-slot">
        <div class="slot-title">Road Trip Series: Georgia Trip</div>
        <div class="slot-time">8:35 PM - 9:05 PM</div>
      </div>
    </div>

    <!-- Guide Footer -->
    <div class="guide-footer">
      <span>▲ / ▼ Change Channel &bull; ◄ / ► Browse Schedule &bull; A to Watch &bull; B Fullscreen</span>
      <span>Instant Live Streaming &bull; Pluto TV Inspired Guide</span>
    </div>
  </div>

</body>
</html>
"""

render(html_pluto_live, OUT_DIR / "tv_pluto_live.png")
print("Pluto TV Live Experience Generated!")
