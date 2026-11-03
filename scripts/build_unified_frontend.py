import json
import base64
from pathlib import Path

root = Path('/Users/agworkywork/ahoy-on-xbox')

# Load catalog & music
with open(root / 'AhoyXbox/Data/catalog.json', 'r', encoding='utf-8') as f:
    catalog_data = json.load(f)

with open(root / 'AhoyXbox/Data/music.json', 'r', encoding='utf-8') as f:
    music_data = json.load(f)

# Load official white logo as base64 data URI
with open(root / 'AhoyXbox/Assets/ahoy_official_white.png', 'rb') as f:
    logo_base64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

videos = catalog_data.get('videos', [])
tracks = music_data.get('tracks', [])

def is_disc_golf(v):
    id_str = v.get('id', '').lower()
    title_str = v.get('title', '').lower()
    tags = [t.lower() for t in v.get('tags', [])]
    return 'disc-golf' in id_str or 'disc-golf' in tags or 'disc' in title_str or 'putter' in title_str

def resolve_thumb(thumb):
    if not thumb:
        return 'https://storage.googleapis.com/ahoy-videos/wintergreen-sessions/web/thumbnails/H6iranjvsNI.jpg'
    if thumb.startswith('/'):
        return 'https://app.ahoy.ooo' + thumb
    return thumb

pure_videos = []
for v in videos:
    if not is_disc_golf(v):
        v_clean = dict(v)
        v_clean['thumbnail'] = resolve_thumb(v.get('thumbnail'))
        pure_videos.append(v_clean)

wintergreen_vids = [v for v in pure_videos if 'wintergreen' in v.get('id', '') or 'whatnot' in v.get('title', '').lower()]
music_vids = [v for v in pure_videos if 'music-video' in v.get('tags', [])]
skate_vids = [v for v in pure_videos if v.get('category') == 'skating' or 'skating' in v.get('tags', []) or 'tallboyz' in v.get('tags', [])]
other_vids = [v for v in pure_videos if v not in wintergreen_vids and v not in skate_vids and v not in music_vids]

ahoy_mix_vids = wintergreen_vids + skate_vids + music_vids + other_vids
music_and_culture_vids = music_vids + skate_vids

radio_tracks = []
for t in tracks[:20]:
    cover = t.get('cover_art') or 'https://i.ytimg.com/vi/XDH0X-dF4GM/maxresdefault.jpg'
    radio_tracks.append({
        'id': t.get('track_id'),
        'title': t.get('title', 'Untitled Track'),
        'host': t.get('artist', 'Ahoy Radio'),
        'album': t.get('album', 'Indie Radio 24/7'),
        'url': t.get('audio_url'),
        'thumbnail': cover,
        'category': 'radio',
        'description': f"Continuous 24/7 indie airplay by {t.get('artist', 'Ahoy Radio')} from {t.get('album', 'Single')}."
    })

# EXACTLY 4 CHANNELS (MATCHING APP.AHOY.OOO)
CHANNELS = [
    {
        'number': '101',
        'name': 'AHOY MIX',
        'tagline': '24/7 Continuous Indie Broadcast',
        'thumb': 'https://storage.googleapis.com/ahoy-videos/wintergreen-sessions/web/thumbnails/H6iranjvsNI.jpg',
        'videos': ahoy_mix_vids
    },
    {
        'number': '102',
        'name': 'WINTERGREEN STUDIOS',
        'tagline': 'Live Concerts & Studio Sessions',
        'thumb': 'https://storage.googleapis.com/ahoy-videos/wintergreen-sessions/web/thumbnails/1hJR3r16J8Q.jpg',
        'videos': wintergreen_vids
    },
    {
        'number': '103',
        'name': 'AHOY RADIO 24/7',
        'tagline': 'Continuous Indie Airplay',
        'thumb': 'https://i.ytimg.com/vi/XDH0X-dF4GM/maxresdefault.jpg',
        'videos': radio_tracks
    },
    {
        'number': '104',
        'name': 'MUSIC & CULTURE',
        'tagline': 'Underground Videos & Skate Tapes',
        'thumb': 'https://storage.googleapis.com/ahoy-videos/skating/flux/Ahoy-FLUX_CashContest.jpg',
        'videos': music_and_culture_vids
    }
]

