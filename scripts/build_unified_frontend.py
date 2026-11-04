# Complete Unified Frontend Builder for Ahoy TV (No Emojis, Pure Broadcast Polish)
import json
import base64
import subprocess
from pathlib import Path

root = Path('/Users/agworkywork/ahoy-on-xbox')

# Load catalog data
with open(root / 'AhoyXbox/Data/catalog.json', 'r', encoding='utf-8') as f:
    catalog_data = json.load(f)

# Load official white logo as base64 data URI
with open(root / 'AhoyXbox/Assets/ahoy_official_white.png', 'rb') as f:
    logo_base64 = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

videos = catalog_data.get('videos', [])
music_tracks = catalog_data.get('music', [])
podcast_shows = catalog_data.get('podcasts', [])

def resolve_thumb(thumb):
    if not thumb:
        return 'https://storage.googleapis.com/ahoy-videos/wintergreen-sessions/web/thumbnails/H6iranjvsNI.jpg'
    if thumb.startswith('/'):
        return 'https://app.ahoy.ooo' + thumb
    return thumb

pure_videos = []
for v in videos:
    v_clean = dict(v)
    v_clean['thumbnail'] = resolve_thumb(v.get('thumbnail'))
    pure_videos.append(v_clean)

wintergreen_vids = [v for v in pure_videos if 'wintergreen' in v.get('id', '') or 'whatnot' in v.get('title', '').lower()]
music_vids = [v for v in pure_videos if 'music-video' in v.get('tags', [])]
skate_vids = [v for v in pure_videos if v.get('category') == 'skating' or 'skating' in v.get('tags', []) or 'tallboyz' in v.get('tags', [])]
other_vids = [v for v in pure_videos if v not in wintergreen_vids and v not in skate_vids and v not in music_vids]

CHANNELS = [
    {
        'number': '101',
        'name': 'LIVE SHOWS',
        'tagline': 'Wintergreen Sessions & Live Concerts',
        'thumb': 'https://storage.googleapis.com/ahoy-videos/wintergreen-sessions/web/thumbnails/H6iranjvsNI.jpg',
        'videos': wintergreen_vids
    },
    {
        'number': '102',
        'name': 'MUSIC VIDEOS',
        'tagline': 'Independent Music Videos & Visuals',
        'thumb': 'https://storage.googleapis.com/ahoy-videos/wintergreen-sessions/web/thumbnails/xPZpU3rY4qU.jpg',
        'videos': music_vids
    },
    {
        'number': '103',
        'name': 'FILMS & SKATE',
        'tagline': 'Skate Tapes & Documentaries',
        'thumb': 'https://storage.googleapis.com/ahoy-videos/skating/flux/Ahoy-FLUX_CashContest.jpg',
        'videos': skate_vids + other_vids
    },
    {
        'number': '104',
        'name': 'THE MIX 24/7',
        'tagline': '24/7 Round-Robin Eclectic Stream',
        'thumb': 'https://storage.googleapis.com/ahoy-videos/wintergreen-sessions/web/thumbnails/1hJR3r16J8Q.jpg',
        'videos': wintergreen_vids + skate_vids + music_vids + other_vids
    }
]

