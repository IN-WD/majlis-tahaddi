#!/usr/bin/env bash
# Build and sign the Android APK from android/ using apktool + apksigner.
# Requirements: Java 17+, apktool 2.9+ (https://apktool.org), apksigner (Android SDK build-tools).
# Usage: APKTOOL=/path/apktool.jar APKSIGNER=/path/apksigner.jar KEYSTORE=my.jks KS_PASS=... ./tools/build_apk.sh
set -euo pipefail
cd "$(dirname "$0")/.."
: "${APKTOOL:?set APKTOOL to apktool.jar}" "${APKSIGNER:?set APKSIGNER to apksigner.jar}" "${KEYSTORE:?set KEYSTORE}" "${KS_PASS:?set KS_PASS}"
ALIAS="${KS_ALIAS:-majlis}"
mkdir -p build
java -jar "$APKTOOL" b android -o build/unsigned.apk --use-aapt2
python3 tools/zipalign.py build/unsigned.apk build/aligned.apk
java -jar "$APKSIGNER" sign --ks "$KEYSTORE" --ks-pass "pass:$KS_PASS" --ks-key-alias "$ALIAS" \
  --min-sdk-version 21 --out build/majlis-tahaddi.apk build/aligned.apk
java -jar "$APKSIGNER" verify build/majlis-tahaddi.apk && echo "Built build/majlis-tahaddi.apk"
