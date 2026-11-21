# Signs the EasyModeKorea Android app bundle on this PC.
#
#   powershell -ExecutionPolicy Bypass -File android\sign-aab.ps1
#
# You type the key password yourself when asked. It is never saved, shown or sent anywhere.
# The key file lives outside the repo, in %USERPROFILE%\.emk-android, so it cannot be committed.
#
# What it does:
#   1. Finds Java (keytool and jarsigner). If Java is missing it tells you how to install it and stops.
#   2. First run only: creates your upload key (asks you to choose a password).
#   3. Downloads the newest unsigned bundle built by GitHub (or uses the file given with -Aab).
#   4. Signs it (asks for the password) and checks the signature.
#   5. Prints the key's SHA-256 fingerprint and where the signed file is.
param([string]$Aab = "")

$ErrorActionPreference = "Stop"
$KeyDir = Join-Path $env:USERPROFILE ".emk-android"
$Keystore = Join-Path $KeyDir "emk-upload.jks"
$Alias = "upload"
$Repo = "EDDpositive/easymodekorea"

function Find-JavaTool([string]$Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $roots = @($env:JAVA_HOME, "C:\Program Files\Eclipse Adoptium", "C:\Program Files\Microsoft", "C:\Program Files\Java", "C:\Program Files\Zulu") | Where-Object { $_ -and (Test-Path $_) }
    foreach ($root in $roots) {
        $hit = Get-ChildItem -Path $root -Recurse -Filter "$Name.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($hit) { return $hit.FullName }
    }
    return $null
}

$Keytool = Find-JavaTool "keytool"
$Jarsigner = Find-JavaTool "jarsigner"
if (-not $Keytool -or -not $Jarsigner) {
    Write-Host ""
    Write-Host "Java (JDK 17) is not installed on this PC. Install it once with this command, then run this script again:" -ForegroundColor Yellow
    Write-Host "    winget install EclipseAdoptium.Temurin.17.JDK"
    exit 1
}

New-Item -ItemType Directory -Force -Path $KeyDir | Out-Null

if (-not (Test-Path $Keystore)) {
    Write-Host ""
    Write-Host "No upload key yet. Creating one now." -ForegroundColor Cyan
    Write-Host "Choose a password (6+ characters) and type it twice. Keep it in your password manager:"
    Write-Host "without this file AND this password you cannot upload app updates."
    & $Keytool -genkeypair -v -keystore $Keystore -alias $Alias -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=EasyModeKorea"
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $Keystore)) { Write-Host "The key was not created." -ForegroundColor Red; exit 1 }
    Write-Host "Key created: $Keystore" -ForegroundColor Green
    Write-Host "Back up this file somewhere safe (not in the repo)."
}

$OutDir = Join-Path $KeyDir "out"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

if (-not $Aab) {
    Write-Host ""
    Write-Host "Downloading the newest unsigned bundle from GitHub..." -ForegroundColor Cyan
    $runId = (& gh run list --repo $Repo --workflow android-build.yml --status success --limit 1 --json databaseId --jq ".[0].databaseId")
    if (-not $runId) { Write-Host "No finished build found. Run the 'Android app bundle' workflow on GitHub first." -ForegroundColor Red; exit 1 }
    $dl = Join-Path $OutDir "download-$runId"
    if (Test-Path $dl) { Remove-Item -Recurse -Force $dl }
    & gh run download $runId --repo $Repo --name emk-android-unsigned --dir $dl
    if ($LASTEXITCODE -ne 0) { Write-Host "Download failed." -ForegroundColor Red; exit 1 }
    $Aab = (Get-ChildItem -Path $dl -Recurse -Filter "*.aab" | Select-Object -First 1).FullName
}
if (-not $Aab -or -not (Test-Path $Aab)) { Write-Host "Bundle file not found." -ForegroundColor Red; exit 1 }

$stamp = Get-Date -Format "yyyyMMdd-HHmm"
$Signed = Join-Path $OutDir "easymodekorea-$stamp.aab"
Copy-Item $Aab $Signed -Force

Write-Host ""
Write-Host "Signing. Type your key password when asked." -ForegroundColor Cyan
& $Jarsigner -sigalg SHA256withRSA -digestalg SHA-256 -keystore $Keystore $Signed $Alias
if ($LASTEXITCODE -ne 0) { Remove-Item $Signed -ErrorAction SilentlyContinue; Write-Host "Signing failed (wrong password?). Nothing was changed." -ForegroundColor Red; exit 1 }

& $Jarsigner -verify $Signed | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "The signature could not be verified." -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "Done. Signed bundle:" -ForegroundColor Green
Write-Host "    $Signed"
Write-Host ""
Write-Host "Upload key fingerprint (SHA-256). This is public; it is safe to share:" -ForegroundColor Cyan
& $Keytool -printcert -jarfile $Signed | Select-String "SHA256"
Write-Host ""
Write-Host "Next: upload the signed file in Play Console (Testing > Closed testing > Create new release)."
Start-Process explorer.exe "/select,`"$Signed`""
