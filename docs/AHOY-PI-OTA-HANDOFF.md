# Ahoy Pi: Instant UI Control & Over-The-Air (OTA) Fleet Handoff

> **Goal:** Eliminate SD card flashing entirely. Push UI changes and channel rotation updates instantly over the air, and control the Ahoy Pi remotely in real-time from your phone or browser.

---

## 1. The Core Architecture: Why Auto-Flashing Happened & How We Stop It

### The Old Workflow (Flashing Loop)
```
Change Code ➔ Rebuild Image ➔ Flash SD Card ➔ Insert into Pi ➔ Reboot (20+ minutes)
```

### The Modern Cloud-Hosted Kiosk Workflow (Instant OTA)
```
Git Push ➔ Cloud Host Deploys (15s) ➔ Ahoy Pi Hot-Reloads (Instant)
```

By decoupling the **Pi Operating System** (flashed once, forever) from the **Ahoy TV Application Layer** (hosted in the cloud and synced over the air), the Pi becomes a zero-maintenance "thin client" appliance.

---

## 2. Three Levels of Instant Control (From Easiest to Full Remote)

### Tier 1: Cloud-Hosted Kiosk URL (Deploy in 10 Minutes, No Re-flashing)
Instead of pointing the Pi's kiosk browser to a local file (`file:///home/pi/index.html`), point it to a live cloud endpoint:
- **Production URL:** `https://app.ahoy.ooo/tv` (or GitHub Pages / Cloudflare Pages: `https://oooahoyooo.github.io/ahoy-on-xbox/`)
- **How it updates:** Whenever code is pushed to `main`, GitHub Actions or Cloudflare Pages builds and deploys in seconds.
- **Auto-Refresh on Update:** A small script embedded in the HTML polls `/api/version` or GitHub commits every 60 seconds; if a new commit hash is detected, it smoothly reloads in the background without dropping frames.

#### Pi 4 Kiosk Boot Configuration (`/etc/xdg/autostart/ahoy-tv.desktop`)
```ini
[Desktop Entry]
Type=Application
Name=Ahoy TV Kiosk
Exec=/home/pi/launch-ahoy-tv.sh
Hidden=false
X-GNOME-Autostart-enabled=true
```

#### The Resilient Launch Script (`/home/pi/launch-ahoy-tv.sh`)
```bash
#!/usr/bin/env bash
# Prevent screen sleeping & hide mouse cursor
xset s off
xset -dpms
xset s noblank
unclutter -idle 0.5 -root &

# Wait for network connectivity
until ping -c1 1.1.1.1 >/dev/null 2>&1; do
    sleep 1
done

# Launch Chromium in locked Big Screen TV Kiosk Mode
chromium-browser \
    --kiosk \
    --noerrdialogs \
    --disable-infobars \
    --check-for-update-interval=3600 \
    --autoplay-policy=no-user-gesture-required \
    --enable-features=OverlayScrollbar \
    --disk-cache-size=1073741824 \
    --enable-gpu-rasterization \
    --ignore-gpu-blocklist \
    "https://oooahoyooo.github.io/ahoy-on-xbox/AhoyXbox/Web/index.html"
```

---

### Tier 2: Real-Time Remote Control (Phone / Web Controller)
Want to sit on the couch or be in another room and control what is playing on the Ahoy Pi TV instantly without touching the keyboard?

```
[Phone / Laptop at ahoy.ooo/remote]
             │ (WebSockets / SSE)
             ▼
      [Supabase Realtime / Ably / Pusher]
             │
             ▼
      [Ahoy Pi TV Screen]
      (Changes channels, skips, pauses, sets volume instantly)
```

#### Embedded Client Listener (Added to `AhoyXbox/Web/index.html`):
```javascript
// Connect to Ahoy Remote Control Channel
const channelId = "ahoy-tv-living-room";
const eventSource = new EventSource(`https://api.ahoy.ooo/remote/stream?channel=${channelId}`);

eventSource.onmessage = (event) => {
    const cmd = JSON.parse(event.data);
    switch(cmd.action) {
        case "TUNE_CHANNEL":
            tuneChannel(cmd.channelIndex); // 0, 1, 2, 3
            break;
        case "PLAY_ITEM":
            playItem(CHANNELS[cmd.channelIndex], cmd.itemIndex);
            break;
        case "PAUSE":
            togglePlay();
            break;
        case "RELOAD":
            window.location.reload(true);
            break;
    }
};
```

---

### Tier 3: Local Offline-First Cache (If WiFi Drops, Video Never Stops)
The Raspberry Pi caches upcoming MP4 video segments and MP3 audio streams into IndexedDB or Service Worker Cache Storage.
- When online: Streams live and updates catalog dynamically.
- When offline: Falls back to cached local library seamlessly with zero interruptions.

---

## 3. Remote Management Commands (SSH from your Mac)

Once your Pi is on the local network, you can run commands directly from your Mac terminal without touching the Pi:

```bash
# 1. Force Ahoy TV to reload the latest UI instantly:
ssh pi@ahoy-pi.local "export DISPLAY=:0 && xdotool key F5"

# 2. Check Chromium memory & performance:
ssh pi@ahoy-pi.local "ps aux | grep chromium"

# 3. Reboot the Pi remotely if needed:
ssh pi@ahoy-pi.local "sudo reboot"
```

---

## 4. Setup Steps for the Next Raspberry Pi Flash (The Last Flash You'll Ever Do)

1. **Flash Base Image:** Flash Raspberry Pi OS Lite (64-bit) or Desktop to the SD card with SSH enabled.
2. **Install Kiosk Tools:**
   ```bash
   sudo apt update && sudo apt install -y chromium-browser unclutter xdotool
   ```
3. **Set Cloud URL:** Place the launch script above in `/home/pi/launch-ahoy-tv.sh`.
4. **Never flash again:** Any update you make to `AhoyXbox/Web/index.html` or channels in git deploys immediately over the air.
