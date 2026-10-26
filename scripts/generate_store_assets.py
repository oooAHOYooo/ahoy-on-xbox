import subprocess
from pathlib import Path

OUT_DIR = Path("/Users/agworkywork/ahoy-on-xbox/dist/store_assets")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def render(html, out, w, h):
    tmp = OUT_DIR / "temp.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", f"--window-size={w},{h}", f"--screenshot={out}", f"file://{tmp}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if tmp.exists(): tmp.unlink()
    print(f"Rendered: {out.name}")

logo_src = "file:///Users/agworkywork/ahoy-on-xbox/dist/store_assets/ahoy_official_white.png"

# Apple TV style: [AHOY] tv
badge_html = f"""
<div style="display:flex; align-items:flex-end; justify-content:center;">
  <img src="{logo_src}" style="height:{{height}}px; object-fit:contain;">
  <span style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size:{{font_size}}px; font-weight:800; color:#FFFFFF; margin-left:14px; margin-bottom:{{margin_b}}px; letter-spacing:-0.5px; opacity:0.95;">tv</span>
</div>
"""

# 1. 1:1 Box Art (1080 x 1080)
render(f"""<!DOCTYPE html><html><body style="margin:0; width:1080px; height:1080px; background:#0B0E14; display:flex; align-items:center; justify-content:center;">
{badge_html.format(height=135, font_size=75, margin_b=10)}
</body></html>""", OUT_DIR / "box_art_1_1.png", 1080, 1080)

# 2. 9:16 Poster Art (720 x 1080)
render(f"""<!DOCTYPE html><html><body style="margin:0; width:720px; height:1080px; background:#0B0E14; display:flex; align-items:center; justify-content:center;">
{badge_html.format(height=95, font_size=52, margin_b=8)}
</body></html>""", OUT_DIR / "poster_art_9_16.png", 720, 1080)

# 3. Branded Key Art (584 x 800)
render(f"""<!DOCTYPE html><html><body style="margin:0; width:584px; height:800px; background:#0B0E14; display:flex; align-items:center; justify-content:center; padding-bottom:120px; box-sizing:border-box;">
{badge_html.format(height=80, font_size=44, margin_b=6)}
</body></html>""", OUT_DIR / "branded_key_art_584x800.png", 584, 800)

# 4. Titled Hero Art (1920 x 1080)
render(f"""<!DOCTYPE html><html><body style="margin:0; width:1920px; height:1080px; background:#0B0E14; display:flex; align-items:center; justify-content:center;">
{badge_html.format(height=160, font_size=88, margin_b=12)}
</body></html>""", OUT_DIR / "titled_hero_art_1920x1080.png", 1920, 1080)

# 5. Sips downscales for tile sizes
for s in [300, 150, 71]:
    subprocess.run(["sips", "-z", str(s), str(s), str(OUT_DIR / "box_art_1_1.png"), "--out", str(OUT_DIR / f"app_tile_{s}x{s}.png")], check=True, stdout=subprocess.DEVNULL)
    print(f"Generated tile: {s}x{s}")

print("Done!")
