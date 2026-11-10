# Ahoy for Xbox

Native UWP media-app starter for a controller-driven, big-screen Ahoy experience.

Xbox and Fire TV follow the same screen and interaction contract while using native controls on each platform. See [the shared TV UI contract](docs/TV-UI-CONTRACT.md).

## Current handoff

The current engineering state, timestamped session notes, changed files, verification limits, and next-day work queue are in [the November 6, 2026 handoff](docs/HANDOFF-2026-11-06.md). The older [Tuesday launch playbook](docs/HANDOFF-TUESDAY.md) is retained as a historical planning document and is not the current build or release status.

## UI preview

- [Controller-oriented UI preview fragment](docs/xbox-ui-preview.html) shows the Xbox screen and a clickable controller simulator. Focus the preview and use arrow keys to browse; Enter selects; `X` saves; `Y` opens the account pairing example; `B` closes it. The on-screen controller buttons provide the same actions.
- [Browser prototype](AhoyXbox/Web/index.html) is a standalone HTML mockup for desktop preview and interaction experiments. It is not packaged into the native UWP app.
- The shipped Xbox UI source is [MainPage.xaml](AhoyXbox/MainPage.xaml) with behavior in [MainPage.xaml.cs](AhoyXbox/MainPage.xaml.cs). The HTML preview demonstrates the shared layout; it does not replace compiling and running the native application.

## Shared TV interface

Xbox and Fire TV share the same user-facing sections, layout hierarchy, content-card behavior, and Ahoy color tokens. Each implementation remains native: WinUI/UWP controls and Xbox controller events on Xbox; Android TV views and Fire TV remote events on Fire TV. The shared contract is also present at `../ahoy-on-tv/docs/TV-UI-CONTRACT.md` in a sibling checkout. Keep the two copies synchronized when changing that contract.

**Verification snapshot — November 6, 2026, 3:54:07 PM EST / 20:54:07 UTC:** native Xbox layout alignment is recorded in commit `d4ded582e6c41bafe4fc1fdaa5caf2a9624b8799`. XAML structure and the HTML preview script were checked, but the native app has not been compiled or run on Windows/Xbox in this session. The HTML prototype and preview are visual aids, not an Xbox package and not a Microsoft Store connection.

| Shared action | Xbox mapping | Fire TV mapping |
| --- | --- | --- |
| Browse | D-pad / left stick; shoulder buttons move channels | D-pad |
| Change section | Triggers or the four header tabs | Header tabs / supported navigation controls |
| Select | A / focused control activation | Select / OK |
| Back / Guide | B | Back |
| Save | X | Not currently implemented as an account-synced action |
| Account pairing | Y opens the Xbox pairing overlay | Not currently implemented |
| Fullscreen | On-screen Fullscreen action | Native playback/guide behavior |

Focus on a live channel updates the hero preview; selecting it tunes the channel. Keep this separation consistent in both clients so browsing a card does not unexpectedly interrupt playback.

## Included

- TV layout with directional focus navigation and native playback controls.
- 36 available videos imported without rewriting titles, hosts, or media URLs from the local Ahoy catalog on October 26, 2026.
- Ahoy Mix, Music Videos, Skating, and G-Dub Disc Golf queues where matching content exists.
- Automatic next-video playback and queue looping; browsing another channel does not interrupt playback until a video is selected.
- Fullscreen playback, back handling, playback error messages, and Windows/Xbox package manifest.

These are curated on-demand queues. They are not synchronized live channels, an EPG, or ad-supported broadcasts. This repository is an initial implementation, not a certified Store release. Catalog availability and streaming rights need review before submission.

## Build on Windows

1. Install Visual Studio 2022 with UWP C# build tooling, Windows SDK 10.0.19041.0, and the .NET Native tools. Use the Visual Studio Installer individual components if the workload is not listed.
2. Open `AhoyXbox/AhoyXbox.csproj` and restore NuGet packages.
3. Select Debug / x64 and run on Local Machine first.
4. For Xbox testing, activate developer mode on a supported console, configure Remote Machine deployment, and use a local development signing certificate. The project leaves package signing disabled; configure signing before creating an installable package. Never commit certificates or private keys.
5. Test with a controller and remote, including fullscreen, back, pause/resume, offline failures, and automatic queue advancement.

