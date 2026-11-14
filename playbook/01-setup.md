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
