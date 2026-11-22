# Signs the EasyModeKorea Android app bundle on this PC. On-screen messages are in Korean for the owner.
#
#   powershell -ExecutionPolicy Bypass -File android\sign-aab.ps1
#
# The owner types the key password when asked. It is never saved, shown or sent anywhere.
# The key file lives outside the repo, in %USERPROFILE%\.emk-android, so it cannot be committed.
# Keep this file saved as UTF-8 with BOM, or Windows PowerShell will garble the Korean text.
#
# What it does:
#   1. Finds Java (keytool and jarsigner). If Java is missing it says how to install it and stops.
#   2. First run only: creates the upload key (asks the owner to choose a password).
#   3. Downloads the newest unsigned bundle built by GitHub (or uses the file given with -Aab).
#   4. Signs it (asks for the password) and checks the signature.
#   5. Prints the key's SHA-256 fingerprint and where the signed file is.
param([string]$Aab = "", [switch]$NoOpen)

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
    Write-Host "이 PC에 자바(JDK 17)가 없습니다. 아래 명령으로 한 번 설치한 뒤, 이 스크립트를 다시 실행하세요:" -ForegroundColor Yellow
    Write-Host "    winget install EclipseAdoptium.Temurin.17.JDK"
    exit 1
}

New-Item -ItemType Directory -Force -Path $KeyDir | Out-Null

if (-not (Test-Path $Keystore)) {
    Write-Host ""
    Write-Host "업로드 열쇠가 아직 없습니다. 지금 만듭니다." -ForegroundColor Cyan
    Write-Host "비밀번호(6자 이상)를 직접 정해서 두 번 입력하세요. 입력하는 글자는 화면에 보이지 않습니다."
    Write-Host "이 비밀번호와 열쇠 파일이 둘 다 있어야 앱 업데이트를 올릴 수 있습니다. 비밀번호 관리자에 보관하세요."
    & $Keytool -genkeypair -v -keystore $Keystore -alias $Alias -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=EasyModeKorea"
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $Keystore)) { Write-Host "열쇠를 만들지 못했습니다." -ForegroundColor Red; exit 1 }
    Write-Host "열쇠를 만들었습니다: $Keystore" -ForegroundColor Green
    Write-Host "이 파일을 안전한 곳에 따로 백업하세요. 저장소 폴더에는 넣지 마세요."
}

$OutDir = Join-Path $KeyDir "out"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

if (-not $Aab) {
    Write-Host ""
    Write-Host "GitHub에서 최신 앱 파일(서명 전)을 받는 중..." -ForegroundColor Cyan
    $runId = (& gh run list --repo $Repo --workflow android-build.yml --status success --limit 1 --json databaseId --jq ".[0].databaseId")
    if (-not $runId) { Write-Host "끝난 빌드가 없습니다. GitHub에서 'Android app bundle' 작업을 먼저 실행하세요." -ForegroundColor Red; exit 1 }
    $dl = Join-Path $OutDir "download-$runId"
    if (Test-Path $dl) { Remove-Item -Recurse -Force $dl }
    & gh run download $runId --repo $Repo --name emk-android-unsigned --dir $dl
    if ($LASTEXITCODE -ne 0) { Write-Host "내려받기에 실패했습니다." -ForegroundColor Red; exit 1 }
    $Aab = (Get-ChildItem -Path $dl -Recurse -Filter "*.aab" | Select-Object -First 1).FullName
}
if (-not $Aab -or -not (Test-Path $Aab)) { Write-Host "앱 파일을 찾지 못했습니다." -ForegroundColor Red; exit 1 }

$stamp = Get-Date -Format "yyyyMMdd-HHmm"
$Signed = Join-Path $OutDir "easymodekorea-$stamp.aab"
Copy-Item $Aab $Signed -Force

Write-Host ""
Write-Host "서명합니다. 비밀번호를 물으면 입력하세요. 입력하는 글자는 화면에 보이지 않습니다." -ForegroundColor Cyan
& $Jarsigner -sigalg SHA256withRSA -digestalg SHA-256 -keystore $Keystore $Signed $Alias
if ($LASTEXITCODE -ne 0) { Remove-Item $Signed -ErrorAction SilentlyContinue; Write-Host "서명에 실패했습니다(비밀번호가 틀렸을 수 있습니다). 바뀐 것은 없습니다." -ForegroundColor Red; exit 1 }

& $Jarsigner -verify $Signed | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "서명을 확인하지 못했습니다." -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "완료. 서명된 파일:" -ForegroundColor Green
Write-Host "    $Signed"
Write-Host ""
Write-Host "업로드 열쇠 지문(SHA-256). 공개해도 되는 값입니다:" -ForegroundColor Cyan
& $Keytool -printcert -jarfile $Signed | Select-String "SHA256:"
Write-Host ""
Write-Host "다음: 플레이 콘솔 > 테스트 > 비공개 테스트 > 새 버전 만들기에서 이 파일을 올리세요."
if (-not $NoOpen) { Start-Process explorer.exe "/select,`"$Signed`"" }
