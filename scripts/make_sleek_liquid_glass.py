#!/usr/bin/env python3
import re

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .xp-tab[aria-selected="true"] to be calm frosted glass with subtle pink indicator line
old_tab_style = """    #xbox-preview .xp-tab[aria-selected="true"] {
      background: var(--xp-pink);
      border-color: var(--xp-pink);
      color: #FFFFFF;
      box-shadow: 0 2px 10px rgba(255, 0, 96, 0.35);
    }"""

new_tab_style = """    #xbox-preview .xp-tab[aria-selected="true"] {
      background: rgba(255, 255, 255, 0.12) !important;
      border: 1px solid rgba(255, 255, 255, 0.24) !important;
      color: #FFFFFF !important;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.18) !important;
      position: relative !important;
    }
    #xbox-preview .xp-tab[aria-selected="true"]::after {
      content: "";
      position: absolute;
      bottom: -3px;
      left: 22%;
      right: 22%;
      height: 2px;
      background: rgba(255, 0, 96, 0.85);
      border-radius: 2px;
      box-shadow: 0 0 8px rgba(255, 0, 96, 0.6);
    }"""

if old_tab_style in content:
    content = content.replace(old_tab_style, new_tab_style, 1)

# 2. Update .xp-keycap for top bar (barely seeing the color, translucent subtle glass)
old_keycaps = """    .xp-keycap-x { background: var(--xp-blue); }
    .xp-keycap-y { background: var(--xp-gold); color: #17130a; }
    .xp-keycap-check { background: var(--xp-green); }"""

new_keycaps = """    .xp-keycap {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      font-size: 9px;
      font-weight: 800;
      flex-shrink: 0;
      line-height: 1;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .xp-keycap-x {
      background: rgba(59, 130, 246, 0.14);
      border: 1px solid rgba(59, 130, 246, 0.28);
      color: rgba(147, 197, 253, 0.95);
      box-shadow: 0 0 6px rgba(59, 130, 246, 0.2);
    }
    .xp-keycap-y {
      background: rgba(245, 158, 11, 0.14);
      border: 1px solid rgba(245, 158, 11, 0.28);
      color: rgba(253, 230, 138, 0.95);
      box-shadow: 0 0 6px rgba(245, 158, 11, 0.2);
    }
    .xp-keycap-check {
      background: rgba(34, 197, 94, 0.14);
      border: 1px solid rgba(34, 197, 94, 0.28);
      color: rgba(134, 239, 172, 0.95);
    }"""

if old_keycaps in content:
    content = content.replace(old_keycaps, new_keycaps, 1)

# 3. Update bottom controller buttons to be ultra-sleek, subtle & translucent (barely seeing color)
old_remote_action_css = """    /* LIQUID GLASS TINTED ACTION BUTTONS */
    #xbox-preview .xp-remote button.xp-btn-a {
      background: rgba(16, 124, 16, 0.28);
      border-color: rgba(34, 197, 94, 0.45);
      color: #4ADE80;
      box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.35), 0 0 14px rgba(34, 197, 94, 0.25);
    }
    #xbox-preview .xp-remote button.xp-btn-a:hover {
      background: rgba(16, 124, 16, 0.48);
      border-color: rgba(34, 197, 94, 0.7);
      color: #86EFAC;
      box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.5), 0 0 20px rgba(34, 197, 94, 0.45);
    }
    #xbox-preview .xp-remote button.xp-btn-b {
      background: rgba(232, 17, 35, 0.28);
      border-color: rgba(248, 113, 113, 0.45);
      color: #F87171;
      box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.35), 0 0 14px rgba(248, 113, 113, 0.25);
    }
    #xbox-preview .xp-remote button.xp-btn-b:hover {
      background: rgba(232, 17, 35, 0.48);
      border-color: rgba(248, 113, 113, 0.7);
      color: #FCA5A5;
      box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.5), 0 0 20px rgba(248, 113, 113, 0.45);
    }
    #xbox-preview .xp-remote button.xp-btn-x {
      background: rgba(0, 120, 215, 0.28);
      border-color: rgba(96, 165, 250, 0.45);
      color: #60A5FA;
      box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.35), 0 0 14px rgba(96, 165, 250, 0.25);
    }
    #xbox-preview .xp-remote button.xp-btn-x:hover {
      background: rgba(0, 120, 215, 0.48);
      border-color: rgba(96, 165, 250, 0.7);
      color: #93C5FD;
      box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.5), 0 0 20px rgba(96, 165, 250, 0.45);
    }
    #xbox-preview .xp-remote button.xp-btn-y {
      background: rgba(255, 140, 0, 0.28);
      border-color: rgba(251, 191, 36, 0.45);
      color: #FBBF24;
      box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.35), 0 0 14px rgba(251, 191, 36, 0.25);
    }
    #xbox-preview .xp-remote button.xp-btn-y:hover {
      background: rgba(255, 140, 0, 0.48);
      border-color: rgba(251, 191, 36, 0.7);
      color: #FDE68A;
      box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.5), 0 0 20px rgba(251, 191, 36, 0.45);
    }"""

