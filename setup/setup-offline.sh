#!/usr/bin/env bash
# Setup for restricted / offline boxes (no apt, no debian mirrors, no cdn.playwright.dev,
# no GitHub release assets — only pypi.org + registry.npmjs.org + codeload.github.com).
#
#   bash setup/setup-offline.sh     # then: python3 engine/doctor.py  -> READY
#
# What it does (all idempotent, re-run any time):
#   python  : playwright, numpy, pillow, openai-whisper, edge-tts, faster-whisper, fonttools, brotli
#   ffmpeg  : static ffmpeg + ffprobe from npm  -> /usr/local/bin
#   chromium: @sparticuz/chromium headless shell -> /opt/chrome153 + playwright's expected paths
#   whisper : whisper "small" int8 (CTranslate2) from npm -> ~/.cache/whisper-ct2/small
#             (engine/transcribe.py falls back to it when openai-whisper cannot download its .pt)
#   fonts   : Inter (stands in for Segoe UI) + Gelasio (metric twin of Georgia) + fontconfig aliases
set -uo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)
PY=${PY:-python3}
WORK=${WORK:-/tmp/mukku-setup}
CHROME_PREFIX=${CHROME_PREFIX:-/opt/chrome153}
say() { printf '\n== %s\n' "$*"; }

mkdir -p "$WORK"

# ---------------------------------------------------------------- python packages
say "python packages ($PY)"
PKGS="playwright numpy pillow openai-whisper edge-tts faster-whisper fonttools brotli"
missing=""
for m in playwright numpy PIL whisper edge_tts faster_whisper fontTools brotli; do
  "$PY" -c "import $m" 2>/dev/null || missing="$missing $m"
done
if [ -n "$missing" ]; then
  # PEP 668 "externally managed" boxes need --break-system-packages; older pip doesn't know it
  "$PY" -m pip install --user -q $PKGS 2>/dev/null \
    || "$PY" -m pip install --user --break-system-packages -q $PKGS
  for m in $missing; do "$PY" -c "import $m" 2>/dev/null && echo "  ok $m" || echo "  MISS $m"; done
else
  echo "  all present"
fi

# ---------------------------------------------------------------- ffmpeg / ffprobe
say "ffmpeg + ffprobe"
if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null; then
  ( cd "$WORK" && npm install --no-save --no-audit --no-fund -s \
      @ffmpeg-installer/linux-x64 @ffprobe-installer/linux-x64 ) || exit 1
  sudo install -m 755 "$WORK/node_modules/@ffmpeg-installer/linux-x64/ffmpeg"  /usr/local/bin/ffmpeg
  sudo install -m 755 "$WORK/node_modules/@ffprobe-installer/linux-x64/ffprobe" /usr/local/bin/ffprobe
fi
ffmpeg -version 2>/dev/null | head -1; ffprobe -version 2>/dev/null | head -1

# ---------------------------------------------------------------- chromium for playwright
say "chromium for playwright"
if [ ! -x "$CHROME_PREFIX/chrome" ]; then
  ( cd "$WORK" && npm install --no-save --no-audit --no-fund -s @sparticuz/chromium ) || exit 1
  cat > "$WORK/extract.mjs" <<'JS'
