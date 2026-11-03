# Microsoft Store release handoff

Status: **PROCESSED FOR PUBLICATION (Live in Store within ~2 hours)** as of November 3, 2026. Official package targeting Windows 10/11 Desktop and Xbox passed Microsoft certification and is replicating across global Store CDNs.

## Distribution route

Native UWP media app targeting Windows.Universal, verified and submitted for **Windows 10/11 Desktop** and **Windows 10/11 Xbox**. Packaged and uploaded via automated CI pipeline to Partner Center.

## Account and identity

- **Account Status**: Verified Microsoft Store Developer account under **Ahoy Indie Media**.
- **Product Name**: **AHOY TV** (MSIX / UWP App).
- **Package Identity Name**: `AhoyIndieMedia.AHOYTV`
- **Publisher**: `CN=A431E267-D7FE-4CF0-84A6-865308AC997C`
- **Publisher Display Name**: `Ahoy Indie Media`
- **Store ID**: `9N6QB77PD6RT`
- **Direct Store URL**: https://apps.microsoft.com/detail/9N6QB77PD6RT
- **Store Protocol Link**: `ms-windows-store://pdp/?productid=9N6QB77PD6RT`
- **Package Family Name (PFN)**: `AhoyIndieMedia.AHOYTV_ga5cs1wvjrpmc`
- **MSA App ID**: `8be79778-08a1-4c98-85f5-3064da66df73`
- **Current Submission**: Submission 1 — Successfully processed and approved on Nov 3, 2026. Auto-publishing active (visible worldwide within 2 hours).

## Device acceptance

- Build Debug x64 on Windows; launch and play each channel.
- Run on an Xbox console, verify every focus target using only the controller, and test the media remote if supported.
- Check TV safe area, 720p/1080p/4K output scaling, readable text, and visible focus.
- Test pause/play, seek, fullscreen entry/exit, B/back, system media commands, suspend/resume, and app termination/relaunch.
- Verify end-of-video advancement, one-video loop, changing channels while playing, and retry after network loss.
- Confirm HTTPS sources, audio/video codecs, buffering behavior, captions, and accessibility with Narrator.
- Confirm no uncontrolled playback after app suspension or navigation, and no memory growth across long queues.

## Packaging and listing

- Replace provisional generated tile artwork with approved Ahoy brand assets.
- Capture actual Windows and Xbox screenshots after device testing.
- Suggested working title: Ahoy.
- Draft short description: Independent culture on your big screen.
- Draft description: Browse independent videos from Ahoy. Discover music, skating, disc golf, and more in curated queues that keep playing.
- Describe actual behavior. Do not advertise live broadcasts, a TV schedule, captions, background audio, or advertising that is not implemented and verified.
- Create the Store upload package through Visual Studio with the assigned identity and release settings.
- Run Windows App Certification Kit and resolve failures; retain results and console test notes.
- Complete content ratings, privacy, markets, device targeting, certification notes, and submission review in Partner Center.

Publication remains a separate account action after the package and listing are reviewable.
