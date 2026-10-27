import base64
import subprocess
from pathlib import Path

ROOT = Path("/Users/agworkywork/ahoy-on-xbox")
LOGO_PATH = ROOT / "dist/store_assets/ahoy_official_white.png"
LOGO_B64 = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Ahoy TV — Subtle Broadcast</title>
  <style>
    :root {{
      --accent: #FF0060;
      --bg: #000000;
      --card-bg: rgba(22, 22, 26, 0.65);
      --card-border: rgba(255, 255, 255, 0.08);
      --text-main: #FFFFFF;
      --text-sub: #8E8E93;
      --text-tertiary: #545458;
      --ease: cubic-bezier(0.16, 1, 0.3, 1);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }}

    html, body {{
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      position: fixed;
      inset: 0;
      background: var(--bg);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif;
      -webkit-font-smoothing: antialiased;
    }}

    /* FULL-SCREEN LIVE BROADCAST CANVAS (FEELS LIKE A REAL TV) */
    .tv-stage {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      background: #000000;
      overflow: hidden;
    }}
    .live-stream-player {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.5s var(--ease), filter 0.5s var(--ease);
    }}
    .billboard-poster {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.35;
      pointer-events: none;
    }}

    /* SUBTLE CINEMATIC GRADIENT VIGNETTES */
    .top-vignette {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 120px;
      background: linear-gradient(to bottom, rgba(0, 0, 0, 0.75) 0%, rgba(0, 0, 0, 0.2) 60%, transparent 100%);
      pointer-events: none;
      z-index: 2;
    }}
    .bottom-vignette {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 520px;
      background: linear-gradient(to top, rgba(0, 0, 0, 0.94) 0%, rgba(0, 0, 0, 0.75) 50%, rgba(0, 0, 0, 0.25) 85%, transparent 100%);
      pointer-events: none;
      z-index: 2;
    }}

    /* MINIMAL TOP BAR: Subtle network watermark & clock */
    .top-osd {{
      position: absolute;
      top: 32px;
      left: 48px;
      right: 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 10;
    }}
    .brand-watermark {{
      display: flex;
      align-items: center;
      opacity: 0.85;
      transition: opacity 0.2s;
    }}
    .brand-logo-img {{
      height: 22px;
      object-fit: contain;
    }}
    .brand-tv-mark {{
      font-size: 14px;
      font-weight: 700;
      color: var(--accent);
      margin-left: 6px;
      letter-spacing: 0.5px;
    }}

    .top-status {{
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-sub);
    }}
    .live-pip {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      color: #FFFFFF;
    }}
    .live-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--accent);
    }}

    /* SUBTLE TV CHANNEL GUIDE (LOWER THIRD DOCK) */
    .guide-dock {{
      position: absolute;
      bottom: 32px;
      left: 48px;
      right: 48px;
      z-index: 10;
      display: flex;
      flex-direction: column;
    }}

    /* ON-SCREEN CURRENT AIRPLAY BANNER */
    .osd-channel-banner {{
      margin-bottom: 14px;
      display: flex;
      align-items: baseline;
      justify-content: space-between;
    }}
    .osd-title-group {{
      display: flex;
      align-items: baseline;
      gap: 14px;
    }}
    .osd-ch-pill {{
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.8px;
      color: var(--accent);
      text-transform: uppercase;
    }}
    .osd-program-title {{
      font-size: 26px;
      font-weight: 700;
      letter-spacing: -0.3px;
      color: #FFFFFF;
    }}
    .osd-host {{
      font-size: 14px;
      color: var(--text-sub);
      font-weight: 400;
    }}

    /* EPG CHANNEL MATRIX (Exactly 4 Canonical Channels) */
    .epg-channel-matrix {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      background: rgba(18, 18, 22, 0.5);
      backdrop-filter: blur(28px) saturate(160%);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 8px;
    }}

    /* Channel Row: Subtle, Apple-clean */
    .ch-row {{
      display: grid;
      grid-template-columns: 220px 1.4fr 1fr;
      gap: 14px;
      align-items: center;
      padding: 10px 14px;
      border-radius: 9px;
      cursor: pointer;
      position: relative;
      transition: background 0.18s var(--ease);
    }}
    .ch-row:hover {{
      background: rgba(255, 255, 255, 0.05);
    }}
    .ch-row.active {{
      background: rgba(255, 255, 255, 0.08);
    }}
    /* Left subtle accent indicator line for active channel */
    .ch-row.active::before {{
      content: "";
      position: absolute;
      left: 0;
      top: 10px;
      bottom: 10px;
      width: 3px;
      background: var(--accent);
      border-radius: 0 2px 2px 0;
    }}

    /* Channel Identity */
    .ch-id-col {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .ch-num {{
      font-size: 14px;
      font-weight: 700;
      color: var(--text-sub);
      width: 30px;
    }}
    .ch-row.active .ch-num {{
      color: var(--accent);
    }}
    .ch-name {{
      font-size: 15px;
      font-weight: 600;
      color: var(--text-main);
    }}

    /* Program Cells */
    .ch-now-cell {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      overflow: hidden;
      position: relative;
    }}
    .now-tag {{
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: var(--accent);
      margin-bottom: 2px;
      text-transform: uppercase;
    }}
    .prog-title {{
      font-size: 14px;
      font-weight: 500;
      color: #FFFFFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .prog-sub {{
      font-size: 12px;
      color: var(--text-sub);
      margin-top: 1px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .ch-next-cell {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      overflow: hidden;
    }}
    .next-tag {{
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: var(--text-tertiary);
      margin-bottom: 2px;
      text-transform: uppercase;
    }}
    .ch-next-cell .prog-title {{
      color: var(--text-sub);
    }}

    /* Subtle TV Controller Footer Hints */
    .guide-footer-hints {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 10px;
      padding: 0 6px;
      font-size: 12px;
      color: var(--text-tertiary);
    }}
    .hints-items {{
      display: flex;
      gap: 20px;
    }}
    .key-mark {{
      color: var(--text-sub);
      font-weight: 600;
      margin-right: 4px;
    }}
  </style>