import chromium from '@sparticuz/chromium';
import { brotliDecompressSync } from 'node:zlib';
import { readFileSync, writeFileSync } from 'node:fs';
console.log(await chromium.executablePath());              // -> /tmp/chromium
const tar = 'node_modules/@sparticuz/chromium/bin/al2023.tar.br';
writeFileSync('/tmp/mukku-al2023.tar', brotliDecompressSync(readFileSync(tar)));
JS
  ( cd "$WORK" && node extract.mjs ) || exit 1
  sudo mkdir -p "$CHROME_PREFIX"
  sudo install -m 755 /tmp/chromium "$CHROME_PREFIX/chrome"
  sudo tar -xf /tmp/mukku-al2023.tar -C "$CHROME_PREFIX"          # libnspr4/libnss3/... -> lib/
  sudo cp /tmp/libEGL.so /tmp/libGLESv2.so /tmp/libvk_swiftshader.so /tmp/libvulkan.so.1 \
          /tmp/vk_swiftshader_icd.json "$CHROME_PREFIX/" 2>/dev/null || true
  # make the nss libs resolvable for every process (playwright spawns the browser itself)
  sudo cp "$CHROME_PREFIX"/lib/*.so* /usr/local/lib/ && sudo ldconfig || true
fi
"$CHROME_PREFIX/chrome" --version || { echo "chromium will not start"; exit 1; }

# point playwright at it (headless=True launches the separate "headless shell" build, and
# chromium.executable_path only reports the headed one -> link every location playwright may use)
mapfile -t PWPATHS < <("$PY" - <<'PY' | sort -u
from playwright.sync_api import sync_playwright
from pathlib import Path
import re
with sync_playwright() as p:
    exe = Path(p.chromium.executable_path)          # .../ms-playwright/chromium-<rev>/<dir>/chrome
    print(exe)
    m = re.search(r"chromium(?:-headless_shell)?-(\d+)", str(exe))
    if m:
        base = next(a for a in exe.parents if a.name.startswith("chromium"))
        for name in (f"chromium-{m.group(1)}", f"chromium_headless_shell-{m.group(1)}"):
            for rel in (("chrome-linux64", "chrome"), ("chrome-linux", "chrome"),
                        ("chrome-headless-shell-linux64", "chrome-headless-shell")):
                print(base.parent / name / rel[0] / rel[1])
PY
)
for p in "${PWPATHS[@]:-}"; do
  [ -n "${p:-}" ] || continue
  mkdir -p "$(dirname "$p")" 2>/dev/null || sudo mkdir -p "$(dirname "$p")"
  ln -sfn "$CHROME_PREFIX/chrome" "$p" 2>/dev/null || sudo ln -sfn "$CHROME_PREFIX/chrome" "$p"
  echo "  linked $p"
done

# ---------------------------------------------------------------- whisper model (local, CT2)
say "whisper small model -> ~/.cache/whisper-ct2/small"
CT2="$HOME/.cache/whisper-ct2/small"
if [ ! -f "$CT2/model.bin" ]; then
  ( cd "$WORK" && npm install --no-save --no-audit --no-fund -s \
      @skillninja/shortmovie-telop-model-p0 @skillninja/shortmovie-telop-model-p1 \
      @skillninja/shortmovie-telop-model-p2 @skillninja/shortmovie-telop-model-p3 ) || exit 1
  B="$WORK/node_modules/@skillninja"; mkdir -p "$CT2"
  for i in 0 1 2 3; do cat "$B/shortmovie-telop-model-p$i/model.bin.part$i"; done > "$CT2/model.bin"
  cp "$B"/shortmovie-telop-model-p0/{config.json,tokenizer.json,vocabulary.json,preprocessor_config.json} "$CT2"/
  want=$(cat "$B/shortmovie-telop-model-p0/model.sha256"); got=$(sha256sum "$CT2/model.bin" | cut -d' ' -f1)
  [ "$want" = "$got" ] && echo "  sha256 ok ($(du -h "$CT2/model.bin" | cut -f1))" || { echo "  SHA MISMATCH"; exit 1; }
else
  echo "  already there ($(du -h "$CT2/model.bin" | cut -f1))"
fi

# ---------------------------------------------------------------- fonts
say "fonts (Inter ~ Segoe UI, Gelasio ~ Georgia)"
if [ ! -f /usr/share/fonts/truetype/mukku/gelasio-400-italic.ttf ]; then
  ( cd "$WORK" && npm install --no-save --no-audit --no-fund -s @fontsource/inter @fontsource/gelasio ) || exit 1
  "$PY" - "$WORK/node_modules" <<'PY'
import os, sys
from fontTools.ttLib import TTFont
src, out = sys.argv[1], "/tmp/mukku-ttf"; os.makedirs(out, exist_ok=True)
for fam, weights in (("inter", ["400","600","700","800","900"]), ("gelasio", ["400","700"])):
    for w in weights:
        for style in ("normal","italic"):
            f = f"{src}/@fontsource/{fam}/files/{fam}-latin-{w}-{style}.woff2"
            if os.path.exists(f):
                ft = TTFont(f); ft.flavor = None; ft.save(f"{out}/{fam}-{w}-{style}.ttf")
PY
  sudo mkdir -p /usr/share/fonts/truetype/mukku
  sudo cp /tmp/mukku-ttf/*.ttf /usr/share/fonts/truetype/mukku/
  sudo tee /etc/fonts/local.conf >/dev/null <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <!-- Mukku Reel Kit: stand-ins for the Windows/Mac fonts the templates ask for -->
  <match target="pattern">
    <test qual="any" name="family"><string>Segoe UI</string></test>
    <edit name="family" mode="assign" binding="same"><string>Inter</string></edit>
  </match>
  <match target="pattern">
    <test qual="any" name="family"><string>Georgia</string></test>
    <edit name="family" mode="assign" binding="same"><string>Gelasio</string></edit>
  </match>
  <match target="pattern">
    <test qual="any" name="family"><string>Arial</string></test>
    <edit name="family" mode="assign" binding="same"><string>Inter</string></edit>
  </match>
</fontconfig>
XML
  command -v fc-cache >/dev/null && sudo fc-cache -f >/dev/null 2>&1
  echo "  installed"
else
  echo "  already installed"
fi

# ---------------------------------------------------------------- done
say "doctor"
"$PY" engine/doctor.py
