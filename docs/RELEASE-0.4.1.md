# AHOY TV 0.4.1 — Microsoft Store handoff

Version 0.4.1.0 targets x64 Xbox only with Store identity `AhoyIndieMedia.AHOYTV` and publisher `CN=A431E267-D7FE-4CF0-84A6-865308AC997C`.

## What changed

Video, music, radio and TV rotations now load from the public app.ahoy.ooo APIs when the app opens. Each feed has its own timeout and cached fallback. Radio entry uses the manifest's ordered items and epoch to find the current track. TV rotation content comes from the API, but exact website EPG timing is not exposed by that endpoint and remains unverified. This release does not add a claim of verified live broadcasting or 4K device playback.

## Package

Use the `.msixupload` from the successful GitHub Actions run for the release commit. Do not upload the old 0.1.0 or 0.4.0 package. Confirm version 0.4.1.0 and the assigned identity in Partner Center after processing. CI compiles native Debug, Release and Store upload builds, and runs catalog adapter checks. It does not submit to Microsoft or run device acceptance or Windows App Certification Kit.

## Screenshots

The older images generated from `docs/xbox-ui-preview.html` are browser prototype captures. They do not represent verified native application screenshots and should not be uploaded as such. The old Music and Pairing files show the wrong scene.

Capture the native release on Xbox. Required scenes for this handoff: TV guide, On Demand (including DUO 4K if desired), Music, and Radio. Do not add simulated pairing screens or claim features absent from the native app. Existing icon, poster and hero artwork can be reused after visual review.

Screenshots must be captured from the native app on an Xbox console. A Windows screenshot or the HTML prototype is not an Xbox capture. No console is available in this session, so actual Xbox screenshots and controller acceptance remain pending. Existing preview files are reference material only.

## Before submitting

- Install and launch this release on the Xbox. Test controller navigation, playback, music, radio, fullscreen/back, suspend/resume, pairing/save and network recovery.
- Confirm newly published videos appear after reopening and that DUO 4K plays correctly. The upload title alone does not prove 4K decoding on Xbox.
- Run Windows App Certification Kit and resolve failures.
- Complete real screenshots and review listing copy, support/privacy links, ratings and device targeting.
- Check the live Partner Center state; historical approval claims in older documents are not current verification. Uploading remains the user's action.

The earlier uncommitted native navigation edits are preserved in a named Git stash. They predate the fetched native redesign and were not applied over this release. The existing Partner Center CLI setup note is retained as documentation, with no credentials added.