channels_json = json.dumps(CHANNELS)
ondemand_json = json.dumps(pure_videos)
music_json = json.dumps(music_tracks)
podcasts_json = json.dumps(podcast_shows)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0, user-scalable=no" />
  <title>AHOY TV — Unified Broadcast Edition</title>
  <style>
    :root {{
      --ahoy-accent: #FF0060;
      --ahoy-accent-glow: rgba(255, 0, 96, 0.4);
      --ahoy-accent-subtle: rgba(255, 0, 96, 0.15);
      --ahoy-bg: #05070B;
      --ahoy-card: rgba(18, 22, 32, 0.85);
      --ahoy-card-active: rgba(28, 34, 48, 0.95);
      --ahoy-border: rgba(255, 255, 255, 0.1);
      --ahoy-border-active: rgba(255, 0, 96, 0.6);
      --ease-apple: cubic-bezier(0.16, 1, 0.3, 1);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
      -webkit-user-select: none;
    }}

    html, body {{
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      background: var(--ahoy-bg);
      color: #FFFFFF;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    .app-container {{
      width: 1920px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      position: relative;
      background: #000000;
      overflow: hidden;
    }}

    /* TOP BROADCAST BAR */
    .top-bar {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 72px;
      padding: 0 44px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 20;
      background: linear-gradient(180deg, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0) 100%);
      pointer-events: auto;
    }}

    .brand-section {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .logo-img {{
      height: 26px;
      width: auto;
      object-fit: contain;
    }}
    .brand-tv-mark {{
      font-size: 15px;
      font-weight: 900;
      color: var(--ahoy-accent);
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-left: -4px;
      margin-top: 6px;
    }}

    /* 4 CLEAN SECTIONS */
    .section-nav {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(18, 22, 32, 0.7);
      border: 1px solid var(--ahoy-border);
      border-radius: 999px;
      padding: 4px 6px;
      backdrop-filter: blur(20px);
    }}
    .nav-btn {{
      background: transparent;
      border: none;
      color: #8E8E93;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 1.2px;
      padding: 8px 18px;
      border-radius: 999px;
      cursor: pointer;
      transition: all 0.2s var(--ease-apple);
    }}
    .nav-btn.active {{
      background: var(--ahoy-accent);
      color: #FFFFFF;
      box-shadow: 0 0 16px var(--ahoy-accent-glow);
    }}
    .nav-btn:hover:not(.active) {{
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.08);
    }}

    .top-status {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .live-badge {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 0, 96, 0.15);
      border: 1px solid rgba(255, 0, 96, 0.35);
      border-radius: 999px;
      padding: 5px 12px;
    }}
    .live-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--ahoy-accent);
      animation: pulseLive 2s infinite ease-in-out;
    }}
    @keyframes pulseLive {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}
    .live-text {{
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      color: #FFFFFF;
    }}
    .btn-save {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--ahoy-border);
      border-radius: 999px;
      padding: 5px 14px;
      font-size: 11px;
      font-weight: 700;
      color: #8E8E93;
      cursor: pointer;
    }}
    .btn-save.saved {{
      background: rgba(255, 0, 96, 0.2);
      border-color: var(--ahoy-accent);
      color: #FFFFFF;
    }}

    /* MAIN VIDEO HERO STAGE */
    .hero-stage {{
      position: absolute;
      inset: 0;
      z-index: 1;
      overflow: hidden;
    }}
    .hero-backdrop {{
      position: absolute;
      inset: 0;
      background-size: cover;
      background-position: center;
      filter: brightness(0.65) contrast(1.05);
      transition: opacity 0.5s ease;
    }}
    .hero-vignette {{
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 60% 40%, rgba(0,0,0,0.1) 0%, rgba(5,7,11,0.85) 75%, #05070B 100%),
                  linear-gradient(180deg, rgba(5,7,11,0.5) 0%, transparent 30%, transparent 60%, #05070B 100%);
    }}
    video, audio {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}

    /* HERO INFO OVERLAY */
    .hero-info {{
      position: absolute;
      bottom: 270px;
      left: 48px;
      max-width: 820px;
      z-index: 10;
      transition: transform 0.4s var(--ease-apple), opacity 0.4s var(--ease-apple);
    }}
    .hero-tag-row {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }}
    .hero-tag {{
      background: var(--ahoy-accent);
      color: #FFFFFF;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 4px;
    }}
    .hero-specs {{
      font-size: 11px;
      font-weight: 700;
      color: #8E8E93;
      letter-spacing: 1px;
    }}
    .hero-title {{
      font-size: 44px;
      font-weight: 800;
      letter-spacing: -0.5px;
      line-height: 1.1;
      margin-bottom: 10px;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
    }}
    .hero-host {{
      font-size: 17px;
      font-weight: 600;
      color: var(--ahoy-accent);
      margin-bottom: 10px;
    }}
    .hero-desc {{
      font-size: 14px;
      line-height: 1.5;
      color: #C7C7CC;
      margin-bottom: 20px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      max-width: 720px;
    }}
    .hero-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .action-btn {{
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #FFFFFF;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      padding: 10px 22px;
      border-radius: 8px;
      cursor: pointer;
      backdrop-filter: blur(16px);
      transition: all 0.2s var(--ease-apple);
    }}
    .action-btn.primary {{
      background: var(--ahoy-accent);
      border-color: var(--ahoy-accent);
      box-shadow: 0 0 20px var(--ahoy-accent-glow);
    }}
    .action-btn:hover, .action-btn.focused {{
      transform: translateY(-2px);
      border-color: var(--ahoy-accent);
      box-shadow: 0 6px 20px rgba(255, 0, 96, 0.35);
    }}

    /* AUDIO / VINYL VISUALIZER STAGE */
    .music-stage {{
      position: absolute;
      top: 140px;
      right: 120px;
      display: none;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      z-index: 10;
    }}
    .music-stage.active {{
      display: flex;
    }}
    .vinyl-wrapper {{
      width: 220px;
      height: 220px;
      position: relative;
      border-radius: 50%;
      background: radial-gradient(circle, #2C2C2E 20%, #1C1C1E 50%, #000000 70%);
      box-shadow: 0 20px 40px rgba(0,0,0,0.8), 0 0 30px var(--ahoy-accent-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      border: 3px solid #3A3A3C;
      animation: spinVinyl 12s linear infinite;
    }}
    @keyframes spinVinyl {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    .vinyl-art {{
      width: 100px;
      height: 100px;
      border-radius: 50%;
      object-fit: cover;
      border: 2px solid #000000;
    }}
    .visualizer-row {{
      display: flex;
      align-items: flex-end;
      gap: 5px;
      height: 36px;
    }}
    .viz-bar {{
      width: 4px;
      background: var(--ahoy-accent);
      border-radius: 2px;
      animation: bounceBar 1s infinite ease-in-out;
    }}
    .viz-bar:nth-child(1) {{ height: 18px; animation-delay: 0.1s; }}
    .viz-bar:nth-child(2) {{ height: 32px; animation-delay: 0.3s; }}
    .viz-bar:nth-child(3) {{ height: 12px; animation-delay: 0.2s; }}
    .viz-bar:nth-child(4) {{ height: 26px; animation-delay: 0.4s; }}
    .viz-bar:nth-child(5) {{ height: 20px; animation-delay: 0.15s; }}
    @keyframes bounceBar {{
      0%, 100% {{ transform: scaleY(0.4); }}
      50% {{ transform: scaleY(1.0); }}
    }}

    /* LOWER-THIRD COUCH GUIDE DOCK */
    .guide-dock {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 250px;
      background: linear-gradient(180deg, rgba(14, 18, 28, 0) 0%, rgba(8, 10, 16, 0.94) 20%, rgba(5, 7, 11, 0.98) 100%);
      padding: 14px 44px 18px 44px;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      z-index: 15;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      backdrop-filter: blur(28px);
      transition: transform 0.35s var(--ease-apple), opacity 0.35s var(--ease-apple);
    }}
    .guide-dock.hidden {{
      transform: translateY(220px);
      opacity: 0.05;
    }}

    .shelf-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }}
    .shelf-title {{
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 1.5px;
      color: #8E8E93;
      text-transform: uppercase;
    }}
    .shelf-meta {{
      font-size: 12px;
      font-weight: 700;
      color: var(--ahoy-accent);
      letter-spacing: 1px;
    }}

    /* ITEMS CAROUSEL ROW */
    .items-row {{
      display: flex;
      gap: 16px;
      overflow-x: auto;
      scroll-behavior: smooth;
      padding-bottom: 8px;
    }}
    .items-row::-webkit-scrollbar {{
      display: none;
    }}

    .item-card {{
      flex: 0 0 260px;
      height: 146px;
      background: var(--ahoy-card);
      border: 1px solid var(--ahoy-border);
      border-radius: 10px;
      overflow: hidden;
      cursor: pointer;
      position: relative;
      transition: all 0.22s var(--ease-apple);
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 14px;
    }}
    .item-card.active, .item-card:hover, .item-card.focused {{
      border-color: var(--ahoy-accent);
      transform: translateY(-4px) scale(1.02);
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.6), 0 0 16px var(--ahoy-accent-glow);
    }}
    .item-thumb {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      filter: brightness(0.7);
      transition: filter 0.2s ease;
    }}
    .item-card.active .item-thumb, .item-card:hover .item-thumb {{
      filter: brightness(0.85);
    }}
    .item-gradient {{
      position: absolute;
      inset: 0;
      background: linear-gradient(180deg, rgba(0,0,0,0) 30%, rgba(5,7,11,0.92) 100%);
    }}
    .item-details {{
      position: relative;
      z-index: 2;
    }}
    .item-badge {{
      font-size: 10px;
      font-weight: 800;
      color: var(--ahoy-accent);
      letter-spacing: 1px;
      margin-bottom: 4px;
      text-transform: uppercase;
    }}
    .item-title {{
      font-size: 13px;
      font-weight: 700;
      color: #FFFFFF;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 2px;
    }}
    .item-sub {{
      font-size: 11px;
      font-weight: 500;
      color: #8E8E93;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    /* BOTTOM CONTROLLER HINTS */
    .controller-bar {{
      height: 28px;
      margin-top: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 600;
      color: #636366;
      letter-spacing: 0.5px;
    }}
    .hints-group {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .key-tag {{
      display: inline-block;
      background: rgba(255, 255, 255, 0.12);
      color: #FFFFFF;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 4px;
      margin-right: 4px;
      font-size: 10px;
    }}
    .controller-brand {{
      color: #48484A;
      font-weight: 700;
    }}

    /* SCHEDULE DRAWER */
    .schedule-drawer {{
      position: absolute;
      inset: 80px 44px 50px 44px;
      background: rgba(10, 13, 20, 0.96);
      backdrop-filter: blur(36px);
      border: 1px solid var(--ahoy-border);
      border-radius: 14px;
      z-index: 30;
      display: none;
      flex-direction: column;
      padding: 24px 30px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.9);
    }}
    .schedule-drawer.open {{
      display: flex;
    }}
    .drawer-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
      padding-bottom: 14px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    .drawer-title {{
      font-size: 18px;
      font-weight: 800;
      letter-spacing: 1px;
    }}
    .drawer-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      overflow-y: auto;
    }}
    .drawer-item {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      padding: 12px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
    }}
    .drawer-item.active, .drawer-item:hover {{
      border-color: var(--ahoy-accent);
      background: rgba(255, 0, 96, 0.15);
    }}
  </style>