From a Visual Studio Developer PowerShell:

```powershell
msbuild AhoyXbox/AhoyXbox.csproj /restore /p:Configuration=Debug /p:Platform=x64
```

The package uses the assigned AHOY TV Store identity. See [the current Xbox release handoff](docs/RELEASE-0.4.1.md) for package and screenshot status.

## Source checks on this Mac

```sh
python3 scripts/validate.py
```

These checks validate source structure, catalog consistency, and image dimensions. They do not compile C#, validate Store certification, or prove playback on Windows/Xbox.

## CI and Cross-Machine Workflow

- Repository: `https://github.com/oooAHOYooo/ahoy-on-xbox`
- Automated GitHub Actions CI runs on `windows-2022` hosted runners upon push or pull request to `main`.
- The CI pipeline runs `scripts/validate.py`, compiles Debug x64 and Release x64 (.NET Native), and attaches the compiled Debug build artifacts to each workflow run.
- Any development machine (Windows, Mac, or Linux) can contribute by cloning this repository:
  ```sh
  git clone https://github.com/oooAHOYooo/ahoy-on-xbox.git
  ```

## Raspberry Pi 4 & Kiosk Over-The-Air (OTA) Control

To eliminate flashing SD cards every time you update channels or UI, see the complete OTA architecture and remote control guide:
- [Ahoy Pi Instant UI Control & OTA Fleet Handoff](docs/AHOY-PI-OTA-HANDOFF.md)

## Next product milestones

1. Compile and exercise this native app on Windows and Xbox; fix device findings.
2. Add an approved HTTPS catalog endpoint with cached fallback and versioning.
3. Decide whether Ahoy needs true clock-synchronized channels. That requires scheduling, reliable duration metadata, tune-in offsets, and an editorial programming workflow.
4. Add search, captions where supplied, accessibility polish, and resume behavior following device tests.
5. Prepare Store artwork, privacy/support URLs, content ratings, certification notes, and the signed package.

Do not add advertising or claim FAST/live television until the relevant rights, infrastructure, and product decisions are in place.

## Automatic content feeds (0.4.1)

The native app fetches the following public feeds concurrently when it opens:

| Content | Endpoint |
| --- | --- |
| Published on-demand videos and metadata | `https://app.ahoy.ooo/api/shows` |
| Music tracks, albums and cover art | `https://app.ahoy.ooo/api/music` |
| Radio playlist, station name and broadcast epoch | `https://app.ahoy.ooo/api/radio/live` |
| TV channel names, items and rotation order | `https://app.ahoy.ooo/api/live-tv/channels` |

Published additions appear without another Store update once users install this version. Reopen the app to refresh; feeds do not refresh during playback. On-demand videos use the public server's release filtering. Radio entry calculates the current item and offset from the manifest epoch and ordered durations, seeking after media opens. The TV endpoint supplies rotations but no start/end timestamps: TV timing remains a local calculation, not a verified match to the website's EPG.

Each request times out after 10 seconds and independently falls back to its last valid device cache. On first use without a cache, bundled video/music/radio data and locally grouped video channels remain available. Empty valid feeds are respected. Offline data can contain older listings; streaming still needs connectivity. Navigation, branding, controller mappings and layout remain part of the installed app. Account pairing and library synchronization use the existing ID APIs. 4K playback and broadcast timing still require Windows/Xbox verification.

## Xbox-only submission

Release 0.4.1 targets `Windows.Xbox` explicitly. Windows CI is used to compile the Xbox UWP package; it is not a separate desktop release. Capture Store screenshots from the app running on Xbox. See [the release handoff](docs/RELEASE-0.4.1.md).
