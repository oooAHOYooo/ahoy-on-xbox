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
  <title>Ahoy TV — Apple Design • #FF0060</title>
  <style>
    :root {{
      --accent: #FF0060;
      --accent-glow: rgba(255, 0, 96, 0.4);
      --accent-dim: rgba(255, 0, 96, 0.15);
      --glass-surface: rgba(18, 20, 28, 0.75);
      --glass-border: rgba(255, 255, 255, 0.12);
      --glass-specular: inset 0 1px 1px rgba(255, 255, 255, 0.25);
      --glass-shadow: 0 20px 48px rgba(0, 0, 0, 0.7);
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
      background: #000000;
      color: #FFFFFF;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif;
      -webkit-font-smoothing: antialiased;
    }}

    /* Subtle Apple ambient glass glow */
    .ambient-glow {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 0;
      overflow: hidden;
    }}
    .orb {{
      position: absolute;
      border-radius: 50%;
      filter: blur(160px);
      opacity: 0.22;
      pointer-events: none;
    }}
    .orb-1 {{ width: 650px; height: 650px; top: -140px; left: 15%; background: radial-gradient(circle, #FF0060, transparent 70%); }}
    .orb-2 {{ width: 500px; height: 500px; bottom: 0%; right: 10%; background: radial-gradient(circle, #7928CA, transparent 70%); opacity: 0.18; }}

    /* Root Frame */
    .tv-root {{
      position: relative;
      z-index: 1;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      padding: 24px 44px 20px 44px;
    }}

    /* TOP BAR: APPLE TV GLASS HEADER */
    .header-bar {{
      height: 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
      flex-shrink: 0;
    }}

    .brand-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-pill {{
      display: flex;
      align-items: center;
      padding: 8px 18px;
      background: var(--glass-surface);
      backdrop-filter: blur(32px) saturate(180%);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-specular), 0 8px 24px rgba(0, 0, 0, 0.5);
      border-radius: 30px;
    }}
    .brand-logo-img {{
      height: 24px;
      object-fit: contain;
      display: block;
    }}
    .brand-tv-mark {{
      font-size: 15px;
      font-weight: 800;
      color: var(--accent);
      margin-left: 8px;
      letter-spacing: 0.5px;
    }}

    .live-indicator {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: var(--accent-dim);
      border: 1px solid var(--accent);
      box-shadow: 0 0 16px var(--accent-glow);
      border-radius: 20px;
      backdrop-filter: blur(20px);
    }}
    .live-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 10px var(--accent);
      animation: pulse 1.6s infinite ease-in-out;
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}
    .live-text {{
      font-size: 11px;
      font-weight: 900;
      letter-spacing: 1.5px;
      color: #FFFFFF;
    }}

    /* 4 CANONICAL CHANNELS PILL TABS */
    .tabs-pill-bar {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(20, 24, 34, 0.65);
      backdrop-filter: blur(36px) saturate(190%);
      padding: 5px 6px;
      border-radius: 40px;
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-specular), 0 8px 28px rgba(0, 0, 0, 0.5);
    }}
    .tab-btn {{
      padding: 8px 22px;
      border-radius: 30px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.3px;
      color: #94A3B8;
      background: transparent;
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.25s var(--ease);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .tab-btn:hover {{
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.06);
    }}
    .tab-btn.active {{
      color: #FFFFFF;
      background: linear-gradient(135deg, rgba(255, 0, 96, 0.3) 0%, rgba(255, 0, 96, 0.15) 100%);
      border: 1px solid var(--accent);
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.6), 0 0 20px var(--accent-glow);
    }}
    .tab-num {{
      font-size: 11px;
      font-weight: 800;
      color: var(--accent);
      opacity: 0.9;
    }}

    .top-meta-pill {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 8px 18px;
      background: var(--glass-surface);
      backdrop-filter: blur(32px);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-specular);
      border-radius: 30px;
      font-size: 13px;
      font-weight: 600;
      color: #94A3B8;
    }}
    .hdr-badge {{
      background: var(--accent-dim);
      border: 1px solid rgba(255, 0, 96, 0.4);
      color: var(--accent);
      font-size: 10px;
      font-weight: 900;
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 0.8px;
    }}

    /* MAIN STAGE: Top Live Player 46%, Bottom EPG Guide 54% */
    .main-stage {{
      flex: 1;
      display: grid;
      grid-template-rows: 46fr 54fr;
      gap: 16px;
      min-height: 0;
      overflow: hidden;
    }}

    /* TOP ROW: APPLE LIVE PLAYER VIEWPORT */
    .player-card {{
      position: relative;
      background: #000000;
      border-radius: 18px;
      overflow: hidden;
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-specular), var(--glass-shadow);
      display: flex;
      flex-direction: column;
    }}
    .video-viewport {{
      width: 100%;
      height: 100%;
      position: relative;
      background: #000000;
    }}
    .live-video {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .billboard-poster {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.35;
      filter: blur(2px);
      pointer-events: none;
    }}

    .player-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 20px 32px;
      background: linear-gradient(to top, rgba(0, 0, 0, 0.96) 0%, rgba(0, 0, 0, 0.6) 65%, transparent 100%);
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      backdrop-filter: blur(10px);
    }}
    .playing-info {{
      max-width: 900px;
    }}
    .channel-callout {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 1.2px;
      color: var(--accent);
      margin-bottom: 6px;
      text-transform: uppercase;
    }}
    .playing-title {{
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.4px;
      color: #FFFFFF;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .playing-desc {{
      font-size: 14px;
      color: #94A3B8;
      margin-top: 4px;
      font-weight: 400;
    }}

    .player-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .glass-btn {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 18px;
      background: rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2);
      border-radius: 10px;
      color: #FFFFFF;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s var(--ease);
    }}
    .glass-btn:hover, .glass-btn.focused {{
      background: #FFFFFF;
      color: #000000;
      box-shadow: 0 0 25px rgba(255, 255, 255, 0.5);
      border-color: #FFFFFF;
    }}
    .glass-btn.primary {{
      background: linear-gradient(135deg, rgba(255, 0, 96, 0.45) 0%, rgba(255, 0, 96, 0.25) 100%);
      border-color: var(--accent);
      box-shadow: 0 0 20px var(--accent-glow);
    }}

    /* BOTTOM ROW: APPLE EPG CHANNEL GUIDE */
    .guide-card {{
      background: var(--glass-surface);
      backdrop-filter: blur(36px) saturate(190%);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-specular), var(--glass-shadow);
      border-radius: 18px;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      min-height: 0;
    }}

    .guide-header-row {{
      display: grid;
      grid-template-columns: 280px 1fr 1fr;
      gap: 16px;
      padding: 0 12px 10px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.5px;
      color: #64748B;
      text-transform: uppercase;
    }}

    .guide-channels-list {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 8px;
      overflow-y: auto;
      padding: 10px 4px 4px 4px;
    }}
    .guide-channels-list::-webkit-scrollbar {{
      width: 4px;
    }}
    .guide-channels-list::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.15);
      border-radius: 4px;
    }}

    /* CHANNEL ROW */
    .channel-row {{
      display: grid;
      grid-template-columns: 280px 1fr 1fr;
      gap: 16px;
      align-items: center;
      cursor: pointer;
      transition: all 0.2s var(--ease);
    }}

    .channel-badge-cell {{
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 12px 16px;
      background: rgba(255, 255, 255, 0.03);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      transition: all 0.2s var(--ease);
    }}
    .channel-row.active .channel-badge-cell {{
      background: linear-gradient(135deg, rgba(255, 0, 96, 0.22) 0%, rgba(255, 0, 96, 0.08) 100%);
      border-color: var(--accent);
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.4), 0 0 24px var(--accent-glow);
    }}
    .ch-index {{
      font-size: 16px;
      font-weight: 900;
      color: var(--accent);
      min-width: 32px;
    }}
    .ch-name-wrap {{
      flex: 1;
      overflow: hidden;
    }}
    .ch-name {{
      font-size: 15px;
      font-weight: 800;
      color: #FFFFFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .ch-tagline {{
      font-size: 11px;
      color: #94A3B8;
      margin-top: 2px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .schedule-slot {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 12px 18px;
      background: rgba(255, 255, 255, 0.03);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.06);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      height: 64px;
      position: relative;
      overflow: hidden;
      transition: all 0.2s var(--ease);
    }}
    .channel-row.active .schedule-slot.now-slot {{
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 0, 96, 0.4);
    }}
    .slot-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 1px;
      color: var(--accent);
      margin-bottom: 2px;
      text-transform: uppercase;
    }}
    .slot-meta.next-meta {{
      color: #64748B;
    }}
    .slot-title {{
      font-size: 14px;
      font-weight: 700;
      color: #FFFFFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .slot-host {{
      font-size: 12px;
      color: #94A3B8;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .slot-progress-bar {{
      position: absolute;
      bottom: 0;
      left: 0;
      height: 3px;
      background: var(--accent);
      box-shadow: 0 0 10px var(--accent);
      border-radius: 0 2px 2px 0;
    }}

    /* FOOTER BAR */
    .footer-bar {{
      height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 10px;
      flex-shrink: 0;
      padding: 0 4px;
    }}
    .hints-group {{
      display: flex;
      align-items: center;
      gap: 18px;
      font-size: 12px;
      color: #94A3B8;
    }}
    .key-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 2px 7px;
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.22);
      border-radius: 5px;
      font-size: 11px;
      font-weight: 800;
      color: #FFFFFF;
      margin-right: 6px;
    }}
    .footer-status {{
      font-size: 12px;
      font-weight: 600;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="ambient-glow">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
  </div>

  <div class="tv-root">
    <!-- Top Bar: Official Ahoy Logo + tv Mark in #FF0060 -->
    <header class="header-bar">
      <div class="brand-group">
        <div class="brand-pill">
          <img class="brand-logo-img" src="{LOGO_B64}" alt="AHOY" />
          <span class="brand-tv-mark">tv</span>
        </div>
        <div class="live-indicator">
          <div class="live-dot"></div>
          <span class="live-text">LIVE</span>
        </div>
      </div>

      <!-- 4 Canonical Channels (Matches app.ahoy.ooo) -->
      <nav class="tabs-pill-bar" id="pillTabs">
        <button class="tab-btn active" data-index="0">
          <span class="tab-num">101</span> Live Shows
        </button>
        <button class="tab-btn" data-index="1">
          <span class="tab-num">102</span> Music Videos
        </button>
        <button class="tab-btn" data-index="2">
          <span class="tab-num">103</span> Films
        </button>
        <button class="tab-btn" data-index="3">
          <span class="tab-num">104</span> Misc
        </button>
      </nav>

      <div class="top-meta-pill">
        <span class="hdr-badge">4K HDR</span>
        <span id="clockDisplay">10:24 PM</span>
      </div>
    </header>

    <!-- Main Content Stage: Top Player, Bottom Apple EPG Guide -->
    <main class="main-stage">
      <section class="player-card">
        <div class="video-viewport">
          <img id="posterBg" class="billboard-poster" src="" alt="" />
          <video id="mainVideo" class="live-video" autoplay playsinline muted loop></video>

          <div class="player-overlay">
            <div class="playing-info">
              <div class="channel-callout">
                <span id="calloutCh">CH 101 • LIVE SHOWS</span>
                <span>•</span>
                <span>CONTINUOUS BROADCAST</span>
              </div>
              <h1 id="streamTitle" class="playing-title">Loading live broadcast...</h1>
              <p id="streamDesc" class="playing-desc">Direct transmission from Ahoy Indie Media.</p>
            </div>

            <div class="player-actions">
              <button class="glass-btn" id="btnAudio">
                <span id="audioIcon">🔇</span> <span id="audioLabel">Unmute Audio</span>
              </button>
              <button class="glass-btn primary" id="btnFullscreen">
                <span>⛶</span> Fullscreen [F]
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 4-Channel Apple EPG Guide -->
      <section class="guide-card">
        <div class="guide-header-row">
          <div>Channel (4 Total)</div>
          <div>On Now (Airplay)</div>
          <div>Up Next in Rotation</div>
        </div>

        <div class="guide-channels-list" id="channelGuideList"></div>
      </section>
    </main>

    <!-- Footer Controller Hints -->
    <footer class="footer-bar">
      <div class="hints-group">
        <div><span class="key-badge">D-PAD</span> Surf Channels</div>
        <div><span class="key-badge">[A] / ENTER</span> Fullscreen / Watch</div>
        <div><span class="key-badge">[B] / ESC</span> Exit Fullscreen to Guide</div>
        <div><span class="key-badge">[X]</span> Bookmark / Save</div>
        <div><span class="key-badge">SPACE</span> Toggle Audio</div>
      </div>
      <div class="footer-status" id="saveStatus">
        Ahoy TV OS • Apple Design • #FF0060 Accent
      </div>
    </footer>
  </div>

  <script>
    const CHANNELS = [
      {{
        id: "live-shows",
        number: "101",
        name: "Live Shows",
        tagline: "Wintergreen Sessions & Live Concerts",
        current: {{
          title: "Whatnot - Sand - Live @ Wintergreen Sessions",
          host: "Wintergreen Studios",
          desc: "Whatnot performs their viral indie single live from Wintergreen Sessions Episode 1.",
          url: "https://ahoycollection.s3.us-east-2.amazonaws.com/Whatnot+-+Sand+-+Live+%40+Wintergreen+Sessions.mp4",
          poster: "https://i.ytimg.com/vi/H6iranjvsNI/maxresdefault.jpg"
        }},
        next: {{
          title: "Whatnot - Running Away - Live @ Wintergreen",
          host: "Wintergreen Studios",
          time: "Next in Queue"
        }}
      }},
      {{
        id: "music-videos",
        number: "102",
        name: "Music Videos",
        tagline: "Premieres, Visuals & Soundscapes",
        current: {{
          title: "Samuel Dylan Witch — Stop and Rewind",
          host: "Samuel Dylan Witch",
          desc: "Independent music video premiere directed by Ahoy Indie Media.",
          url: "https://ahoycollection.s3.us-east-2.amazonaws.com/01%20I%27ve%20Seen%20Better%20Days.mp3",
          poster: "https://i.ytimg.com/vi/XDH0X-dF4GM/maxresdefault.jpg"
        }},
        next: {{
          title: "Put Me on the Run",
          host: "Samuel Dylan Witch",
          time: "Next in Queue"
        }}
      }},
      {{
        id: "films",
        number: "103",
        name: "Films",
        tagline: "Skate Tapes, Documentaries & Shorts",
        current: {{
          title: "DC Shoes Skate Special",
          host: "DC Skate Collective",
          desc: "High octane street and park skate tape recorded across urban terrain.",
          url: "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
          poster: "https://i.ytimg.com/vi/koPyEhqksBk/maxresdefault.jpg"
        }},
        next: {{
          title: "Tallboyz Series Premiere",
          host: "Tallboyz Comedy",
          time: "Next in Queue"
        }}
      }},
      {{
        id: "misc",
        number: "104",
        name: "Misc",
        tagline: "Continuous Cultural Mix & Curations",
        current: {{
          title: "Ahoy Mix 24/7 — Independent Culture Always On",
          host: "Ahoy Curators",
          desc: "The heartbeat of independent arts, comedy, poetry and studio sessions.",
          url: "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
          poster: "https://i.ytimg.com/vi/grB5ydvYWW8/maxresdefault.jpg"
        }},
        next: {{
          title: "Dave Gunn — Poets & Friends Session",
          host: "Dave Gunn",
          time: "Next in Queue"
        }}
      }}
    ];

    let activeChannelIdx = 0;
    const video = document.getElementById("mainVideo");
    const posterBg = document.getElementById("posterBg");
    const streamTitle = document.getElementById("streamTitle");
    const streamDesc = document.getElementById("streamDesc");
    const calloutCh = document.getElementById("calloutCh");
    const channelGuideList = document.getElementById("channelGuideList");
    const pillTabs = document.getElementById("pillTabs");
    const btnAudio = document.getElementById("btnAudio");
    const audioLabel = document.getElementById("audioLabel");
    const audioIcon = document.getElementById("audioIcon");
    const btnFullscreen = document.getElementById("btnFullscreen");
    const clockDisplay = document.getElementById("clockDisplay");

    function updateClock() {{
      const now = new Date();
      clockDisplay.innerText = now.toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit' }});
    }}
    setInterval(updateClock, 1000);
    updateClock();

    function renderGuide() {{
      channelGuideList.innerHTML = "";
      CHANNELS.forEach((ch, idx) => {{
        const row = document.createElement("div");
        row.className = `channel-row ${{idx === activeChannelIdx ? 'active' : ''}}`;
        row.dataset.index = idx;
        row.innerHTML = `
          <div class="channel-badge-cell">
            <span class="ch-index">${{ch.number}}</span>
            <div class="ch-name-wrap">
              <div class="ch-name">${{ch.name}}</div>
              <div class="ch-tagline">${{ch.tagline}}</div>
            </div>
          </div>
          <div class="schedule-slot now-slot">
            <div class="slot-meta">● ON AIR NOW</div>
            <div class="slot-title">${{ch.current.title}}</div>
            <div class="slot-host">${{ch.current.host}}</div>
            <div class="slot-progress-bar" style="width: 62%;"></div>
          </div>
          <div class="schedule-slot">
            <div class="slot-meta next-meta">UP NEXT</div>
            <div class="slot-title">${{ch.next.title}}</div>
            <div class="slot-host">${{ch.next.host}}</div>
          </div>
        `;
        row.addEventListener("click", () => tuneChannel(idx));
        channelGuideList.appendChild(row);
      }});

      const tabBtns = pillTabs.querySelectorAll(".tab-btn");
      tabBtns.forEach((btn, idx) => {{
        btn.classList.toggle("active", idx === activeChannelIdx);
      }});
    }}

    function tuneChannel(index) {{
      activeChannelIdx = index;
      const ch = CHANNELS[index];

      calloutCh.innerText = `CH ${{ch.number}} • ${{ch.name.toUpperCase()}}`;
      streamTitle.innerText = ch.current.title;
      streamDesc.innerText = ch.current.desc;
      posterBg.src = ch.current.poster;

      video.src = ch.current.url;
      video.play().catch(() => {{}});

      renderGuide();
    }}

    pillTabs.querySelectorAll(".tab-btn").forEach(btn => {{
      btn.addEventListener("click", () => {{
        const idx = parseInt(btn.dataset.index, 10);
        tuneChannel(idx);
      }});
    }});

    function toggleAudio() {{
      video.muted = !video.muted;
      audioIcon.innerText = video.muted ? "🔇" : "🔊";
      audioLabel.innerText = video.muted ? "Unmute Audio" : "Mute Audio";
    }}
    btnAudio.addEventListener("click", toggleAudio);

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }}
    btnFullscreen.addEventListener("click", toggleFullscreen);

    window.addEventListener("keydown", (e) => {{
      if (e.key === "ArrowUp") {{
        e.preventDefault();
        tuneChannel((activeChannelIdx - 1 + CHANNELS.length) % CHANNELS.length);
      }} else if (e.key === "ArrowDown") {{
        e.preventDefault();
        tuneChannel((activeChannelIdx + 1) % CHANNELS.length);
      }} else if (e.key === " " || e.key === "m" || e.key === "M") {{
        e.preventDefault();
        toggleAudio();
      }} else if (e.key === "f" || e.key === "F" || e.key === "Enter") {{
        toggleFullscreen();
      }} else if (e.key === "x" || e.key === "X") {{
        const status = document.getElementById("saveStatus");
        status.innerText = `★ Saved '${{CHANNELS[activeChannelIdx].current.title}}' to Library!`;
        status.style.color = "var(--accent)";
      }}
    }});

    window.addEventListener("click", () => {{
      if (video.muted) {{
        video.muted = false;
        audioIcon.innerText = "🔊";
        audioLabel.innerText = "Mute Audio";
      }}
    }}, {{ once: true }});

    tuneChannel(0);
  </script>
</body>
</html>
"""

# Write to preview locations
(ROOT / "dist/store_assets/tv_app_preview.html").write_text(html, encoding="utf-8")
(ROOT / "AhoyXbox/Web/index.html").write_text(html, encoding="utf-8")

# Write to the user's open tab path
user_tab_path = Path("/Users/agworkywork/.gemini/antigravity/brain/a90c34eb-a13f-49bc-822c-f79f8d44883c/ahoy_tv_frontend.html")
if user_tab_path.parent.exists():
    user_tab_path.write_text(html, encoding="utf-8")

print("Files written successfully!")