new_remote_action_css = """    /* SLEEK & SEXY SUBTLE TRANSLUCENT XBOX BUTTONS */
    #xbox-preview .xp-remote button {
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
      background: rgba(255, 255, 255, 0.04) !important;
      backdrop-filter: blur(14px) !important;
      -webkit-backdrop-filter: blur(14px) !important;
      color: rgba(255, 255, 255, 0.6) !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 2px 6px rgba(0, 0, 0, 0.35) !important;
    }
    #xbox-preview .xp-remote button:hover {
      background: rgba(255, 255, 255, 0.09) !important;
      color: #FFFFFF !important;
      border-color: rgba(255, 255, 255, 0.2) !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18), 0 4px 10px rgba(0, 0, 0, 0.45) !important;
    }
    #xbox-preview .xp-remote button.xp-round-btn {
      width: 25px;
      height: 25px;
      font-size: 10px;
      font-weight: 800;
      border-radius: 50%;
    }
    #xbox-preview .xp-remote button.xp-btn-a {
      background: rgba(34, 197, 94, 0.06) !important;
      border-color: rgba(34, 197, 94, 0.18) !important;
      color: rgba(74, 222, 128, 0.8) !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 0 8px rgba(34, 197, 94, 0.12) !important;
    }
    #xbox-preview .xp-remote button.xp-btn-a:hover {
      background: rgba(34, 197, 94, 0.14) !important;
      border-color: rgba(34, 197, 94, 0.4) !important;
      color: #86EFAC !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 0 14px rgba(34, 197, 94, 0.28) !important;
    }
    #xbox-preview .xp-remote button.xp-btn-b {
      background: rgba(239, 68, 68, 0.06) !important;
      border-color: rgba(239, 68, 68, 0.18) !important;
      color: rgba(248, 113, 113, 0.8) !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 0 8px rgba(239, 68, 68, 0.12) !important;
    }
    #xbox-preview .xp-remote button.xp-btn-b:hover {
      background: rgba(239, 68, 68, 0.14) !important;
      border-color: rgba(239, 68, 68, 0.4) !important;
      color: #FCA5A5 !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 0 14px rgba(239, 68, 68, 0.28) !important;
    }
    #xbox-preview .xp-remote button.xp-btn-x {
      background: rgba(59, 130, 246, 0.06) !important;
      border-color: rgba(59, 130, 246, 0.18) !important;
      color: rgba(96, 165, 250, 0.8) !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 0 8px rgba(59, 130, 246, 0.12) !important;
    }
    #xbox-preview .xp-remote button.xp-btn-x:hover {
      background: rgba(59, 130, 246, 0.14) !important;
      border-color: rgba(59, 130, 246, 0.4) !important;
      color: #93C5FD !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 0 14px rgba(59, 130, 246, 0.28) !important;
    }
    #xbox-preview .xp-remote button.xp-btn-y {
      background: rgba(245, 158, 11, 0.06) !important;
      border-color: rgba(245, 158, 11, 0.18) !important;
      color: rgba(251, 191, 36, 0.8) !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 0 8px rgba(245, 158, 11, 0.12) !important;
    }
    #xbox-preview .xp-remote button.xp-btn-y:hover {
      background: rgba(245, 158, 11, 0.14) !important;
      border-color: rgba(245, 158, 11, 0.4) !important;
      color: #FDE68A !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 0 14px rgba(245, 158, 11, 0.28) !important;
    }"""

if old_remote_action_css in content:
    content = content.replace(old_remote_action_css, new_remote_action_css, 1)

# 4. Fix Timestamps & Button Size & Remove Star:
# In #xp-hero-music DOM:
old_hero_music_block = """          <!-- AUDIO PROGRESS SCRUBBER -->
          <div class="xp-music-scrubber-box">
            <div class="xp-music-scrubber-bar" id="xp-music-scrubber-bar" title="Click timeline to seek">
              <div class="xp-music-scrubber-fill" id="xp-music-scrubber-fill">
                <div class="xp-music-scrubber-thumb"></div>
              </div>
            </div>
            <div class="xp-music-scrubber-times">
              <span id="xp-music-time-cur">0:00</span>
              <span id="xp-music-time-total">3:00</span>
            </div>
          </div>

          <!-- AUDIO CONTROLS & UP NEXT -->
          <div class="xp-music-btn-row">
            <button class="xp-action" id="xp-music-play-btn" type="button">
              <span id="xp-music-play-label">▶ &nbsp; PLAY TRACK [A]</span>
            </button>
            <button class="xp-music-sub-btn" type="button" onclick="act('X')">
              <span>★ SAVE TO LIBRARY [X]</span>
            </button>
            <div class="xp-music-up-next" id="xp-music-up-next" onclick="act('ArrowRight')">
              <span class="xp-up-next-label">⏭ UP NEXT:</span>
              <span class="xp-up-next-song" id="xp-up-next-song">Song</span>
              <span class="xp-up-next-artist" id="xp-up-next-artist">Artist</span>
            </div>
          </div>"""

