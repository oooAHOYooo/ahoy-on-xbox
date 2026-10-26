# Ahoy for Xbox and Windows

Native UWP media-app starter for a controller-driven, big-screen Ahoy experience.

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

Package identity is a development placeholder. Associate with the real Store product before generating a submission package. See [the release checklist](docs/STORE-RELEASE.md).

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

## Next product milestones

1. Compile and exercise this native app on Windows and Xbox; fix device findings.
2. Add an approved HTTPS catalog endpoint with cached fallback and versioning.
3. Decide whether Ahoy needs true clock-synchronized channels. That requires scheduling, reliable duration metadata, tune-in offsets, and an editorial programming workflow.
4. Add search, captions where supplied, accessibility polish, and resume behavior following device tests.
5. Prepare Store artwork, privacy/support URLs, content ratings, certification notes, and the signed package.

Do not add advertising or claim FAST/live television until the relevant rights, infrastructure, and product decisions are in place.
