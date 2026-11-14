# 01 — Setup

Run from the kit root:

```
python engine/doctor.py --install
python engine/doctor.py          # must end with READY
```

What it needs and installs:
| Need | How |
|---|---|
| Python 3.10+ | must exist. Windows `winget install Python.Python.3.12`, Mac `brew install python`, Linux apt |
| playwright + Chromium | `pip install --user playwright` + `python -m playwright install chromium` (renders the HTML frames) |
| openai-whisper | local speech-to-text with word timestamps (first run downloads the `small` model, ~460 MB) |
| numpy, pillow | contact sheets, analysis |
| edge-tts (optional) | AI voice fallback, only used with user consent |
| ffmpeg + ffprobe | Windows `winget install --id Gyan.FFmpeg -e`, Mac `brew install ffmpeg`, Linux `apt install ffmpeg` |
| Node 18+ | Windows `winget install --id OpenJS.NodeJS.LTS -e`, Mac `brew install node` (runs the SFX mixer, built-ins only, no npm install) |

Troubleshooting
- After winget/brew installs, PATH only refreshes in a NEW terminal. Tell the user, then rerun doctor.
- `ModuleNotFoundError: playwright` but pip says installed → you ran `python -I` or a different python. Use the same
  interpreter doctor printed.
- whisper needs torch; pip pulls it (big download). On slow internet warn the user before.
- `pip --user` blocked (externally-managed env on Linux/Mac) → use a venv: `python -m venv .venv` and activate it,
  then rerun doctor with that python.
- Chromium launch fails on Linux → `python -m playwright install-deps chromium`.

Smoke test (optional, ~1 min): `python engine/new_project.py smoke`, then
`python engine/render.py projects/smoke snap projects/smoke/review/s 1 5 11`, look at one PNG, then delete `projects/smoke`
(it is yours, created just now).

---

## Restricted / offline machine (no apt, no browser CDN)

Some sandboxes only allow `pypi.org`, `registry.npmjs.org` and `codeload.github.com`. There:
`sudo apt-get install ffmpeg` fails (no debian mirror), `python -m playwright install chromium` dies on
`cdn.playwright.dev`, and openai-whisper cannot fetch its `.pt` model from `openaipublic.azureedge.net`.
Use the offline installer instead (idempotent, safe to re-run, ends by running doctor):

```
bash setup/setup-offline.sh
python3 engine/doctor.py          # must print READY
```

What it does, and why each piece is safe:

| Need | Offline route | Notes |
|---|---|---|
| ffmpeg + ffprobe | npm `@ffmpeg-installer/linux-x64`, `@ffprobe-installer/linux-x64` → `/usr/local/bin` | static builds, no libs needed |
| Chromium for playwright | npm `@sparticuz/chromium` (headless shell) → `/opt/chrome153`, symlinked to every path playwright looks at; nss libs → `/usr/local/lib` + `ldconfig` | Chromium **153** vs the **159** this playwright expects — rendering is verified end-to-end; re-run the smoke test after a playwright upgrade |
| whisper | `whisper small` (int8 CTranslate2, 4 npm parts, sha256 checked) → `~/.cache/whisper-ct2/small` | `engine/transcribe.py` tries openai-whisper first and falls back to this dir with faster-whisper when the download fails. `--model base` etc. only uses openai-whisper |
| fonts | Inter (stands in for `Segoe UI`), Gelasio (Georgia metric twin) + aliases in `/etc/fonts/local.conf` | templates keep asking for the real font names, no template edits |

Caveats worth telling the user once:
- No apt, so no system font package: Devanagari/emoji glyphs are missing. The kit writes Hinglish in Latin
  letters anyway (`hi` + Latin script); if a reel needs Devanagari on screen, install that font first
  (e.g. `npm i @fontsource/noto-sans-devanagari`, convert the woff2 to ttf, drop it in
  `/usr/share/fonts/truetype/mukku/`).
- CPU-only: a 18 s reel takes ~5 min to render (546 frames through playwright). Whisper `small` int8
  transcribes ~17 s of speech in ~10 s.
- Nothing outside the repo is captured in a snapshot — after a fresh boot re-run `bash setup/setup-offline.sh`.