</head>
<body>
  <!-- Fullscreen Live Broadcast Canvas -->
  <div class="tv-stage">
    <img id="posterBg" class="billboard-poster" src="" alt="" />
    <video id="mainVideo" class="live-stream-player" autoplay playsinline muted loop></video>
  </div>

  <div class="top-vignette"></div>
  <div class="bottom-vignette"></div>

  <!-- Minimal Top OSD: Watermark & Clock -->
  <header class="top-osd">
    <div class="brand-watermark">
      <img class="brand-logo-img" src="{LOGO_B64}" alt="AHOY" />
      <span class="brand-tv-mark">tv</span>
    </div>
    <div class="top-status">
      <div class="live-pip">
        <div class="live-dot"></div>
        <span>LIVE</span>
      </div>
      <span id="clockDisplay">10:32 PM</span>
    </div>
  </header>

  <!-- Lower-Third Subtle TV Guide Dock -->
  <div class="guide-dock">
    <!-- Active Stream Title Banner -->
    <div class="osd-channel-banner">
      <div class="osd-title-group">
        <span class="osd-ch-pill" id="osdChannel">CH 101 • LIVE SHOWS</span>
        <h1 class="osd-program-title" id="osdTitle">Whatnot - Sand - Live @ Wintergreen Sessions</h1>
        <span class="osd-host" id="osdHost">Wintergreen Studios</span>
      </div>
    </div>

    <!-- 4 Canonical Channels EPG Matrix -->
    <div class="epg-channel-matrix" id="channelMatrix"></div>

    <!-- Subtle Controller Hints -->
    <div class="guide-footer-hints">
      <div class="hints-items">
        <div><span class="key-mark">▲/▼</span> Surf Channels</div>
        <div><span class="key-mark">Enter</span> Fullscreen</div>
        <div><span class="key-mark">Space</span> Audio</div>
        <div><span class="key-mark">X</span> Save</div>
      </div>
      <div id="saveNotice">AHOY INDIE MEDIA • ALWAYS ON</div>
    </div>
  </div>

  <script>
    const CHANNELS = [
      {{
        id: "live-shows",
        number: "101",
        name: "Live Shows",
        tagline: "Wintergreen Sessions & Concerts",
        current: {{
          title: "Whatnot - Sand - Live @ Wintergreen Sessions",
          host: "Wintergreen Studios",
          url: "https://ahoycollection.s3.us-east-2.amazonaws.com/Whatnot+-+Sand+-+Live+%40+Wintergreen+Sessions.mp4",
          poster: "https://i.ytimg.com/vi/H6iranjvsNI/maxresdefault.jpg"
        }},
        next: {{
          title: "Whatnot - Running Away - Live @ Wintergreen",
          host: "Wintergreen Studios"
        }}
      }},
      {{
        id: "music-videos",
        number: "102",
        name: "Music Videos",
        tagline: "Premieres & Soundscapes",
        current: {{
          title: "Samuel Dylan Witch — Stop and Rewind",
          host: "Samuel Dylan Witch",
          url: "https://ahoycollection.s3.us-east-2.amazonaws.com/01%20I%27ve%20Seen%20Better%20Days.mp3",
          poster: "https://i.ytimg.com/vi/XDH0X-dF4GM/maxresdefault.jpg"
        }},
        next: {{
          title: "Put Me on the Run",
          host: "Samuel Dylan Witch"
        }}
      }},
      {{
        id: "films",
        number: "103",
        name: "Films",
        tagline: "Skate Tapes & Documentaries",
        current: {{
          title: "DC Shoes Skate Special",
          host: "DC Skate Collective",
          url: "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
          poster: "https://i.ytimg.com/vi/koPyEhqksBk/maxresdefault.jpg"
        }},
        next: {{
          title: "Tallboyz Series Premiere",
          host: "Tallboyz Comedy"
        }}
      }},
      {{
        id: "misc",
        number: "104",
        name: "Misc",
        tagline: "24/7 Mix & Curations",
        current: {{
          title: "Ahoy Mix 24/7 — Independent Culture Always On",
          host: "Ahoy Curators",
          url: "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
          poster: "https://i.ytimg.com/vi/grB5ydvYWW8/maxresdefault.jpg"
        }},
        next: {{
          title: "Dave Gunn — Poets & Friends Session",
          host: "Dave Gunn"
        }}
      }}
    ];

    let activeIndex = 0;
    const video = document.getElementById("mainVideo");
    const poster = document.getElementById("posterBg");
    const osdChannel = document.getElementById("osdChannel");
    const osdTitle = document.getElementById("osdTitle");
    const osdHost = document.getElementById("osdHost");
    const matrix = document.getElementById("channelMatrix");
    const clockDisplay = document.getElementById("clockDisplay");

    function updateClock() {{
      const now = new Date();
      clockDisplay.innerText = now.toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit' }});
    }}
    setInterval(updateClock, 1000);
    updateClock();

    function renderMatrix() {{
      matrix.innerHTML = "";
      CHANNELS.forEach((ch, idx) => {{
        const row = document.createElement("div");
        row.className = `ch-row ${{idx === activeIndex ? 'active' : ''}}`;
        row.innerHTML = `
          <div class="ch-id-col">
            <span class="ch-num">${{ch.number}}</span>
            <span class="ch-name">${{ch.name}}</span>
          </div>
          <div class="ch-now-cell">
            <span class="now-tag">On Now</span>
            <span class="prog-title">${{ch.current.title}}</span>
            <span class="prog-sub">${{ch.current.host}}</span>
          </div>
          <div class="ch-next-cell">
            <span class="next-tag">Up Next</span>
            <span class="prog-title">${{ch.next.title}}</span>
            <span class="prog-sub">${{ch.next.host}}</span>
          </div>
        `;
        row.addEventListener("click", () => tune(idx));
        matrix.appendChild(row);
      }});
    }}

    function tune(idx) {{
      activeIndex = idx;
      const ch = CHANNELS[idx];

      osdChannel.innerText = `CH ${{ch.number}} • ${{ch.name.toUpperCase()}}`;
      osdTitle.innerText = ch.current.title;
      osdHost.innerText = ch.current.host;
      poster.src = ch.current.poster;

      video.src = ch.current.url;
      video.play().catch(() => {{}});

      renderMatrix();
    }}

    window.addEventListener("keydown", (e) => {{
      if (e.key === "ArrowUp") {{
        e.preventDefault();
        tune((activeIndex - 1 + CHANNELS.length) % CHANNELS.length);
      }} else if (e.key === "ArrowDown") {{
        e.preventDefault();
        tune((activeIndex + 1) % CHANNELS.length);
      }} else if (e.key === " " || e.key === "m" || e.key === "M") {{
        e.preventDefault();
        video.muted = !video.muted;
      }} else if (e.key === "f" || e.key === "F" || e.key === "Enter") {{
        if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(() => {{}});
        else document.exitFullscreen().catch(() => {{}});
      }} else if (e.key === "x" || e.key === "X") {{
        const notice = document.getElementById("saveNotice");
        notice.innerText = `★ Saved to Library`;
        notice.style.color = "var(--accent)";
      }}
    }});

    window.addEventListener("click", () => {{
      if (video.muted) video.muted = false;
    }}, {{ once: true }});

    tune(0);
  </script>
</body>
</html>
"""

# Write to preview files
(ROOT / "dist/store_assets/tv_app_preview.html").write_text(html, encoding="utf-8")
(ROOT / "AhoyXbox/Web/index.html").write_text(html, encoding="utf-8")

# User open tab
user_tab = Path("/Users/agworkywork/.gemini/antigravity/brain/a90c34eb-a13f-49bc-822c-f79f8d44883c/ahoy_tv_frontend.html")
if user_tab.parent.exists():
    user_tab.write_text(html, encoding="utf-8")

print("Subtle TV files created!")
