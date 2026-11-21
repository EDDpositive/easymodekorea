# Android app (Trusted Web Activity)

The Android app is the website opened full screen, with no browser bar. Site updates reach the app at once; a new upload to Play is only needed when the icon, the name or Google's yearly target-version rule changes.

| File | What it is |
|---|---|
| `twa-manifest.json` | App settings for Bubblewrap 1.27 (package `com.easymodekorea.app`, colors, icons, shortcuts, version). |
| `fingerprints.json` | Public certificate fingerprints. The build writes them to `/.well-known/assetlinks.json`, which is what removes the browser bar. |
| `prepare_build.py` | Used by the workflow: points icon addresses at the commit being built. |
| `sign-aab.ps1` | Signs the bundle on the owner's PC. The owner types the password; nothing secret is stored in the repo or on GitHub. |

## Build path, step by step

1. **Build (GitHub, no secrets).** Actions > *Android app bundle* > Run workflow. Leave the version boxes empty for the first build; for a later upload enter a version code one higher than the last one. The run produces the artifact `emk-android-unsigned` with an unsigned `.aab`, and fails if the app asks for any sensitive permission.
2. **Sign (owner's PC).** Java 17 must be installed once (`winget install EclipseAdoptium.Temurin.17.JDK`). Then, from the repo folder:
   `powershell -ExecutionPolicy Bypass -File android\sign-aab.ps1`
   The first run creates the upload key in `%USERPROFILE%\.emk-android\emk-upload.jks` and asks for a new password. Every run downloads the newest unsigned bundle, signs it, and prints the upload key's SHA-256 fingerprint and the path of the signed file.
3. **Upload (owner, Play Console).** Upload the signed `.aab` to a closed-testing release. Play then shows the *app signing key* fingerprint under Test and release > App integrity > App signing.
4. **Link the app to the site.** Put the app signing key fingerprint (and, for testing a locally installed build, the upload key fingerprint) into `fingerprints.json`, run `python src/build.py`, and merge. Until this is live the app still works but shows a thin browser bar at the top.
5. **Check.** `https://easymodekorea.com/.well-known/assetlinks.json` lists the fingerprint, and the app opens without a browser bar.

Keep the key file and its password backed up outside the repo. If both are lost, Google can reset the upload key on request, which takes a few days.