new_hero_music_block = """          <!-- AUDIO PROGRESS SCRUBBER -->
          <div class="xp-music-scrubber-box">
            <div class="xp-music-scrubber-bar" id="xp-music-scrubber-bar" title="Click timeline to seek">
              <div class="xp-music-scrubber-fill" id="xp-music-scrubber-fill">
                <div class="xp-music-scrubber-thumb"></div>
              </div>
            </div>
            <div class="xp-music-scrubber-times">
              <span class="xp-scrubber-time-cur" id="xp-music-time-cur">0:00</span>
              <span class="xp-scrubber-time-total" id="xp-music-time-total">3:00</span>
            </div>
          </div>

          <!-- UNIFIED SLEEK LIQUID GLASS BUTTONS (NO STAR, IDENTICAL 36PX HEIGHT) -->
          <div class="xp-music-btn-row">
            <button class="xp-action" id="xp-music-play-btn" type="button">
              <span id="xp-music-play-label">▶ &nbsp; PLAY TRACK [A]</span>
            </button>
            <button class="xp-music-sub-btn" id="xp-music-save-btn" type="button" onclick="act('X')">
              <span id="xp-music-save-label">SAVE TO LIBRARY [X]</span>
            </button>
          </div>"""

if old_hero_music_block in content:
    content = content.replace(old_hero_music_block, new_hero_music_block, 1)

# 5. Add exact unified button CSS, flex scrubber times, and sleek layout
unified_btn_css = """
    /* UNIFIED 36PX SLEEK LIQUID GLASS BUTTONS & PINNED TIMESTAMPS */
    #xbox-preview .xp-hero-music {
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      width: min(92%, 1120px) !important;
      gap: 32px !important;
    }
    #xbox-preview .xp-music-hero-left {
      flex-shrink: 0 !important;
    }
    #xbox-preview .xp-music-hero-right {
      flex: 1 1 auto !important;
      min-width: 0 !important;
    }
    #xbox-preview .xp-music-scrubber-box {
      width: 100% !important;
      max-width: 440px !important;
      margin-top: 6px !important;
    }
    #xbox-preview .xp-music-scrubber-times {
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      width: 100% !important;
      box-sizing: border-box !important;
      margin-top: 5px !important;
      font-size: 10px !important;
      color: #9A9AA6 !important;
      font-weight: 700 !important;
      font-family: -apple-system, BlinkMacSystemFont, "SF Mono", monospace !important;
      letter-spacing: 0.5px !important;
    }
    #xbox-preview .xp-scrubber-time-cur {
      text-align: left !important;
    }
    #xbox-preview .xp-scrubber-time-total {
      text-align: right !important;
    }

    #xbox-preview .xp-music-btn-row {
      display: flex !important;
      align-items: center !important;
      gap: 10px !important;
      margin-top: 14px !important;
      flex-wrap: nowrap !important;
    }
    #xbox-preview .xp-music-btn-row button {
      height: 36px !important;
      min-height: 36px !important;
      padding: 0 16px !important;
      margin: 0 !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 7px !important;
      border-radius: 999px !important;
      font-size: 11px !important;
      font-weight: 800 !important;
      letter-spacing: 0.04em !important;
      white-space: nowrap !important;
      box-sizing: border-box !important;
      line-height: 1 !important;
      background: rgba(255, 255, 255, 0.06) !important;
      border: 1px solid rgba(255, 255, 255, 0.14) !important;
      color: #FFFFFF !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
      cursor: pointer !important;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    #xbox-preview .xp-music-btn-row button:hover {
      background: rgba(255, 255, 255, 0.14) !important;
      border-color: rgba(255, 255, 255, 0.3) !important;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
      transform: translateY(-1px) !important;
    }
    #xbox-preview .xp-music-btn-row button:active {
      transform: translateY(1px) scale(0.98) !important;
    }
"""

content = content.replace("/* CALM LIQUID GLASS MUSIC BUTTONS */", unified_btn_css + "\n    /* CALM LIQUID GLASS MUSIC BUTTONS */", 1)

# 6. Update toggleSaveCurrentItem and renderSaveModal to keep Save button without stars
content = content.replace("toggleLabel.textContent = '★ SAVE TO LIBRARY [X]';", "toggleLabel.textContent = 'SAVE TO LIBRARY [X]';", 1)

with open('/Users/agworkywork/ahoy-on-xbox/docs/preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('/Users/agworkywork/ahoy-on-xbox/docs/xbox-ui-preview.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Sleek, sexy liquid glass Xbox buttons, exact twin button sizes, no star, and pinned timestamps installed!")