</head>
<body>
  <div class="app-container">
    <!-- TOP BROADCAST BAR -->
    <div class="top-bar">
      <div class="brand-section">
        <img class="logo-img" src="{logo_base64}" alt="Ahoy" />
        <span class="brand-tv-mark">tv</span>
      </div>

      <!-- 4 CLEAN SECTIONS -->
      <div class="section-nav">
        <button class="nav-btn active" id="nav-channels" onclick="setSection('channels')">LIVE TV</button>
        <button class="nav-btn" id="nav-ondemand" onclick="setSection('ondemand')">ON DEMAND</button>
        <button class="nav-btn" id="nav-music" onclick="setSection('music')">MUSIC</button>
        <button class="nav-btn" id="nav-podcasts" onclick="setSection('podcasts')">PODCASTS</button>
      </div>

      <div class="top-status">
        <div class="live-badge">
          <div class="live-dot"></div>
          <span class="live-text" id="status-live">LIVE</span>
        </div>
        <button class="btn-save" id="btn-save" onclick="toggleSave()">[X] SAVE</button>
      </div>
    </div>

    <!-- MAIN VIDEO STAGE -->
    <div class="hero-stage">
      <div class="hero-backdrop" id="hero-backdrop"></div>
      <div class="hero-vignette"></div>

      <video id="video-player" playsinline autoplay loop muted></video>
      <audio id="audio-player"></audio>

      <!-- AUDIO VISUALIZER (WHEN IN MUSIC MODE) -->
      <div class="music-stage" id="music-stage">
        <div class="vinyl-wrapper">
          <img class="vinyl-art" id="vinyl-art" src="" alt="Album Art" />
        </div>
        <div class="visualizer-row">
          <div class="viz-bar"></div>
          <div class="viz-bar"></div>
          <div class="viz-bar"></div>
          <div class="viz-bar"></div>
          <div class="viz-bar"></div>
        </div>
      </div>

      <!-- HERO INFO -->
      <div class="hero-info" id="hero-info">
        <div class="hero-tag-row">
          <span class="hero-tag" id="hero-tag">CH 101 • LIVE SHOWS</span>
          <span class="hero-specs" id="hero-specs">4K UHD • STEREO BROADCAST</span>
        </div>
        <h1 class="hero-title" id="hero-title">Wintergreen Sessions</h1>
        <div class="hero-host" id="hero-host">Continuous Indie Broadcast</div>
        <p class="hero-desc" id="hero-desc">Synchronized independent broadcast streamed continuously from the Ahoy library.</p>

        <div class="hero-actions">
          <button class="action-btn primary" id="btn-play" onclick="togglePlayback()">PLAY</button>
          <button class="action-btn" id="btn-fullscreen" onclick="toggleFullscreen()">FULLSCREEN [A]</button>
          <button class="action-btn" id="btn-schedule" onclick="toggleSchedule()">SCHEDULE [Y]</button>
        </div>
      </div>
    </div>

    <!-- LOWER-THIRD COUCH GUIDE DOCK -->
    <div class="guide-dock" id="guide-dock">
      <div class="shelf-header">
        <span class="shelf-title" id="shelf-title">CHANNELS</span>
        <span class="shelf-meta" id="shelf-meta">CH 101 OF 104</span>
      </div>

      <div class="items-row" id="items-row"></div>

      <div class="controller-bar">
        <div class="hints-group">
          <div><span class="key-tag">LT/RT</span> SECTIONS</div>
          <div><span class="key-tag">LB/RB</span> CHANNELS</div>
          <div><span class="key-tag">A</span> SELECT</div>
          <div><span class="key-tag">B</span> GUIDE</div>
          <div><span class="key-tag">X</span> SAVE</div>
          <div><span class="key-tag">Y</span> SCHEDULE</div>
        </div>
        <div class="controller-brand">AHOY INDIE MEDIA • v0.3.0</div>
      </div>
    </div>

    <!-- SCHEDULE DRAWER -->
    <div class="schedule-drawer" id="schedule-drawer">
      <div class="drawer-header">
        <span class="drawer-title" id="drawer-title">Channel Schedule</span>
        <button class="action-btn" onclick="toggleSchedule()">CLOSE [B]</button>
      </div>
      <div class="drawer-list" id="drawer-list"></div>
    </div>
  </div>

  <script>
    const CHANNELS = {channels_json};
    const ONDEMAND = {ondemand_json};
    const MUSIC = {music_json};
    const PODCASTS = {podcasts_json};

    let currentSection = 'channels';
    let selectedChannel = 0;
    let selectedIndex = 0;
    let playingItem = null;
    let isPlaying = false;
    let isMuted = true;
    let isDockVisible = true;
    let dockTimer = null;
    let scheduleOpen = false;

    const savedIds = new Set(JSON.parse(localStorage.getItem('Ahoy_Saved_Ids') || '[]'));

    const videoEl = document.getElementById('video-player');
    const audioEl = document.getElementById('audio-player');
    const heroBackdrop = document.getElementById('hero-backdrop');
    const musicStage = document.getElementById('music-stage');
    const vinylArt = document.getElementById('vinyl-art');
    const guideDock = document.getElementById('guide-dock');
    const scheduleDrawer = document.getElementById('schedule-drawer');

    const heroTag = document.getElementById('hero-tag');
    const heroSpecs = document.getElementById('hero-specs');
    const heroTitle = document.getElementById('hero-title');
    const heroHost = document.getElementById('hero-host');
    const heroDesc = document.getElementById('hero-desc');
    const btnPlay = document.getElementById('btn-play');
    const btnSave = document.getElementById('btn-save');
    const shelfTitle = document.getElementById('shelf-title');
    const shelfMeta = document.getElementById('shelf-meta');
    const itemsRow = document.getElementById('items-row');
    const drawerList = document.getElementById('drawer-list');

    function wakeDock() {{
      isDockVisible = true;
      guideDock.classList.remove('hidden');
      clearTimeout(dockTimer);
      dockTimer = setTimeout(() => {{
        if (isPlaying && currentSection === 'channels' && !scheduleOpen) {{
          isDockVisible = false;
          guideDock.classList.add('hidden');
        }}
      }}, 6000);
    }}

    function setSection(sec) {{
      currentSection = sec;
      selectedIndex = 0;
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('nav-' + sec).classList.add('active');
      renderShelf();
      wakeDock();
    }}

    function renderShelf() {{
      itemsRow.innerHTML = '';
      if (currentSection === 'channels') {{
        shelfTitle.innerText = 'CHANNELS • 4 CANONICAL PILLARS';
        shelfMeta.innerText = 'CH ' + CHANNELS[selectedChannel].number + ' OF 104';

        CHANNELS.forEach((ch, idx) => {{
          const card = document.createElement('div');
          card.className = 'item-card' + (idx === selectedChannel ? ' active' : '');
          card.innerHTML = `
            <img class="item-thumb" src="${{ch.thumb}}" />
            <div class="item-gradient"></div>
            <div class="item-details">
              <div class="item-badge">CH ${{ch.number}}</div>
              <div class="item-title">${{ch.name}}</div>
              <div class="item-sub">${{ch.tagline}}</div>
            </div>
          `;
          card.onclick = () => tuneChannel(idx);
          itemsRow.appendChild(card);
        }});
      }} else if (currentSection === 'ondemand') {{
        shelfTitle.innerText = 'ON DEMAND • ' + ONDEMAND.length + ' TITLES';
        shelfMeta.innerText = 'INSTANT PLAYBACK';

        ONDEMAND.forEach((v, idx) => {{
          const card = document.createElement('div');
          card.className = 'item-card' + (idx === selectedIndex ? ' active' : '');
          card.innerHTML = `
            <img class="item-thumb" src="${{v.thumbnail}}" />
            <div class="item-gradient"></div>
            <div class="item-details">
              <div class="item-badge">${{v.category || 'VIDEO'}}</div>
              <div class="item-title">${{v.title}}</div>
              <div class="item-sub">${{v.duration || 'Full Feature'}}</div>
            </div>
          `;
          card.onclick = () => playOnDemand(idx);
          itemsRow.appendChild(card);
        }});
      }} else if (currentSection === 'music') {{
        shelfTitle.innerText = 'AHOY MUSIC • ' + MUSIC.length + ' TRACKS';
        shelfMeta.innerText = 'AUDIO BROADCAST';

        MUSIC.forEach((m, idx) => {{
          const card = document.createElement('div');
          card.className = 'item-card' + (idx === selectedIndex ? ' active' : '');
          const thumb = m.thumbnail || 'https://i.ytimg.com/vi/XDH0X-dF4GM/maxresdefault.jpg';
          card.innerHTML = `
            <img class="item-thumb" src="${{thumb}}" />
            <div class="item-gradient"></div>
            <div class="item-details">
              <div class="item-badge">${{m.artist}}</div>
              <div class="item-title">${{m.title}}</div>
              <div class="item-sub">${{m.album || 'Single'}}</div>
            </div>
          `;
          card.onclick = () => playMusicTrack(idx);
          itemsRow.appendChild(card);
        }});
      }} else if (currentSection === 'podcasts') {{
        shelfTitle.innerText = 'PODCASTS • ' + PODCASTS.length + ' SERIES';
        shelfMeta.innerText = 'TALK & CULTURE';

        PODCASTS.forEach((p, idx) => {{
          const card = document.createElement('div');
          card.className = 'item-card' + (idx === selectedIndex ? ' active' : '');
          card.innerHTML = `
            <img class="item-thumb" src="${{p.thumbnail}}" />
            <div class="item-gradient"></div>
            <div class="item-details">
              <div class="item-badge">PODCAST SERIES</div>
              <div class="item-title">${{p.title}}</div>
              <div class="item-sub">${{p.episodes.length}} Episodes</div>
            </div>
          `;
          card.onclick = () => openPodcastShow(idx);
          itemsRow.appendChild(card);
        }});
      }}
    }}

    function tuneChannel(idx) {{
      selectedChannel = idx;
      renderShelf();
      const ch = CHANNELS[idx];
      if (!ch.videos || ch.videos.length === 0) return;

      // Pluto TV Live UTC Sync
      const nowSec = Math.floor(Date.now() / 1000);
      const totalCycle = ch.videos.length * 900;
      const cycleSec = nowSec % totalCycle;
      const vidIdx = Math.floor(cycleSec / 900) % ch.videos.length;
      const seekSec = cycleSec % 900;

      const vid = ch.videos[vidIdx];
      playVideoItem(vid, seekSec, `CH ${{ch.number}} • ${{ch.name}}`, 'LIVE BROADCAST');
    }}

    function playOnDemand(idx) {{
      selectedIndex = idx;
      renderShelf();
      const v = ONDEMAND[idx];
      playVideoItem(v, 0, v.category || 'ON DEMAND', 'ON DEMAND');
    }}

    function playVideoItem(item, startSec, tag, status) {{
      playingItem = item;
      musicStage.classList.remove('active');
      audioEl.pause();

      videoEl.style.display = 'block';
      heroBackdrop.style.backgroundImage = `url("${{item.thumbnail}}")`;

      heroTag.innerText = tag;
      heroSpecs.innerText = item.duration ? `${{item.duration}} • STEREO` : 'HD • STEREO';
      heroTitle.innerText = item.title;
      heroHost.innerText = item.host || 'Ahoy';
      heroDesc.innerText = item.description || 'Continuous independent video stream from the Ahoy library.';

      videoEl.src = item.url;
      videoEl.currentTime = startSec || 0;
      videoEl.muted = isMuted;
      videoEl.play().then(() => {{
        isPlaying = true;
        btnPlay.innerText = 'PAUSE';
      }}).catch(() => {{
        isPlaying = false;
        btnPlay.innerText = 'PLAY';
      }});

      updateSaveStatus();
      wakeDock();
    }}

    function playMusicTrack(idx) {{
      selectedIndex = idx;
      renderShelf();
      const m = MUSIC[idx];
      playingItem = m;

      videoEl.pause();
      videoEl.style.display = 'none';
      musicStage.classList.add('active');

      const thumb = m.thumbnail || 'https://i.ytimg.com/vi/XDH0X-dF4GM/maxresdefault.jpg';
      vinylArt.src = thumb;
      heroBackdrop.style.backgroundImage = `url("${{thumb}}")`;

      heroTag.innerText = 'AHOY MUSIC';
      heroSpecs.innerText = 'STEREO HIGH-FIDELITY';
      heroTitle.innerText = m.title;
      heroHost.innerText = m.artist;
      heroDesc.innerText = `Album: ${{m.album || 'Single'}} • Indie airplay from New Haven, CT.`;

      audioEl.src = m.stream_url;
      audioEl.muted = isMuted;
      audioEl.play().then(() => {{
        isPlaying = true;
        btnPlay.innerText = 'PAUSE';
      }}).catch(() => {{
        isPlaying = false;
        btnPlay.innerText = 'PLAY';
      }});

      updateSaveStatus();
      wakeDock();
    }}

    function openPodcastShow(idx) {{
      const p = PODCASTS[idx];
      shelfTitle.innerText = p.title + ' • EPISODES';
      shelfMeta.innerText = p.episodes.length + ' EPISODES';
      itemsRow.innerHTML = '';

      p.episodes.forEach((ep, epIdx) => {{
        const card = document.createElement('div');
        card.className = 'item-card';
        card.innerHTML = `
          <img class="item-thumb" src="${{ep.thumbnail || p.thumbnail}}" />
          <div class="item-gradient"></div>
          <div class="item-details">
            <div class="item-badge">EPISODE</div>
            <div class="item-title">${{ep.title}}</div>
            <div class="item-sub">${{ep.date || 'Ahoy Podcast'}}</div>
          </div>
        `;
        card.onclick = () => {{
          playingItem = ep;
          videoEl.pause();
          videoEl.style.display = 'none';
          musicStage.classList.add('active');
          vinylArt.src = ep.thumbnail || p.thumbnail;
          heroBackdrop.style.backgroundImage = `url("${{ep.thumbnail || p.thumbnail}}")`;

          heroTag.innerText = p.title;
          heroSpecs.innerText = ep.duration || 'PODCAST AUDIO';
          heroTitle.innerText = ep.title;
          heroHost.innerText = p.title;
          heroDesc.innerText = ep.description || p.description;

          audioEl.src = ep.audio_url;
          audioEl.muted = isMuted;
          audioEl.play().then(() => {{
            isPlaying = true;
            btnPlay.innerText = 'PAUSE';
          }}).catch(() => {{
            isPlaying = false;
            btnPlay.innerText = 'PLAY';
          }});

          updateSaveStatus();
          wakeDock();
        }};
        itemsRow.appendChild(card);
      }});
    }}

    function togglePlayback() {{
      const player = (videoEl.style.display === 'none') ? audioEl : videoEl;
      if (player.paused) {{
        player.play().catch(() => {{}});
        isPlaying = true;
        btnPlay.innerText = 'PAUSE';
      }} else {{
        player.pause();
        isPlaying = false;
        btnPlay.innerText = 'PLAY';
      }}
    }}

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }}

    function toggleSchedule() {{
      scheduleOpen = !scheduleOpen;
      if (scheduleOpen) {{
        scheduleDrawer.classList.add('open');
        const ch = CHANNELS[selectedChannel];
        document.getElementById('drawer-title').innerText = `CH ${{ch.number}} • ${{ch.name}} SCHEDULE`;
        drawerList.innerHTML = '';
        ch.videos.forEach((v, i) => {{
          const item = document.createElement('div');
          item.className = 'drawer-item';
          item.innerHTML = `
            <div>
              <div style="font-weight:700;font-size:14px;">${{v.title}}</div>
              <div style="font-size:12px;color:#8E8E93;">${{v.host || 'Ahoy'}}</div>
            </div>
            <div style="font-size:11px;font-weight:700;color:var(--ahoy-accent);">${{v.duration || '15:00'}}</div>
          `;
          item.onclick = () => {{
            playVideoItem(v, 0, `CH ${{ch.number}} • ${{ch.name}}`, 'SCHEDULE SELECTION');
            toggleSchedule();
          }};
          drawerList.appendChild(item);
        }});
      }} else {{
        scheduleDrawer.classList.remove('open');
      }}
    }}

    function toggleSave() {{
      if (!playingItem) return;
      const id = playingItem.id || playingItem.title;
      if (savedIds.has(id)) {{
        savedIds.delete(id);
      }} else {{
        savedIds.add(id);
      }}
      localStorage.setItem('Ahoy_Saved_Ids', JSON.stringify(Array.from(savedIds)));
      updateSaveStatus();
    }}

    function updateSaveStatus() {{
      if (!playingItem) return;
      const id = playingItem.id || playingItem.title;
      if (savedIds.has(id)) {{
        btnSave.innerText = '[X] SAVED';
        btnSave.classList.add('saved');
      }} else {{
        btnSave.innerText = '[X] SAVE';
        btnSave.classList.remove('saved');
      }}
    }}

    // KEYBOARD & GAMEPAD CONTROLS
    window.addEventListener('keydown', (e) => {{
      wakeDock();
      switch (e.key) {{
        case '1': setSection('channels'); break;
        case '2': setSection('ondemand'); break;
        case '3': setSection('music'); break;
        case '4': setSection('podcasts'); break;
        case 'Tab':
          e.preventDefault();
          const sections = ['channels', 'ondemand', 'music', 'podcasts'];
          const nextSec = sections[(sections.indexOf(currentSection) + 1) % sections.length];
          setSection(nextSec);
          break;
        case 'ArrowLeft':
          if (currentSection === 'channels') {{
            selectedChannel = (selectedChannel - 1 + CHANNELS.length) % CHANNELS.length;
            tuneChannel(selectedChannel);
          }}
          break;
        case 'ArrowRight':
          if (currentSection === 'channels') {{
            selectedChannel = (selectedChannel + 1) % CHANNELS.length;
            tuneChannel(selectedChannel);
          }}
          break;
        case 'Enter':
        case ' ':
        case 'a':
        case 'A':
          togglePlayback();
          break;
        case 'b':
        case 'B':
          if (scheduleOpen) toggleSchedule();
          else {{
            isDockVisible = !isDockVisible;
            guideDock.classList.toggle('hidden', !isDockVisible);
          }}
          break;
        case 'x':
        case 'X':
          toggleSave();
          break;
        case 'y':
        case 'Y':
          toggleSchedule();
          break;
        case 'PageUp':
        case '[':
          selectedChannel = (selectedChannel - 1 + CHANNELS.length) % CHANNELS.length;
          tuneChannel(selectedChannel);
          break;
        case 'PageDown':
        case ']':
          selectedChannel = (selectedChannel + 1) % CHANNELS.length;
          tuneChannel(selectedChannel);
          break;
      }}
    }});

    // GAMEPAD POLLER
    let lastPadButtons = {{}};
    function pollGamepad() {{
      const gamepads = navigator.getGamepads ? navigator.getGamepads() : [];
      const gp = gamepads[0];
      if (gp) {{
        const checkBtn = (btnIndex, keyName) => {{
          const isPressed = gp.buttons[btnIndex] && gp.buttons[btnIndex].pressed;
          if (isPressed && !lastPadButtons[btnIndex]) {{
            window.dispatchEvent(new KeyboardEvent('keydown', {{ key: keyName }}));
          }}
          lastPadButtons[btnIndex] = isPressed;
        }};

        checkBtn(12, 'ArrowUp');
        checkBtn(13, 'ArrowDown');
        checkBtn(14, 'ArrowLeft');
        checkBtn(15, 'ArrowRight');
        checkBtn(4, 'PageUp');    // LB
        checkBtn(5, 'PageDown');  // RB
        checkBtn(6, 'Tab');       // LT (Cycle Section)
        checkBtn(7, 'Tab');       // RT (Cycle Section)
        checkBtn(0, 'A');         // [A]
        checkBtn(1, 'B');         // [B]
        checkBtn(2, 'X');         // [X]
        checkBtn(3, 'Y');         // [Y]
      }}
      requestAnimationFrame(pollGamepad);
    }}
    window.addEventListener('gamepadconnected', () => requestAnimationFrame(pollGamepad));
    requestAnimationFrame(pollGamepad);

    // Initial load: Channel 101
    tuneChannel(0);
  </script>
</body>
</html>
"""

# Write to target paths
for path in [root / 'AhoyXbox/Web/index.html', root / 'dist/store_assets/tv_app_preview.html', Path('/Users/agworkywork/.gemini/antigravity/brain/16a4042b-c7c9-4978-be35-735909a8ed76/ahoy_tv_frontend.html')]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f'Wrote: {path}')

# Render 1080p preview screenshot
try:
    chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    preview_png = root / 'dist/store_assets/v0.3.0_preview.png'
    target_html = root / 'dist/store_assets/tv_app_preview.html'
    subprocess.run([chrome, '--headless', '--disable-gpu', '--window-size=1920,1080', f'--screenshot={preview_png}', f'file://{target_html}'], check=True)
    
    brain_preview = Path('/Users/agworkywork/.gemini/antigravity/brain/16a4042b-c7c9-4978-be35-735909a8ed76/v0.3.0_preview.png')
    brain_preview.write_bytes(preview_png.read_bytes())
    print('Rendered and copied 1080p preview screenshot successfully')
except Exception as e:
    print('Screenshot note:', e)