channels_json = json.dumps(CHANNELS)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Ahoy TV — Apple TV Edition (#FF0060)</title>
  <style>
    :root {{
      --ahoy-accent: #FF0060;
      --ahoy-accent-glow: rgba(255, 0, 96, 0.45);
      --ahoy-accent-subtle: rgba(255, 0, 96, 0.16);
      --apple-canvas: #05070B;
      --apple-card: rgba(18, 22, 32, 0.72);
      --apple-card-active: rgba(28, 34, 48, 0.88);
      --glass-border: rgba(255, 255, 255, 0.12);
      --glass-highlight: rgba(255, 255, 255, 0.22);
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
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      position: fixed;
      inset: 0;
      background: var(--apple-canvas);
      color: #FFFFFF;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif;
      padding: 22px 38px 18px 38px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    /* APPLE AMBIENT LIGHTING MESH */
    .ambient-mesh {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 0;
      overflow: hidden;
    }}
    .blob-accent {{
      position: absolute;
      top: -15%;
      left: 20%;
      width: 55vw;
      height: 55vw;
      background: radial-gradient(circle, rgba(255, 0, 96, 0.13) 0%, transparent 65%);
      filter: blur(120px);
    }}
    .blob-deep {{
      position: absolute;
      bottom: -20%;
      right: 15%;
      width: 60vw;
      height: 60vw;
      background: radial-gradient(circle, rgba(140, 20, 80, 0.10) 0%, transparent 65%);
      filter: blur(120px);
    }}

    /* LIQUID GLASS PILLS */
    .liquid-pill {{
      background: rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(32px) saturate(190%);
      -webkit-backdrop-filter: blur(32px) saturate(190%);
      border: 1px solid var(--glass-border);
      box-shadow: inset 0 1px 1px var(--glass-highlight), 0 8px 24px rgba(0, 0, 0, 0.45);
      border-radius: 9999px;
    }}

    /* TOP BAR (Row 0) */
    .top-bar {{
      position: relative;
      z-index: 20;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 48px;
      margin-bottom: 12px;
      flex-shrink: 0;
    }}
    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .brand-pill {{
      padding: 6px 16px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .logo-img {{
      height: 22px;
      width: auto;
      object-fit: contain;
    }}
    .brand-tv-mark {{
      font-size: 16px;
      font-weight: 900;
      color: var(--ahoy-accent);
      letter-spacing: -0.5px;
      margin-left: 2px;
    }}
    .live-pill {{
      padding: 5px 12px;
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 0, 96, 0.14);
      border: 1px solid rgba(255, 0, 96, 0.4);
    }}
    .live-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--ahoy-accent);
      box-shadow: 0 0 10px var(--ahoy-accent);
      animation: pulseDot 2s infinite ease-in-out;
    }}
    @keyframes pulseDot {{
      0%, 100% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(1.35); opacity: 0.6; }}
    }}
    .live-label {{
      font-size: 11px;
      font-weight: 900;
      color: #FFFFFF;
      letter-spacing: 0.8px;
    }}

    .header-banner {{
      padding: 6px 22px;
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 13.5px;
    }}
    .header-channel {{
      font-weight: 800;
      color: var(--ahoy-accent);
      letter-spacing: 0.5px;
    }}
    .header-divider {{
      color: rgba(255, 255, 255, 0.25);
    }}
    .header-nowplaying {{
      color: #FFFFFF;
      font-weight: 600;
      max-width: 480px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .top-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .action-pill {{
      padding: 6px 16px;
      font-size: 11px;
      font-weight: 800;
      color: rgba(255, 255, 255, 0.7);
      letter-spacing: 0.8px;
      cursor: pointer;
      transition: all 0.2s var(--ease-apple);
    }}
    .action-pill.active {{
      color: var(--ahoy-accent);
      border-color: rgba(255, 0, 96, 0.45);
      background: rgba(255, 0, 96, 0.12);
    }}

    /* MAIN STAGE */
    .main-stage {{
      position: relative;
      z-index: 10;
      flex: 1;
      display: flex;
      flex-direction: column;
      min-height: 0;
      gap: 12px;
    }}

    /* TOP BILLBOARD / HERO STAGE (Apple TV Top-Shelf) */
    .billboard-container {{
      flex: 1;
      min-height: 0;
      background: #000000;
      border-radius: 18px;
      border: 1px solid var(--glass-border);
      box-shadow: inset 0 1px 1px var(--glass-highlight), 0 24px 60px rgba(0, 0, 0, 0.8);
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: stretch;
      justify-content: stretch;
    }}

    /* POSTER BACKDROP */
    .billboard-backdrop {{
      position: absolute;
      inset: 0;
      background-size: cover;
      background-position: center center;
      opacity: 0.95;
      transition: background-image 0.4s var(--ease-apple), opacity 0.4s var(--ease-apple);
      z-index: 1;
    }}
    .billboard-vignette {{
      position: absolute;
      inset: 0;
      background: linear-gradient(90deg, rgba(5, 7, 11, 0.94) 0%, rgba(5, 7, 11, 0.55) 45%, rgba(5, 7, 11, 0.25) 100%),
                  linear-gradient(0deg, rgba(5, 7, 11, 0.96) 0%, transparent 40%);
      z-index: 2;
    }}

    /* VIDEO ELEMENT */
    #media-element {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      z-index: 2;
      opacity: 1;
      transition: opacity 0.3s;
    }}
    #audio-element {{
      display: none;
    }}

    /* BILLBOARD HERO CONTENT (Apple TV Layout) */
    .billboard-content {{
      position: relative;
      z-index: 5;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 30px 36px;
      max-width: 840px;
    }}

    .hero-meta-row {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .tag-badge {{
      background: rgba(255, 0, 96, 0.18);
      border: 1px solid rgba(255, 0, 96, 0.45);
      color: var(--ahoy-accent);
      font-size: 11px;
      font-weight: 900;
      padding: 3px 10px;
      border-radius: 6px;
      letter-spacing: 0.8px;
      text-transform: uppercase;
    }}
    .spec-pills {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      color: rgba(255, 255, 255, 0.65);
      background: rgba(0, 0, 0, 0.45);
      padding: 3px 10px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .hero-title {{
      font-size: 34px;
      font-weight: 900;
      color: #FFFFFF;
      letter-spacing: -0.6px;
      line-height: 1.15;
      margin-bottom: 8px;
      text-shadow: 0 4px 16px rgba(0, 0, 0, 0.85);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 800px;
    }}
    .hero-desc {{
      font-size: 14.5px;
      font-weight: 500;
      color: rgba(255, 255, 255, 0.82);
      line-height: 1.45;
      margin-bottom: 20px;
      max-width: 700px;
      text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    /* ACTION BUTTONS (Apple TV Liquid Glass Buttons with #FF0060 accent) */
    .hero-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .glass-btn {{
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(24px) saturate(180%);
      -webkit-backdrop-filter: blur(24px) saturate(180%);
      border: 1px solid var(--glass-border);
      box-shadow: inset 0 1px 1px var(--glass-highlight), 0 6px 18px rgba(0, 0, 0, 0.4);
      border-radius: 12px;
      padding: 10px 22px;
      font-size: 13.5px;
      font-weight: 800;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      transition: all 0.22s var(--ease-apple);
    }}
    .glass-btn.primary {{
      background: var(--ahoy-accent);
      color: #FFFFFF;
      border-color: var(--ahoy-accent);
      box-shadow: 0 0 25px var(--ahoy-accent-glow);
    }}
    .glass-btn.primary:hover, .glass-btn.primary.focused {{
      background: #FFFFFF;
      border-color: #FFFFFF;
      color: #000000;
      transform: scale(1.05);
      box-shadow: 0 0 30px rgba(255, 255, 255, 0.7);
    }}
    .glass-btn:hover, .glass-btn.focused {{
      background: rgba(255, 255, 255, 0.2);
      border-color: var(--ahoy-accent);
      transform: scale(1.05);
      box-shadow: 0 0 22px var(--ahoy-accent-glow);
    }}

    /* UNMUTE PILL */
    .unmute-pill {{
      position: absolute;
      top: 20px;
      right: 24px;
      z-index: 10;
      padding: 8px 18px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      font-weight: 800;
      color: #FFFFFF;
      cursor: pointer;
      background: rgba(255, 0, 96, 0.18);
      border-color: var(--ahoy-accent);
      animation: pulseGlow 2.5s infinite;
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ box-shadow: 0 0 15px rgba(255, 0, 96, 0.3); }}
      50% {{ box-shadow: 0 0 32px rgba(255, 0, 96, 0.75); }}
    }}

    /* RADIO 24/7 3D LIQUID GLASS STAGE */
    .radio-stage {{
      position: absolute;
      inset: 0;
      z-index: 3;
      display: none;
      align-items: center;
      justify-content: flex-end;
      padding-right: 70px;
      pointer-events: none;
    }}
    .vinyl-wrapper {{
      position: relative;
      width: 220px;
      height: 220px;
      perspective: 1000px;
    }}
    .vinyl-disc {{
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: radial-gradient(circle, #252830 0%, #101217 60%, #06080b 100%);
      box-shadow: 0 16px 50px rgba(0, 0, 0, 0.85), inset 0 0 0 2px rgba(255, 255, 255, 0.1);
      display: flex;
      align-items: center;
      justify-content: center;
      animation: spinVinyl 12s linear infinite;
    }}
    @keyframes spinVinyl {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    .vinyl-art {{
      width: 96px;
      height: 96px;
      border-radius: 50%;
      object-fit: cover;
      box-shadow: 0 0 14px rgba(0, 0, 0, 0.7);
      border: 2px solid var(--ahoy-accent);
    }}
    .visualizer-bars {{
      position: absolute;
      bottom: -35px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: flex-end;
      gap: 5px;
      height: 30px;
    }}
    .viz-bar {{
      width: 4px;
      background: var(--ahoy-accent);
      border-radius: 2px;
      animation: bounceBar 0.8s ease-in-out infinite alternate;
    }}
    .viz-bar:nth-child(2) {{ height: 18px; animation-delay: 0.15s; background: #FFFFFF; }}
    .viz-bar:nth-child(3) {{ height: 28px; animation-delay: 0.3s; background: var(--ahoy-accent); }}
    .viz-bar:nth-child(4) {{ height: 14px; animation-delay: 0.45s; background: #FFFFFF; }}
    .viz-bar:nth-child(5) {{ height: 22px; animation-delay: 0.2s; background: var(--ahoy-accent); }}
    @keyframes bounceBar {{
      0% {{ height: 6px; }}
      100% {{ height: 28px; }}
    }}

    /* BOTTOM SHELF: 4 CHANNELS (APP.AHOY.OOO) */
    .bottom-section {{
      height: 180px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .shelf-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 4px;
    }}
    .shelf-title {{
      font-size: 13px;
      font-weight: 800;
      color: rgba(255, 255, 255, 0.6);
      letter-spacing: 1px;
      text-transform: uppercase;
    }}
    .shelf-meta {{
      font-size: 12px;
      font-weight: 800;
      color: var(--ahoy-accent);
    }}

    /* 4 CHANNELS ROW */
    .channels-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      height: 145px;
    }}
    .channel-tile {{
      background: var(--apple-card);
      backdrop-filter: blur(28px) saturate(190%);
      -webkit-backdrop-filter: blur(28px) saturate(190%);
      border: 1px solid var(--glass-border);
      box-shadow: inset 0 1px 1px var(--glass-highlight), 0 12px 28px rgba(0, 0, 0, 0.45);
      border-radius: 16px;
      padding: 15px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.22s var(--ease-apple);
    }}
    .channel-tile-content {{
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      height: 100%;
      justify-content: space-between;
    }}
    .tile-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
    }}
    .tile-number {{
      font-size: 18px;
      font-weight: 900;
      color: var(--ahoy-accent);
      letter-spacing: -0.5px;
    }}
    .tile-badge {{
      font-size: 9px;
      font-weight: 900;
      padding: 3px 8px;
      border-radius: 5px;
      background: rgba(255, 255, 255, 0.1);
      color: rgba(255, 255, 255, 0.8);
      letter-spacing: 0.6px;
    }}
    .channel-tile.active .tile-badge {{
      background: rgba(255, 0, 96, 0.25);
      color: var(--ahoy-accent);
      border: 1px solid rgba(255, 0, 96, 0.5);
    }}
    .tile-info {{
      margin-top: auto;
    }}
    .tile-name {{
      font-size: 15.5px;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .tile-tagline {{
      font-size: 11px;
      color: rgba(255, 255, 255, 0.65);
      margin-top: 3px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .channel-tile.active {{
      background: var(--apple-card-active);
      border-color: rgba(255, 0, 96, 0.45);
    }}
    .channel-tile.focused {{
      border-color: var(--ahoy-accent) !important;
      transform: scale(1.03) translateY(-4px);
      box-shadow: 0 14px 34px rgba(0, 0, 0, 0.6), 0 0 28px var(--ahoy-accent-glow);
    }}

    /* BOTTOM CONTROLLER BAR */
    .bottom-bar {{
      position: relative;
      z-index: 20;
      height: 32px;
      margin-top: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      padding: 0 4px;
      font-size: 12px;
      color: rgba(255, 255, 255, 0.55);
    }}
    .key-hints {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .key-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 18px;
      height: 18px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 4px;
      font-size: 10px;
      font-weight: 800;
      color: #FFFFFF;
      margin-right: 5px;
    }}
    .status-text {{
      font-size: 11px;
      font-weight: 700;
      color: rgba(255, 255, 255, 0.4);
      letter-spacing: 0.5px;
    }}

    /* SCHEDULE DRAWER */
    .schedule-drawer {{
      position: absolute;
      inset: 60px 38px 50px 38px;
      background: rgba(8, 10, 16, 0.95);
      backdrop-filter: blur(36px) saturate(200%);
      -webkit-backdrop-filter: blur(36px) saturate(200%);
      border: 1px solid var(--glass-border);
      border-radius: 18px;
      z-index: 30;
      display: none;
      flex-direction: column;
      padding: 24px 32px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9);
    }}
    .schedule-drawer.open {{
      display: flex;
    }}
    .drawer-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 12px;
    }}
    .drawer-title {{
      font-size: 20px;
      font-weight: 800;
      color: #FFFFFF;
    }}
    .drawer-list {{
      flex: 1;
      overflow-y: auto;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }}
    .sched-item {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 12px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.18s var(--ease-apple);
    }}
    .sched-item.playing {{
      border-color: var(--ahoy-accent);
      background: rgba(255, 0, 96, 0.14);
    }}
    .sched-item:hover, .sched-item.focused {{
      border-color: var(--ahoy-accent);
      background: rgba(255, 0, 96, 0.22);
      transform: scale(1.01);
    }}
  </style>
</head>
<body>
  <div class="ambient-mesh">
    <div class="blob-accent"></div>
    <div class="blob-deep"></div>
  </div>

  <!-- TOP BAR -->
  <div class="top-bar">
    <div class="brand-wrap">
      <div class="liquid-pill brand-pill">
        <img class="logo-img" src="{logo_base64}" alt="Ahoy" />
        <span class="brand-tv-mark">tv</span>
      </div>
      <div class="liquid-pill live-pill">
        <div class="live-dot"></div>
        <span class="live-label">LIVE</span>
      </div>
    </div>

    <div class="liquid-pill header-banner">
      <span class="header-channel" id="header-channel">CH 101 • AHOY MIX</span>
      <span class="header-divider">|</span>
      <span class="header-nowplaying" id="header-nowplaying">Connecting to continuous broadcast...</span>
    </div>

    <div class="top-actions">
      <div class="liquid-pill action-pill" id="schedule-pill" onclick="toggleScheduleDrawer()">[Y] SCHEDULE</div>
      <div class="liquid-pill action-pill" id="save-indicator" onclick="toggleSaveCurrent()">[X] SAVE TO LIBRARY</div>
    </div>
  </div>

  <!-- MAIN STAGE -->
  <div class="main-stage">
    <!-- TOP BILLBOARD / HERO STAGE -->
    <div class="billboard-container" id="billboard">
      <div class="billboard-backdrop" id="billboard-backdrop"></div>
      <div class="billboard-vignette"></div>

      <!-- VIDEO ELEMENT WITH POSTER BACKDROP -->
      <video id="media-element" playsinline autoplay muted loop></video>
      <audio id="audio-element"></audio>

      <!-- UNMUTE PILL -->
      <div class="liquid-pill unmute-pill" id="unmute-banner" onclick="enableAudio()">
        <span>🔊 Tap to Unmute Audio</span>
      </div>

      <!-- SPECIALIZED 3D LIQUID GLASS RADIO STAGE -->
      <div class="radio-stage" id="radio-stage">
        <div class="vinyl-wrapper">
          <div class="vinyl-disc">
            <img class="vinyl-art" id="vinyl-art" src="" alt="Album Art" />
          </div>
          <div class="visualizer-bars">
            <div class="viz-bar"></div>
            <div class="viz-bar"></div>
            <div class="viz-bar"></div>
            <div class="viz-bar"></div>
            <div class="viz-bar"></div>
          </div>
        </div>
      </div>

      <!-- BILLBOARD HERO METADATA & ACTION BUTTONS -->
      <div class="billboard-content">
        <div class="hero-meta-row">
          <span class="tag-badge" id="hero-tag">AHOY LIVE SHOW</span>
          <div class="spec-pills">
            <span>4K UHD</span>
            <span>•</span>
            <span>HDR10</span>
            <span>•</span>
            <span>DOLBY 5.1</span>
            <span>•</span>
            <span id="hero-status-pill">LIVE ON AIR</span>
          </div>
        </div>

        <h1 class="hero-title" id="hero-title">Wintergreen Sessions</h1>
        <p class="hero-desc" id="hero-desc">Live high-fidelity indie concert recordings and 24/7 continuous broadcast from the Ahoy studio.</p>

        <div class="hero-actions">
          <button class="glass-btn primary" id="btn-play" onclick="togglePlay()">
            <span id="play-icon">▶</span> <span id="play-text">Play Live</span>
          </button>
          <button class="glass-btn" id="btn-fullscreen" onclick="toggleFullscreen()">
            <span>⛶ Fullscreen [A]</span>
          </button>
          <button class="glass-btn" id="btn-next" onclick="playNext()">
            <span>⏭ Next Program</span>
          </button>
          <button class="glass-btn" id="btn-save" onclick="toggleSaveCurrent()">
            <span>🔖 Bookmark</span>
          </button>
        </div>
      </div>
    </div>

    <!-- BOTTOM SHELF: 4 CHANNELS (APP.AHOY.OOO) -->
    <div class="bottom-section">
      <div class="shelf-header">
        <span class="shelf-title">Curated Channels (4 Channels • app.ahoy.ooo)</span>
        <span class="shelf-meta" id="channel-counter">CH 101 of 104</span>
      </div>

      <div class="channels-row" id="channels-row">
        <!-- Rendered via JS -->
      </div>
    </div>
  </div>

  <!-- SCHEDULE DRAWER -->
  <div class="schedule-drawer" id="schedule-drawer">
    <div class="drawer-header">
      <span class="drawer-title" id="drawer-title">Program Rotation</span>
      <button class="glass-btn" onclick="toggleScheduleDrawer()">Close [B]</button>
    </div>
    <div class="drawer-list" id="drawer-list"></div>
  </div>

  <!-- CONTROLLER NAVIGATION BAR -->
  <div class="bottom-bar">
    <div class="key-hints">
      <span><span class="key-badge">◀▶</span> Surf Channels</span>
      <span><span class="key-badge">▲▼</span> Select / Shelf</span>
      <span><span class="key-badge">A</span> Play / Fullscreen</span>
      <span><span class="key-badge">B</span> Close Guide</span>
      <span><span class="key-badge">Y</span> Toggle Schedule</span>
      <span><span class="key-badge">X</span> Bookmark</span>
    </div>
    <div class="status-text">AHOY INDIE MEDIA • APPLE TV LIQUID GLASS</div>
  </div>

  <script>
    const CHANNELS = {channels_json};

    let selectedChannelIndex = 0;
    let selectedProgramIndex = 0;
    let currentFocusZone = 'channels'; // 'channels' | 'hero' | 'drawer'
    let heroActionIndex = 0;
    let playingChannel = null;
    let playingIndex = 0;
    let isPlaying = false;
    let isMuted = true;
    let scheduleOpen = false;

    const savedIds = new Set(JSON.parse(localStorage.getItem('Ahoy_Saved_Ids') || '[]'));

    // DOM Elements
    const mediaEl = document.getElementById('media-element');
    const audioEl = document.getElementById('audio-element');
    const billboardBackdrop = document.getElementById('billboard-backdrop');
    const radioStage = document.getElementById('radio-stage');
    const vinylArt = document.getElementById('vinyl-art');
    const unmuteBanner = document.getElementById('unmute-banner');

    const headerChannel = document.getElementById('header-channel');
    const headerNowplaying = document.getElementById('header-nowplaying');
    const heroTag = document.getElementById('hero-tag');
    const heroTitle = document.getElementById('hero-title');
    const heroDesc = document.getElementById('hero-desc');
    const heroStatusPill = document.getElementById('hero-status-pill');
    const playText = document.getElementById('play-text');
    const playIcon = document.getElementById('play-icon');
    const saveIndicator = document.getElementById('save-indicator');
    const channelCounter = document.getElementById('channel-counter');
    const channelsRow = document.getElementById('channels-row');

    const scheduleDrawer = document.getElementById('schedule-drawer');
    const drawerTitle = document.getElementById('drawer-title');
    const drawerList = document.getElementById('drawer-list');

    const heroButtons = [
      document.getElementById('btn-play'),
      document.getElementById('btn-fullscreen'),
      document.getElementById('btn-next'),
      document.getElementById('btn-save')
    ];

    function renderChannels() {{
      channelsRow.innerHTML = '';
      CHANNELS.forEach((ch, idx) => {{
        const tile = document.createElement('div');
        const isActive = idx === selectedChannelIndex;
        const isFocused = currentFocusZone === 'channels' && idx === selectedChannelIndex;

        tile.className = 'channel-tile' + (isActive ? ' active' : '') + (isFocused ? ' focused' : '');
        tile.innerHTML = `
          <div class="channel-tile-content">
            <div class="tile-top">
              <span class="tile-number">${{ch.number}}</span>
              <span class="tile-badge">${{isActive ? 'TUNED' : 'LIVE'}}</span>
            </div>
            <div class="tile-info">
              <div class="tile-name">${{ch.name}}</div>
              <div class="tile-tagline">${{ch.tagline}}</div>
            </div>
          </div>
        `;

        tile.style.backgroundImage = `linear-gradient(180deg, rgba(14, 18, 28, 0.78) 0%, rgba(6, 8, 14, 0.96) 100%), url("${{ch.thumb}}")`;
        tile.style.backgroundSize = 'cover';
        tile.style.backgroundPosition = 'center';

        tile.onclick = () => {{
          currentFocusZone = 'channels';
          tuneChannel(idx);
        }};

        channelsRow.appendChild(tile);
      }});

      channelCounter.innerText = `CH ${{CHANNELS[selectedChannelIndex].number}} of 104`;
    }}

    function tuneChannel(idx) {{
      selectedChannelIndex = idx;
      selectedProgramIndex = 0;
      renderChannels();
      const ch = CHANNELS[idx];
      if (ch.videos.length > 0) {{
        playItem(ch, 0);
      }}
      renderDrawer();
      updateFocus();
    }}

    function playItem(ch, idx) {{
      playingChannel = ch;
      playingIndex = idx;
      const item = ch.videos[idx];
      if (!item) return;

      const thumb = item.thumbnail || ch.thumb;
      billboardBackdrop.style.backgroundImage = `url("${{thumb}}")`;

      headerChannel.innerText = `CH ${{ch.number}} • ${{ch.name}}`;
      headerNowplaying.innerText = `${{item.title}} (${{item.host || 'Ahoy'}})`;

      heroTag.innerText = ch.number === '103' ? 'AHOY RADIO 24/7' : 'AHOY LIVE BROADCAST';
      heroTitle.innerText = item.title;
      heroDesc.innerText = item.description || `${{item.title}} performing live on Ahoy Indie Media. Continuous broadcast on ${{ch.name}}.`;
      heroStatusPill.innerText = `ON AIR • ${{item.host || 'Ahoy'}}`;

      updateSaveBadge();

      if (item.category === 'radio' || (item.url && item.url.endsWith('.mp3'))) {{
        // RADIO MODE
        mediaEl.pause();
        mediaEl.style.opacity = '0';
        radioStage.style.display = 'flex';
        vinylArt.src = thumb;

        audioEl.src = item.url;
        audioEl.muted = isMuted;
        audioEl.play().then(() => {{
          isPlaying = true;
          updatePlayBtn();
        }}).catch(() => {{
          isPlaying = false;
          updatePlayBtn();
        }});
      }} else {{
        // VIDEO MODE
        audioEl.pause();
        radioStage.style.display = 'none';
        mediaEl.style.opacity = '1';
        mediaEl.poster = thumb;
        mediaEl.src = item.url;
        mediaEl.muted = isMuted;
        mediaEl.play().then(() => {{
          isPlaying = true;
          updatePlayBtn();
        }}).catch(() => {{
          isPlaying = false;
          updatePlayBtn();
          unmuteBanner.style.display = 'flex';
        }});
      }}

      renderDrawer();
    }}

    function enableAudio() {{
      isMuted = false;
      mediaEl.muted = false;
      audioEl.muted = false;
      mediaEl.play().catch(() => {{}});
      audioEl.play().catch(() => {{}});
      unmuteBanner.style.display = 'none';
      isPlaying = true;
      updatePlayBtn();
    }}

    function togglePlay() {{
      const isRadio = playingChannel && playingChannel.number === '103';
      const player = isRadio ? audioEl : mediaEl;

      if (isMuted) {{
        enableAudio();
        return;
      }}

      if (player.paused) {{
        player.play().catch(() => {{}});
        isPlaying = true;
      }} else {{
        player.pause();
        isPlaying = false;
      }}
      updatePlayBtn();
    }}

    function updatePlayBtn() {{
      if (isPlaying) {{
        playIcon.innerText = '❚❚';
        playText.innerText = 'Pause';
      }} else {{
        playIcon.innerText = '▶';
        playText.innerText = 'Play Live';
      }}
    }}

    function playNext() {{
      if (!playingChannel) return;
      const nextIdx = (playingIndex + 1) % playingChannel.videos.length;
      playItem(playingChannel, nextIdx);
    }}

    mediaEl.onended = playNext;
    audioEl.onended = playNext;

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }} else {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }}

    function toggleSaveCurrent() {{
      if (!playingChannel) return;
      const item = playingChannel.videos[playingIndex];
      if (!item) return;

      if (savedIds.has(item.id)) {{
        savedIds.delete(item.id);
      }} else {{
        savedIds.add(item.id);
      }}
      localStorage.setItem('Ahoy_Saved_Ids', JSON.stringify(Array.from(savedIds)));
      updateSaveBadge();
    }}

    function updateSaveBadge() {{
      if (!playingChannel) return;
      const item = playingChannel.videos[playingIndex];
      const isSaved = item && savedIds.has(item.id);
      if (isSaved) {{
        saveIndicator.innerText = '★ SAVED IN LIBRARY';
        saveIndicator.classList.add('active');
      }} else {{
        saveIndicator.innerText = '[X] SAVE TO LIBRARY';
        saveIndicator.classList.remove('active');
      }}
    }}

    function toggleScheduleDrawer() {{
      scheduleOpen = !scheduleOpen;
      if (scheduleOpen) {{
        scheduleDrawer.classList.add('open');
        currentFocusZone = 'drawer';
        renderDrawer();
      }} else {{
        scheduleDrawer.classList.remove('open');
        currentFocusZone = 'channels';
      }}
      updateFocus();
    }}

    function renderDrawer() {{
      if (!playingChannel) return;
      drawerTitle.innerText = `${{playingChannel.name}} • SCHEDULE (${{playingChannel.videos.length}} ROTATIONS)`;
      drawerList.innerHTML = '';
      playingChannel.videos.forEach((vid, idx) => {{
        const item = document.createElement('div');
        const isCurrent = idx === playingIndex;
        item.className = 'sched-item' + (isCurrent ? ' playing' : '');
        item.innerHTML = `
          <div>
            <div style="font-weight: 700; font-size: 14px; color: #FFF;">${{vid.title}}</div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.6);">${{vid.host || 'Ahoy'}}</div>
          </div>
          <span style="font-size: 11px; font-weight: 900; color: ${{isCurrent ? 'var(--ahoy-accent)' : 'rgba(255,255,255,0.5)'}};">
            ${{isCurrent ? 'PLAYING NOW' : 'ON AIR'}}
          </span>
        `;
        item.onclick = () => {{
          playItem(playingChannel, idx);
          toggleScheduleDrawer();
        }};
        drawerList.appendChild(item);
      }});
    }}

    function updateFocus() {{
      // Update channel tiles focus
      const tiles = channelsRow.querySelectorAll('.channel-tile');
      tiles.forEach((t, idx) => {{
        if (currentFocusZone === 'channels' && idx === selectedChannelIndex) {{
          t.classList.add('focused');
        }} else {{
          t.classList.remove('focused');
        }}
      }});

      // Update hero buttons focus
      heroButtons.forEach((btn, idx) => {{
        if (currentFocusZone === 'hero' && idx === heroActionIndex) {{
          btn.classList.add('focused');
        }} else {{
          btn.classList.remove('focused');
        }}
      }});
    }}

    // KEYBOARD & GAMEPAD CONTROLLER NAVIGATION
    window.addEventListener('keydown', (e) => {{
      if (scheduleOpen) {{
        if (e.key === 'Escape' || e.key === 'b' || e.key === 'B') {{
          toggleScheduleDrawer();
          return;
        }}
      }}

      switch(e.key) {{
        case 'ArrowLeft':
          if (currentFocusZone === 'channels') {{
            selectedChannelIndex = (selectedChannelIndex - 1 + CHANNELS.length) % CHANNELS.length;
            tuneChannel(selectedChannelIndex);
          }} else if (currentFocusZone === 'hero') {{
            heroActionIndex = (heroActionIndex - 1 + heroButtons.length) % heroButtons.length;
            updateFocus();
          }}
          break;

        case 'ArrowRight':
          if (currentFocusZone === 'channels') {{
            selectedChannelIndex = (selectedChannelIndex + 1) % CHANNELS.length;
            tuneChannel(selectedChannelIndex);
          }} else if (currentFocusZone === 'hero') {{
            heroActionIndex = (heroActionIndex + 1) % heroButtons.length;
            updateFocus();
          }}
          break;

        case 'ArrowUp':
          if (currentFocusZone === 'channels') {{
            currentFocusZone = 'hero';
            updateFocus();
          }}
          break;

        case 'ArrowDown':
          if (currentFocusZone === 'hero') {{
            currentFocusZone = 'channels';
            updateFocus();
          }}
          break;

        case 'Enter':
        case 'a':
        case 'A':
          if (currentFocusZone === 'hero') {{
            heroButtons[heroActionIndex].click();
          }} else if (currentFocusZone === 'channels') {{
            tuneChannel(selectedChannelIndex);
          }}
          break;

        case 'x':
        case 'X':
          toggleSaveCurrent();
          break;

        case 'y':
        case 'Y':
          toggleScheduleDrawer();
          break;

        case 'PageUp':
        case '[':
          selectedChannelIndex = (selectedChannelIndex - 1 + CHANNELS.length) % CHANNELS.length;
          tuneChannel(selectedChannelIndex);
          break;

        case 'PageDown':
        case ']':
          selectedChannelIndex = (selectedChannelIndex + 1) % CHANNELS.length;
          tuneChannel(selectedChannelIndex);
          break;

        case 'b':
        case 'B':
          if (scheduleOpen) toggleScheduleDrawer();
          else {{
            currentFocusZone = 'channels';
            updateFocus();
          }}
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
        checkBtn(4, 'PageUp');
        checkBtn(5, 'PageDown');
        checkBtn(0, 'A');
        checkBtn(1, 'B');
        checkBtn(2, 'X');
        checkBtn(3, 'Y');
      }}
      requestAnimationFrame(pollGamepad);
    }}
    window.addEventListener('gamepadconnected', () => requestAnimationFrame(pollGamepad));
    requestAnimationFrame(pollGamepad);

    // Initial boot
    tuneChannel(0);
  </script>
</body>
</html>
"""

# Synchronize across all targets:
# 1. AhoyXbox/Web/index.html
target_xbox = root / 'AhoyXbox/Web/index.html'
target_xbox.parent.mkdir(parents=True, exist_ok=True)
with open(target_xbox, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Updated {target_xbox}")

# 2. dist/store_assets/tv_app_preview.html
target_dist = root / 'dist/store_assets/tv_app_preview.html'
target_dist.parent.mkdir(parents=True, exist_ok=True)
with open(target_dist, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Updated {target_dist}")

# 3. Artifact for user browser preview
target_art = Path('/Users/agworkywork/.gemini/antigravity/brain/16a4042b-c7c9-4978-be35-735909a8ed76/ahoy_tv_frontend.html')
target_art.parent.mkdir(parents=True, exist_ok=True)
with open(target_art, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Updated {target_art}")
