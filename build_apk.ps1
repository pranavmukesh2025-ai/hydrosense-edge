$ErrorActionPreference = "Stop"

$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

$JAVA_HOME = $env:JAVA_HOME
$JAVAC = "$JAVA_HOME\bin\javac.exe"
$JAR = "$JAVA_HOME\bin\jar.exe"
$KEYTOOL = "$JAVA_HOME\bin\keytool.exe"

$SDK_DIR = "$env:LOCALAPPDATA\Android\Sdk"
$BUILD_TOOLS = "$SDK_DIR\build-tools\36.1.0"
$ANDROID_JAR = "$SDK_DIR\platforms\android-36.1\android.jar"

$AAPT2 = "$BUILD_TOOLS\aapt2.exe"
$D8 = "$BUILD_TOOLS\d8.bat"
$ZIPALIGN = "$BUILD_TOOLS\zipalign.exe"
$APKSIGNER = "$BUILD_TOOLS\apksigner.bat"

Write-Host "=== Starting HydroSense Edge APK Build ===" -ForegroundColor Cyan

# Clean & create directories
New-Item -ItemType Directory -Force -Path "android_build\gen" | Out-Null
New-Item -ItemType Directory -Force -Path "android_build\obj" | Out-Null
New-Item -ItemType Directory -Force -Path "android_build\dex" | Out-Null

# 1. Compile Resources with AAPT2
Write-Host "1. Compiling resources with aapt2..." -ForegroundColor Yellow
& $AAPT2 compile --dir "android_build\res" -o "android_build\compiled_res.zip"

# 2. Link Resources, Assets & Manifest
Write-Host "2. Linking resources and generating R.java..." -ForegroundColor Yellow
& $AAPT2 link -I $ANDROID_JAR --manifest "android_build\AndroidManifest.xml" -o "android_build\unaligned.apk" -A "android_build\assets" --java "android_build\gen" "android_build\compiled_res.zip" --auto-add-overlay

# 3. Compile Java Source Code
Write-Host "3. Compiling Java sources with javac..." -ForegroundColor Yellow
$javaFiles = Get-ChildItem -Path "android_build\gen", "android_build\src" -Filter *.java -Recurse | Select-Object -ExpandProperty FullName
& $JAVAC -source 1.8 -target 1.8 -cp $ANDROID_JAR -d "android_build\obj" $javaFiles

# 4. Convert .class to classes.dex with D8
Write-Host "4. Converting bytecode to classes.dex with D8..." -ForegroundColor Yellow
$classFiles = Get-ChildItem -Path "android_build\obj" -Filter *.class -Recurse | Select-Object -ExpandProperty FullName
& $D8 --output "android_build\dex" --lib $ANDROID_JAR $classFiles

# 5. Add classes.dex into unaligned.apk
Write-Host "5. Packaging classes.dex into APK container..." -ForegroundColor Yellow
Set-Location "android_build\dex"
& $JAR -uf "..\unaligned.apk" "classes.dex"
Set-Location "c:\Users\HOME\hydrosense"

# 6. Zipalign APK (4-byte alignment)
Write-Host "6. Aligning APK with zipalign..." -ForegroundColor Yellow
if (Test-Path "android_build\aligned.apk") { Remove-Item "android_build\aligned.apk" -Force }
& $ZIPALIGN -p 4 "android_build\unaligned.apk" "android_build\aligned.apk"

# 7. Generate Keystore if needed
if (-not (Test-Path "android_build\debug.keystore")) {
    Write-Host "7. Generating signing keystore..." -ForegroundColor Yellow
    & $KEYTOOL -genkeypair -v -keystore "android_build\debug.keystore" -alias "hydrosense" -keyalg RSA -keysize 2048 -validity 10000 -storepass "hydrosense123" -keypass "hydrosense123" -dname "CN=HydroSense, OU=Edge, O=HydroSense, L=SF, ST=CA, C=US"
}

# 8. Sign APK with apksigner
Write-Host "8. Signing APK with apksigner..." -ForegroundColor Yellow
$FINAL_APK = "c:\Users\HOME\hydrosense\HydroSense_Edge.apk"
if (Test-Path $FINAL_APK) { Remove-Item $FINAL_APK -Force }
& $APKSIGNER sign --ks "android_build\debug.keystore" --ks-pass "pass:hydrosense123" --out $FINAL_APK "android_build\aligned.apk"

# 9. Verify APK Signature
Write-Host "9. Verifying APK signature..." -ForegroundColor Yellow
& $APKSIGNER verify -v $FINAL_APK

Write-Host "=== BUILD SUCCESSFUL ===" -ForegroundColor Green
Write-Host "Output APK: $FINAL_APK" -ForegroundColor Green
$apkSize = (Get-Item $FINAL_APK).Length / 1MB
Write-Host "APK Size: $([math]::Round($apkSize, 2)) MB" -ForegroundColor Green
