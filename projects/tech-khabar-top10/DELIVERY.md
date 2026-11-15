# DELIVERY — Top 10 Tech Khabar (14 Nov 2026)

## File
`export/tech-khabar-top10.mp4`
- 1920×1080, 30 fps, H.264 high (yuv420p, +faststart), AAC 48 kHz stereo
- Duration **166.1 s (2:46)**, 31 MB, ~1.53 Mbps
- sha256 start: `32481182b5a17338…`

## Verification (run on the delivered file)
| Check | Result |
|---|---|
| Resolution / fps / duration | 1920×1080 · 30/1 · 166.100 s ✅ |
| Loudness (EBU R128) | **−14.1 LUFS** ✅ (target −14 ±1.5) |
| True peak | **−3.5 dBTP** ✅ (≤ −2.5) |
| QA script (`src/qa169.py --video …`) | **0 FAIL, 0 WARN → PASS** |
| Sfx sync (`engine/mix.py … check`) | 26 struck cues placed, **worst 0 ms** ✅ |
| Scene sheet (14 scenes) | `review/final_sheet.jpg` — no overflow / no empty column |
| Comment CTA visible | `review/f146.jpg`, `review/f161.jpg` ✅ |
| Cover frame | `review/cover.jpg` (t=34.5, GTA6 212 GB scene) |

## What changed vs v2
Audio same, visuals same — **comment CTA add** hua (audio ke CTA ke mutabik):
slide-in sticker `Comment karo "GTA"` + end-card chip + `GTA.` word pill, plus 1 naya cue
(`curated/ui-pop.wav` at the GTA word). Cues 27 → 28.

## Review artifacts
```
review/silent.mp4          # video-only master before mux (26 MB)
review/mix.wav             # ducked mix (−14.1 LUFS)
review/strips/sync-0*.jpg  # audio↔frame sync strips
review/final_sheet.jpg     # 14-scene contact sheet from the final mp4
review/f*.jpg, cover.jpg   # spot frames (comment CTA + cover)
review/qa.txt              # QA log
review/sheet169.jpg        # earlier snap sheet
```

## Assets / sources
- `inputs/vo.mp3` — user's voice-over (ElevenLabs "Ranga" Hindi narrator), untouched.
- `inputs/script.txt` — transcript (Latin, for word timings).
- `src/words.json`, `src/cues.json` — 449 words / 28 cues.
- `assets/avatar.png` — **not used** (user ne mukku avatar mana kiya; TK monogram instead).
- Facts: Apple, Rockstar Newswire, Nikkei/ABB, Reuters, US DOJ (SDNY), Nitori, Paris Call for AI Safety,
  Google Gemini API pricing, Anthropic. **DOJ ka figure $129M hai, audio me $139M** — audio wala rakha, caption me note.

## Honest gaps
- Render 2-core sandbox pe ~40 min chala; frame-level QA DOM checks sample points par hain, har frame par nahi.
- Captions word-by-word hain lekin forced-align timings `words.json` se aate hain (≈±30 ms), ear-check nahi hua.
- Music nahi hai — sirf voice + SFX (user ne music nahi maanga).

## Reproduce
```bash
bash /home/user/.mukku-setup.sh          # toolchain (playwright, ffmpeg, chromium, fonts)
cd projects/tech-khabar-top10
python3 src/make_cues.py
python3 src/render169.py . video review/silent.mp4 --crf=17 --preset=veryfast
cd ../.. && python3 engine/mix.py projects/tech-khabar-top10
python3 projects/tech-khabar-top10/src/qa169.py projects/tech-khabar-top10 --video projects/tech-khabar-top10/export/tech-khabar-top10.mp4
```
