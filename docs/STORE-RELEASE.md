# Microsoft Store release handoff

Status: source starter only. No Windows build, signed package, Xbox deployment, Partner Center product, or Store submission has been completed.

## Distribution route

Use a UWP media app targeting Windows.Universal, tested on Windows and Xbox. Microsoft's supported-technologies documentation covers UWP on Xbox, and its Xbox architecture guidance addresses media applications. A Windows PWA listing alone does not establish Xbox distribution eligibility. Confirm current Xbox app submission availability for the publisher account in Partner Center before investing in release packaging.

References checked October 26, 2026:

- https://learn.microsoft.com/en-us/windows/uwp/apps-for-xbox/supported-technologies
- https://github.com/MicrosoftDocs/windows-dev-docs/blob/docs/uwp/apps-for-xbox/application-architecture.md
- https://learn.microsoft.com/en-us/windows/uwp/publish/
- https://learn.microsoft.com/en-us/windows/uwp/xbox-apps/devkit-activation
- https://learn.microsoft.com/en-us/windows/apps/publish/store-policies

## Account and identity

- Enroll or use the existing Microsoft developer / Partner Center account.
- Reserve the intended Ahoy product name and confirm Xbox device-family submission eligibility.
- Associate the Visual Studio project with the Store product. Replace development Name, Publisher, and publisher display name with assigned values.
- Confirm supported markets, age ratings, content ownership, and media licenses. Public URLs alone do not prove redistribution or television streaming rights.
- Supply real privacy and support URLs and publisher contact details. Do not invent these.

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
