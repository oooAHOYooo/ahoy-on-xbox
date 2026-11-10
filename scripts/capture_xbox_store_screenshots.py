#!/usr/bin/env python3
import subprocess
import time
from pathlib import Path

ROOT = Path("/Users/agworkywork/ahoy-on-xbox")
HTML_FILE = ROOT / "docs/xbox-ui-preview.html"
OUT_STORE = ROOT / "dist/store_assets/ready_for_store_upload"
OUT_NEWS = ROOT / "dist/newsletter_assets"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

OUT_STORE.mkdir(parents=True, exist_ok=True)
OUT_NEWS.mkdir(parents=True, exist_ok=True)

base_html = HTML_FILE.read_text(encoding="utf-8")

# Style injection for 1920x1080 full 10-foot TV capture
screen_override_css = """
<style id="screenshot-overrides">
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    width: 1920px !important;
    height: 1080px !important;
    overflow: hidden !important;
    background: #08090C !important;
  }
  #xbox-preview {
    max-width: 1920px !important;
    width: 1920px !important;
    height: 1080px !important;
    margin: 0 !important;
  }
  #xbox-preview .xp-screen {
    width: 1920px !important;
    height: 1080px !important;
    aspect-ratio: auto !important;
  }
  #xbox-preview .xp-controls {
    display: none !important;
  }
  #xbox-preview .xp-top {
    height: 90px !important;
    padding: 0 52px !important;
  }
  #xbox-preview .xp-shelf {
    padding: 16px 52px 20px !important;
  }
  #xbox-preview .xp-hero {
    left: 52px !important;
    bottom: 34% !important;
  }
</style>
"""

scenes = [
    {
        "name": "Live TV Guide",
        "store_file": OUT_STORE / "04_Screenshot_Live_TV_1920x1080.png",
        "news_file": OUT_NEWS / "newsletter_screenshot_1_live_guide.png",
        "script": """
          setTimeout(() => {
            if (typeof act === 'function') {
              // Ensure Section 0 (Live TV)
              tabs[0].click();
            }
          }, 300);
        """
    },
    {
        "name": "On Demand Video Shelf",
        "store_file": OUT_STORE / "05_Screenshot_On_Demand_1920x1080.png",
        "news_file": OUT_NEWS / "newsletter_screenshot_2_on_demand.png",
        "script": """
          setTimeout(() => {
            tabs[1].click();
          }, 300);
        """
    },
    {
        "name": "Music & Audio",
        "store_file": OUT_STORE / "06_Screenshot_Music_1920x1080.png",
        "news_file": None,
        "script": """
          setTimeout(() => {
            tabs[2].click();
          }, 300);
        """
    },
    {
        "name": "Radio & Broadcasts",
        "store_file": OUT_STORE / "07_Screenshot_Podcasts_1920x1080.png",
        "news_file": None,
        "script": """
          setTimeout(() => {
            tabs[3].click();
          }, 300);
        """
    },
    {
        "name": "Ahoy ID Device Pairing",
        "store_file": OUT_STORE / "08_Screenshot_Pairing_1920x1080.png",
        "news_file": OUT_NEWS / "newsletter_screenshot_3_device_sync.png",
        "script": """
          setTimeout(() => {
            tabs[0].click();
            openPairModal();
          }, 400);
        """
    }
]

tmp_html = ROOT / "dist/temp_render.html"

for sc in scenes:
    print(f"Capturing: {sc['name']}...")
    injection = f"{screen_override_css}<script>{sc['script']}</script></body>"
    modified_html = base_html.replace("</body>", injection)
    tmp_html.write_text(modified_html, encoding="utf-8")

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1920,1080",
        f"--screenshot={sc['store_file']}",
        f"file://{tmp_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  -> Saved Store: {sc['store_file'].name}")

    if sc["news_file"]:
        # Copy to newsletter destination
        sc["news_file"].write_bytes(sc["store_file"].read_bytes())
        print(f"  -> Saved Newsletter: {sc['news_file'].name}")

if tmp_html.exists():
    tmp_html.unlink()

print("All screenshots captured successfully!")
