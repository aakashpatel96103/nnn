# 07 — Sound design (src/cues.json)

The mixer (`engine/mix.py` → `skills/edit-video/scripts/sfx-sync.mjs`) places each cue on its exact frame,
ducks SFX 6 dB under the voice, normalises to −14 LUFS, true peak −2.5 dBTP, and muxes with the silent video.

```json
{"fps":30, "total":18.2, "cues":[
  {"frame":0,   "sound":"curated/hook-impact.wav", "gain":-6, "label":"opening frame"},
  {"frame":62,  "sound":"curated/ui-pop.wav",      "gain":0,  "label":"FREE chips stamp"}
]}
```
- `total` is SECONDS (mix.py syncs it to project duration). `frame` = round(t × 30); frame wins over `t`.
- `sound`: a file in the pack (`skills/edit-video/assets/sfx/`, listed in its `manifest.json`), e.g.
  `curated/ui-click.wav`, `clean-ding.wav`, `tick.wav`, or a path relative to cues.json (e.g. `../assets/x.wav`).
- gain in dB (0 = as is). Typical: impacts −6, pops 0…−4, ticks −6…−10, swishes −3…−5.

## Which sound for which beat
| Beat | Sound |
|---|---|
| Opening frame (hook) | `curated/hook-impact.wav` −6 |
| Sticker / chip stamp | `curated/ui-pop.wav` |
| Cursor click / button | `curated/ui-click.wav` |
| Check mark (each) | `tick.wav` or `latch.wav` −6 |
| DONE / success / reveal | `clean-ding.wav` −4, `sparkle.wav`, `shimmer.wav` |
| Card arriving fast / camera move | `curated/zoom-swish.wav` −4 |
| Halftone wipe | `curated/zoom-swish.wav` at wipe start, optionally `curated/metallic-riser.wav` ending at peak |
| Typing | `typing-tick.wav` every 2–3 chars, −10 |
| Screenshot / copy | `curated/camera-shutter.wav` |
| Big number / heavy hit | `sub-impact.wav`, `thock.wav` |
| Follow click on end card | `curated/ui-click.wav` |

## Rules
- Every visible beat gets a sound; no sound without a visual. 5–15 cues per 15–20 s.
- Place on the frame the thing VISIBLY lands (the pop peak / the press), not when its animation starts —
  usually 2–4 frames after the animation start time.
- Never stack 3+ sounds within 100 ms. Keep ticks under the voice; the voice is king.
- No music by default (voice + SFX is the house sound). Music only if the user gives a licensed track; then add it
  as a cue at frame 0 with gain −22…−18.
- Verify: `python engine/mix.py projects/<slug> check` → look at strips for the main beats (waveform spike on the
  marker line). If the earshot tool exists you may also run its `timeline` on the export.
