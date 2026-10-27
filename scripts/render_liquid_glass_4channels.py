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
